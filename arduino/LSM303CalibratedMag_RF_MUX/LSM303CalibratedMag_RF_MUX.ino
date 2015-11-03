/*
 * SIMPLE CALIBRATION OF MAGNETOMETER DATA
 *      FOR MULTIPLE SENSORS, MUXXED TOGETHER
 * 
 * You just take a nr of measurements, waving your sensor around.
 * Then you calculate the hard iron offset, by aligning the values around the center
 * To calculate the soft iron offset (scale factor), 
 * you take the average radius of the 3 directions, which is the average radius
 * and calculate a scale factor for each axis, to scale the measurments to this radius
 * 
 * according to: 
 * https://github.com/kriswiner/MPU-6050/wiki/Simple-and-Effective-Magnetometer-Calibration
 * 
 */

#include <Wire.h>
#include <LSM303.h>
#include <RFduinoBLE.h>

LSM303 compass;
float magX, magY, magZ, rawX, rawY, rawZ;
float minData[4][3] = {{10000, 10000, 10000},
                        {10000, 10000, 10000},
                        {10000, 10000, 10000},
                        {10000, 10000, 10000}};
float maxData[4][3] = {{-10000, -10000, -10000},
                        {-10000, -10000, -10000},
                        {-10000, -10000, -10000},
                        {-10000, -10000, -10000}};
float hardBias[4][3];
float softBias[4][3];
char dataHard[12];
char dataSoft[12];

//pins
int s0 = 0;
int s1 = 1;
int s2 = 2;
int s3 = 3;
int s4 = 4;

//datasheet p.10: resolution of 0.16 mgauss/LSB
float conversionFactorMag = 0.479;   //for range +-12gauss
int sampleNum = 1000;

void setup()
{
  //Serial.begin(9600);
  Wire.beginOnPins(5,6);    //SCL on GPIO 5, SDA on GPIO 6
  
  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);
  digitalWrite(s0, LOW);
  digitalWrite(s1, LOW);
  digitalWrite(s2, LOW);
  digitalWrite(s3, LOW);

  pinMode(s4, INPUT);
  //digitalWrite(s4, LOW);
  
  delay(50);

  //set up the magnetic range for each sensor
  for(int i=0; i<4; i++){
    setChannel(i);
    delay(50);
    compass.init();
    compass.enableDefault();
    compass.writeReg(compass.CTRL5, 0x74);    // put magnetic data rate to 100 Hz
    compass.writeReg(compass.CTRL6, 0x60);    // put magnetic scale to +-12 gauss
  }
  
  RFduinoBLE.deviceName = "magnetic";
  RFduinoBLE.advertisementData = "magField";
  RFduinoBLE.begin();

  calibrateCompass();
}

void loop()
{  
  //getMagnetCali();

  //output is in [mgauss]
  for(int i=0; i<4; i++){
    RFduinoBLE.sendInt(i);
    for(int j=0; j<3; j++){
      memcpy(&dataHard[j*sizeof(float)], &hardBias[i][j], sizeof(float));
      memcpy(&dataSoft[j*sizeof(float)], &softBias[i][j], sizeof(float));
    }
    RFduinoBLE.send(dataHard,12);
    delay(50);
    RFduinoBLE.send(dataSoft,12);
    delay(50);
  }
  
  delay(1000);
}

void setChannel(int ch){
  int controlPin[] = {s0, s1, s2, s3};

  int muxChannel[16][4]={
    {0,0,0,0}, //channel 0
    {1,0,0,0}, //channel 1
    {0,1,0,0}, //channel 2
    {1,1,0,0}, //channel 3
    {0,0,1,0}, //channel 4
    {1,0,1,0}, //channel 5
    {0,1,1,0}, //channel 6
    {1,1,1,0}, //channel 7
    {0,0,0,1}, //channel 8
    {1,0,0,1}, //channel 9
    {0,1,0,1}, //channel 10
    {1,1,0,1}, //channel 11
    {0,0,1,1}, //channel 12
    {1,0,1,1}, //channel 13
    {0,1,1,1}, //channel 14
    {1,1,1,1}  //channel 15
  };

  for(int i=0; i<4; i++){
    digitalWrite(controlPin[i], muxChannel[ch][i]);
  }
}

void getMagnetCali(int cnt){
 setChannel(cnt);
 getRawMagnet();
 
 magX = (rawX - hardBias[cnt][0]) * softBias[cnt][0];
 magY = (rawY - hardBias[cnt][1]) * softBias[cnt][1];
 magZ = (rawZ - hardBias[cnt][2]) * softBias[cnt][2];
  
}

//in [mT]
void getRawMagnet(){    
    while(compass.readReg(compass.STATUS_M) <= 0x0F);     
    compass.readMag();

    rawX = compass.m.x * conversionFactorMag;
    rawY = compass.m.y * conversionFactorMag;
    rawZ = compass.m.z * conversionFactorMag;
}

void getMinMaxData(){ 
 for(int i = 0; i < sampleNum; i++){
  for(int s = 0; s<4; s++){
    setChannel(s);
    delay(50);
    getRawMagnet();
    //updating the minimum
    minData[s][0] = min(minData[s][0], rawX);
    minData[s][1] = min(minData[s][1], rawY);
    minData[s][2] = min(minData[s][2], rawZ);
    //updating the maximum
    maxData[s][0] = max(maxData[s][0], rawX);
    maxData[s][1] = max(maxData[s][1], rawY);
    maxData[s][2] = max(maxData[s][2], rawZ);     
  } 
  if(!(i%20)) RFduinoBLE.sendInt(i); 
 }
}

void calcHardBias(int cnt){
 hardBias[cnt][0] = (maxData[cnt][0] + minData[cnt][0])/2; 
 hardBias[cnt][1] = (maxData[cnt][1] + minData[cnt][1])/2;
 hardBias[cnt][2] = (maxData[cnt][2] + minData[cnt][2])/2;  

 /*Serial.print("hardBias:\t");
 Serial.print(hardBias[cnt][0]); Serial.print("\t");
 Serial.print(hardBias[cnt][1]); Serial.print("\t");
 Serial.println(hardBias[cnt][2]);*/
}

void calcSoftBias(int cnt){
  float tempX = (maxData[cnt][0] + abs(minData[cnt][0]))/2;
  float tempY = (maxData[cnt][1] + abs(minData[cnt][1]))/2;
  float tempZ = (maxData[cnt][2] + abs(minData[cnt][2]))/2;
  
  float rad = (tempX + tempY + tempZ) / 3;
  
  softBias[cnt][0] = rad/tempX;
  softBias[cnt][1] = rad/tempY;
  softBias[cnt][2] = rad/tempZ;

  /*Serial.print("softBias:\t");
  Serial.print(softBias[cnt][0]); Serial.print("\t");
  Serial.print(softBias[cnt][1]); Serial.print("\t");
  Serial.println(softBias[cnt][2]);*/
}

void calibrateCompass(){
  
  while(digitalRead(s4) == HIGH){    // wait till user initiates the data collection
    RFduinoBLE.sendInt(99);
  }
  getMinMaxData();
  for(int i = 0; i<4; i++){    
    delay(50);    
    calcHardBias(i);
    calcSoftBias(i);
  }  
}




/*
 * SIMPLE CALIBRATION OF MAGNETOMETER DATA
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
float minData[3] = {10000, 10000, 10000};
float maxData[3] = {-10000, -10000, -10000};
float hardBias[3];
float softBias[3];
//datasheet p.10: resolution of 0.16 mgauss/LSB

float conversionFactor = 0.479;   //for range +-12gauss
int sampleNum = 2000;

void setup()
{
  Serial.begin(9600);
  Wire.beginOnPins(5,6);    //SCL on GPIO 5, SDA on GPIO 6
  compass.init();
  compass.enableDefault();
  compass.writeReg(compass.CTRL6, 0x60);    //set magnetic range to +-12gauss
  
  calibrateCompass();
}

void loop()
{  
  getMagnetCali();

  //output is in [mgauss]
  /*Serial.print("mag\t");
  Serial.print(magX);
  Serial.print("\t");
  Serial.print(magY);
  Serial.print("\t");
  Serial.println(magZ);*/
 
}

void getMagnetCali(){
 getRawMagnet();
 
 magX = (rawX - hardBias[0]) * softBias[0];
 magY = (rawY - hardBias[1]) * softBias[1];
 magZ = (rawZ - hardBias[2]) * softBias[2];
  
}

//in [mT]
void getRawMagnet(){
   
  compass.readMag();

  rawX = compass.m.x * conversionFactor;
  rawY = compass.m.y * conversionFactor;
  rawZ = compass.m.z * conversionFactor;
}

void getMinMaxData(){
 for(int i = 0; i < sampleNum; i++){
  getRawMagnet();
  //finding the minimum
  minData[0] = min(minData[0], rawX);
  minData[1] = min(minData[1], rawY);
  minData[2] = min(minData[2], rawZ);
  //finding the maximum
  maxData[0] = max(maxData[0], rawX);
  maxData[1] = max(maxData[1], rawY);
  maxData[2] = max(maxData[2], rawZ);  
  Serial.print("Taking measurement nr: "); Serial.println(i);
  //Serial.print(rawX);Serial.print("\t");
  //Serial.print(rawY);Serial.print("\t");
  //Serial.println(rawZ);
 }  
}

void calcHardBias(){
 hardBias[0] = (maxData[0] + minData[0])/2; 
 hardBias[1] = (maxData[1] + minData[1])/2;
 hardBias[2] = (maxData[2] + minData[2])/2;  

 Serial.print("hardBias:\t");
 Serial.print(hardBias[0]); Serial.print("\t");
 Serial.print(hardBias[1]); Serial.print("\t");
 Serial.println(hardBias[2]);
}

void calcSoftBias(){
  float tempX = (maxData[0] + abs(minData[0]))/2;
  float tempY = (maxData[1] + abs(minData[1]))/2;
  float tempZ = (maxData[2] + abs(minData[2]))/2;
  
  float rad = (tempX + tempY + tempZ) / 3;
  
  softBias[0] = rad/tempX;
  softBias[1] = rad/tempY;
  softBias[2] = rad/tempZ;

  Serial.print("softBias:\t");
  Serial.print(softBias[0]); Serial.print("\t");
  Serial.print(softBias[1]); Serial.print("\t");
  Serial.println(softBias[2]);
}

void calibrateCompass(){
  
  while(!Serial.find("ready")){
    Serial.println("Waiting for user to type 'ready'. Then wave your magnetometer around to collect data");
    delay(1000);
  }
  getMinMaxData();
  calcHardBias();
  calcSoftBias();
}




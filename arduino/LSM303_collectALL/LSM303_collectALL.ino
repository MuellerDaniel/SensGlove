/*
 * COLLECTING AND SENDING ALL THE DATA OF THE SENSOR
 * 
 * 
 */
#include "Wire.h"
#include <RFduinoBLE.h>
#include <stdio.h>
#include <LSM303.h>
#include <L3G.h>

LSM303 compass;
L3G gyro;

float magX[4], magY[4], magZ[4], rawX[4], rawY[4], rawZ[4];

/*float hardBias[4][3] = {{0, 0, 0},
                        {0, 0, 0},
                        {0, 0, 0},
                        {0, 0, 0}};
float softBias[4][3] = {{1, 1, 1},
                        {1, 1, 1},
                        {1, 1, 1},
                        {1, 1, 1}};*/                         
/*float offFree[4][3] = {{72.621156801701048, 7.2729417646131465, 80.228360877530477},
                        {72.621156801701048, 7.2729417646131465, 80.228360877530477},
                        {72.621156801701048, 7.2729417646131465, 80.228360877530477},
                        {72.621156801701048, 7.2729417646131465, 80.228360877530477}};*/
float offFree[4][3] = {{0.0, 0.0, 0.0},
                        {0.0, 0.0, 0.0},
                        {0.0, 0.0, 0.0},
                        {0.0, 0.0, 0.0}};
                        
float smoothMagX[4] = {0.0, 0.0, 0.0, 0.0};
float smoothMagY[4] = {0.0, 0.0, 0.0, 0.0};
float smoothMagZ[4] = {0.0, 0.0, 0.0, 0.0};
                        
//float conversionFactor = 0.080;  //for range +-2gauss
float conversionFactor = 0.160;  //for range +-4gauss
//float conversionFactor = 0.320;  //for range +-8gauss
//float conversionFactor = 0.479;  //for range +-12gauss

char data[16];
float fData[4][4];
int sensCnt = 4;    //Number of sensors
int a = 0;
float alphaMag = 0.15;
//float alphaMag = 1.0;

//pins
int s0 = 0;
int s1 = 1;
int s2 = 2;
int s3 = 3;
int ledPin = 4;

void setup() {
    //Serial.begin(9600);     //you have not enough gpios to use serial communication...
    //Wire.begin();
    //Serial.println("here setup");
    Wire.beginOnPins(5,6);    //SCL on GPIO 5, SDA on GPIO 6
    // set up the signal pins
    pinMode(s0, OUTPUT);
    pinMode(s1, OUTPUT);
    pinMode(s2, OUTPUT);
    pinMode(s3, OUTPUT);
    //pinMode(ledPin, OUTPUT);
    digitalWrite(s0, LOW);
    digitalWrite(s1, LOW);
    digitalWrite(s2, LOW);
    digitalWrite(s3, LOW);
    delay(50);

    //set up the magnetic range for each sensor
    for(int i=0; i<4; i++){      
      setChannel(i);      
      //setChannel(0);
      delay(50);      
      compass.init();            
      //digitalWrite(ledPin,LOW);
      compass.enableDefault();
      compass.writeReg(compass.CTRL5, 0x74);    // put magnetic data rate to 100 Hz
      //compass.writeReg(compass.CTRL6, 0x00);    // put magnetic scale to +-2 gauss
      compass.writeReg(compass.CTRL6, 0x20);    // put magnetic scale to +-4 gauss
      //compass.writeReg(compass.CTRL6, 0x40);    // put magnetic scale to +-8 gauss
      //compass.writeReg(compass.CTRL6, 0x60);    // put magnetic scale to +-12 gauss
      
    }
    
    RFduinoBLE.deviceName = "magnetic";
    RFduinoBLE.advertisementData = "magField";
    RFduinoBLE.begin();
    
}

void loop() {      

  getMagnetCali();
  
  for(int a = 0; a<sensCnt; a++){
    //setChannel(a);
    //getMagnet(a);
    
    fData[a][0] = a;
    fData[a][1] = magX[a];
    fData[a][2] = magY[a];
    fData[a][3] = magZ[a];   
  }

  // for sending via BLE
  for(int i = 0; i<4; i++){
    for(int j = 0; j<4; j++){
      memcpy(&data[j*sizeof(float)], &fData[i][j], sizeof(float));
    }      
    RFduinoBLE.send(data, 16);      
  }
  
  
  // serial output
  /*for(int i=0; i<4; i++){
    Serial.print(i); Serial.print("\t");
    Serial.print(magX[i]); Serial.print("\t");
    Serial.print(magY[i]); Serial.print("\t");
    Serial.println(magZ[i]);
  }*/

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


void getRawMagnet(int channel){
  //setChannel(channel);
  while(compass.readReg(compass.STATUS_M) <= 0x0F);
  compass.readMag();

  smoothingMag(&compass.m.x, &smoothMagX[channel]);
  smoothingMag(&compass.m.y, &smoothMagY[channel]);
  smoothingMag(&compass.m.z, &smoothMagZ[channel]);

  rawX[channel] = smoothMagX[channel] * conversionFactor;
  rawY[channel] = smoothMagY[channel] * conversionFactor;
  rawZ[channel] = smoothMagZ[channel] * conversionFactor;

  /*rawX = compass.m.x * conversionFactor;
  rawY = compass.m.y * conversionFactor;
  rawZ = compass.m.z * conversionFactor;*/

}

// updates all 4 sensor readings
void getMagnetCali(){   
  for(int i=0; i<4; i++){
    setChannel(i);
    //setChannel(0);
    getRawMagnet(i);
    // off Freescale approach
    magX[i] = rawX[i]-offFree[i][0];
    magY[i] = rawY[i]-offFree[i][1];
    magZ[i] = rawZ[i]-offFree[i][2];
  }
}

void smoothingMag(short int *raw, float *smooth){
  //*smooth = (*raw * alphaMag) - (*smooth * (1-alphaMag));
  *smooth = *smooth + alphaMag*(*raw-*smooth);
}

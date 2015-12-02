/*
 * COLLECTING AND SENDING THE CALIBRATED MAGNETOMETER DATA VIA BLUETOOTH
 * 
 * code for MULTIPLE sensors
 * for obtaining hard and soft iron values, run the "LSMCalibradetMag_RF.ino" script 
 * 
 */
#include "Wire.h"
#include <RFduinoBLE.h>
#include <stdio.h>
#include <LSM303.h>

LSM303 compass;

float magX, magY, magZ, rawX, rawY, rawZ;

//taking the measurements independently (not on the rack)
/*float hardBias[4][3] = {{36.64,  -3.11, 199.26},
                        {48.86, 27.30, 321.65},
                        {17.48, -38.56,  234.71},
                        {-30.42, 54.37, -179.39}};
float softBias[4][3] = {{0.99, 1.02, 1.00},
                         {0.97,  0.98,  1.05},
                         {1.06,  0.94,  1.01},
                         {1.00,  0.99,  1.01}};*/
// recorded on 23.10.15
/*float hardBias[4][3] = {{20.84,   26.35,  228.48},
                        {100.35,   23.47,    9.1},
                        {11.26,  48.86,  13.17},
                        {80.71,  -87.9 ,  279.26}};
float softBias[4][3] = {{1.0  ,  0.99,  1.01},
                         {0.97,  0.99,  1.05},
                         {0.98,  0.98,  1.04},
                         {1.02,  0.98,  1.01}};*/

/*float hardBias[4][3] = {{7.66,  -1.68, -55.8},
                        {86.94,    8.62, -150.17},
                        {33.29,  57.0  , -47.42},
                        {-71.13,  -29.7 ,  152.56}};
float softBias[4][3] = {{1.0  ,  1.01,  1.0},
                         {0.97,  1.  ,  1.04},
                         {0.98,  1.02,  1.0},
                         {1.02,  1.01,  0.97}};*/                                               

//recorded151101
/*float hardBias[4][3] = {{-34.25, -5.99, -52.45},
                        {29.94,   26.82, -186.09},
                        {-74.72,  64.19, -44.79},
                        {-85.26, -36.88, -11.26}};
float softBias[4][3] = {{1.01,  1.0  ,  1.0},
                         {0.98,  0.99,  1.03},
                         {0.98,  1.0  ,  1.02},
                         {1.04,  1.02,  0.94}};*/

float hardBias[4][3] = {{0, 0, 0},
                        {0, 0, 0},
                        {0, 0, 0},
                        {0, 0, 0}};
float softBias[4][3] = {{1, 1, 1},
                        {1, 1, 1},
                        {1, 1, 1},
                        {1, 1, 1}};                         

//float conversionFactorMag = 0.080;  //for range +-2gauss
//float conversionFactorMag = 0.160;  //for range +-4gauss
float conversionFactorMag = 0.320;  //for range +-8gauss
//float conversionFactorMag = 0.479;  //for range +-12gauss

char data[16];
float fData[4][4];
int sensCnt = 4;    //Number of sensors
int a = 0;

//pins
int s0 = 0;
int s1 = 1;
int s2 = 2;
int s3 = 3;

void setup() {
    //Serial.begin(9600);     //you have not enough gpios to use serial communication...
    Wire.beginOnPins(5,6);    //SCL on GPIO 5, SDA on GPIO 6
    // set up the signal pins
    pinMode(s0, OUTPUT);
    pinMode(s1, OUTPUT);
    pinMode(s2, OUTPUT);
    pinMode(s3, OUTPUT);
    digitalWrite(s0, LOW);
    digitalWrite(s1, LOW);
    digitalWrite(s2, LOW);
    digitalWrite(s3, LOW);
    delay(50);

    //set up the magnetic range for each sensor
    for(int i=0; i<4; i++){
      setChannel(i);
      delay(50);
      compass.init();
      compass.enableDefault();
      compass.writeReg(compass.CTRL5, 0x74);    // put magnetic data rate to 100 Hz
      //compass.writeReg(compass.CTRL6, 0x00);    // put magnetic scale to +-2 gauss
      //compass.writeReg(compass.CTRL6, 0x20);    // put magnetic scale to +-4 gauss
      compass.writeReg(compass.CTRL6, 0x40);    // put magnetic scale to +-8 gauss
      //compass.writeReg(compass.CTRL6, 0x60);    // put magnetic scale to +-12 gauss
    }
    
    RFduinoBLE.deviceName = "magnetic";
    RFduinoBLE.advertisementData = "magField";
    RFduinoBLE.begin();
}

void loop() {   
    //int a = cnt%sensCnt;
    //float startTime = millis();
    for(int a = 0; a<sensCnt; a++){
      setChannel(a);
      getMagnetCali(a);
      
      fData[a][0] = a;
      fData[a][1] = magX;
      fData[a][2] = magY;
      fData[a][3] = magZ;   
    }
    //float endTime = millis();    
    //RFduinoBLE.sendFloat(endTime-startTime);
    
    for(int i = 0; i<sensCnt; i++){
      for(int j = 0; j<4; j++){
        memcpy(&data[j*sizeof(float)], &fData[i][j], sizeof(float));
      }      
      RFduinoBLE.send(data, 16);      
    }
    
    //a += 1;
    //a = a%4;
    //delay(100);
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

void getMagnetCali(int i){ 
 getRawMagnet();
  
 magX = (rawX - hardBias[i][0]) * softBias[i][0];
 magY = (rawY - hardBias[i][1]) * softBias[i][1];
 magZ = (rawZ - hardBias[i][2]) * softBias[i][2];
}

void getRawMagnet(){    
    while(compass.readReg(compass.STATUS_M) <= 0x0F);  
    compass.readMag();
    
    rawX = compass.m.x * conversionFactorMag;
    rawY = compass.m.y * conversionFactorMag;
    rawZ = compass.m.z * conversionFactorMag;
}


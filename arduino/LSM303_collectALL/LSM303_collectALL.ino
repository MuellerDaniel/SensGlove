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
// zero bias values
/*float offFree[4][3] = {{0.0, 0.0, 0.0},
                        {0.0, 0.0, 0.0},
                        {0.0, 0.0, 0.0},
                        {0.0, 0.0, 0.0}};
float scale[4] = {1.0, 1.0, 1.0, 1.0};*/
float offFree[4][3] = {{47.289612442372295, 15.181165609732277, 206.6271129712874},
                        {-141.89726315328829, -49.738964753578351, -351.58590700070096},
                        {-31.563006578399072, -64.617792909008344, -143.79092483501179},
                        {-128.65707944985073, -83.688955303444942, -313.42472501811159}};
float scale[4] = {0.997309043969, 1.01934260961, 0.983302110365, 1.0007045843};

float smoothMagX[4] = {0.0, 0.0, 0.0, 0.0};
float smoothMagY[4] = {0.0, 0.0, 0.0, 0.0};
float smoothMagZ[4] = {0.0, 0.0, 0.0, 0.0};

//float conversionFactor = 0.080;  //for range +-2gauss
float conversionFactor = 0.160;    //for range +-4gauss
//float conversionFactor = 0.320;  //for range +-8gauss
//float conversionFactor = 0.479;  //for range +-12gauss

char data[4][16];
const int sensCnt = 4;    //Number of sensors
float fData[sensCnt][4];
int a = 0;
float alphaMag = 0.3;
//float alphaMag = 1.0;

//pins
int s0 = 0;
int s1 = 1;
int s2 = 2;
int s3 = 3;
int ledPin = 1;

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

    pinMode(ledPin, OUTPUT);
    digitalWrite(ledPin, LOW);

    //set up the magnetic range for each sensor
    for(int i=0; i<4; i++){
      setChannel(i);
      //setChannel(0);
      delay(50);
      compass.init();
      //digitalWrite(ledPin,LOW);
      compass.enableDefault();
      
      compass.writeReg(compass.CTRL1, 0x00);    // set accelerometer in power-down mode
      //compass.writeReg(compass.CTRL5, 0x74);    // put magnetic data rate to 100 Hz
      compass.writeReg(compass.CTRL5, 0x70);    // put magnetic data rate to 50 Hz
      //compass.writeReg(compass.CTRL5, 0x6C);    // put magnetic data rate to 25 Hz
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

  //digitalWrite(ledPin,HIGH);

  for(int a = 0; a<sensCnt; a++){
    //setChannel(a);
    //getMagnet(a);

    fData[a][0] = a;
    fData[a][1] = magX[a];
    fData[a][2] = magY[a];
    fData[a][3] = magZ[a];
  }

  // for sending via BLE 
    for(int i = 0; i<sensCnt; i++){
      for(int j = 0; j<4; j++){
        memcpy(&data[i][j*sizeof(float)], &fData[i][j], sizeof(float));
      }
      while(!RFduinoBLE.send(data[i], 16));
    }

  


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
  for(int i=0; i<sensCnt; i++){
    setChannel(i);
    //setChannel(0);
    getRawMagnet(i);
    // off Freescale approach
    magX[i] = (rawX[i]-offFree[i][0])*scale[i];
    magY[i] = (rawY[i]-offFree[i][1])*scale[i];
    magZ[i] = (rawZ[i]-offFree[i][2])*scale[i];
  }
}

void smoothingMag(short int *raw, float *smooth){
  //*smooth = (*raw * alphaMag) - (*smooth * (1-alphaMag));
  *smooth = *smooth + alphaMag*(*raw-*smooth);
}

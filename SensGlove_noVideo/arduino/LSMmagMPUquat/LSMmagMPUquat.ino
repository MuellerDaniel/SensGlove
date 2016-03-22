/*
Based on the Madgwick algorithm found at:
 See: http://www.x-io.co.uk/open-source-imu-and-ahrs-algorithms/

 This code inherits all relevant liscenses and may be freely modified and redistributed.
 The MinIMU v1 has a roughly +/- 10degree accuracy
 The MinIMU v2 has a roughly +/- 1 degree accuracy
 */
#include <Wire.h>
#include <RFduinoBLE.h>
#include <LSM303.h>
#include <L3G.h>
#include <math.h>

#include "I2Cdev.h"
#include "helper_3dmath.h"
//#include "MPU9250_6Axis_MotionApps20.h"
//#include "MPU6050_9Axis_MotionApps41.h"
#include "MPU9250_9Axis_MotionApps41.h"
//#include "MPU6050.h" // not necessary if using MotionApps include file
#define MPU9250_INCLUDE_DMP_MOTIONAPPS41
#include "MPU9250.h"


#define alpha 0.15f

//L3G gyro;
LSM303 compass;
MPU9250 mpu;

long timer, printTimer;
float G_Dt;
int loopCount;

float q0;
float q1;
float q2;
float q3;
float beta;
float q0_I;
float q1_I;
float q2_I;
float q3_I;

float floatMagX,floatMagY,floatMagZ;

int i;

float magX[4], magY[4], magZ[4], rawX[4], rawY[4], rawZ[4];
float mag_I[4][3];
float offFree[4][3] = {{47.289612442372295, 15.181165609732277, 206.6271129712874},
                        {-141.89726315328829, -49.738964753578351, -351.58590700070096},
                        {-31.563006578399072, -64.617792909008344, -143.79092483501179},
                        {-128.65707944985073, -83.688955303444942, -313.42472501811159}};
float scale[4] = {0.997309043969, 1.01934260961, 0.983302110365, 1.0007045843};
// zero bias values
/*float offFree[4][3] = {{0.0, 0.0, 0.0},
                        {0.0, 0.0, 0.0},
                        {0.0, 0.0, 0.0},
                        {0.0, 0.0, 0.0}};
float scale[4] = {1.0, 1.0, 1.0, 1.0};*/
                                               
float smoothMagX[4] = {0.0, 0.0, 0.0, 0.0};
float smoothMagY[4] = {0.0, 0.0, 0.0, 0.0};
float smoothMagZ[4] = {0.0, 0.0, 0.0, 0.0};
float alphaMag = 0.15;

float smoothQ[4];
float alphaQ = 0.4;

float conversionFactor = 0.16;

float rotB[4][3];
int s0 = 0;
int s1 = 1;
int s2 = 2;
int s3 = 3;
int led = 4;
int sensCnt = 4;

int chMPU = 5;

Quaternion q;  
bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

char data[16];
float fData[4][4];


volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
void dmpDataReady() {
    mpuInterrupt = true;
}

void setup(){
    
  //Serial.begin(38400);
  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);
  pinMode(led, OUTPUT);
  digitalWrite(s0, LOW);
  digitalWrite(s1, LOW);
  digitalWrite(s2, LOW);
  digitalWrite(s3, LOW);
  digitalWrite(led, LOW);
  delay(50);

  setChannel(chMPU);
  Wire.beginOnPins(5,6);    //SCL on GPIO 5, SDA on GPIO 6
  
  //Serial.println("Keeping the device still and level during startup will yeild the best results");
  
  //Wire.begin();
  //TWBR = ((F_CPU / 400000) - 16) / 2;//set the I2C speed to 400KHz
  InitEarthMag();


  RFduinoBLE.deviceName = "magnetic";
  RFduinoBLE.advertisementData = "magField";
  RFduinoBLE.begin();
}



void loop(){

    getQuat();

    smoothQuat(&q.w, &smoothQ[0]);
    smoothQuat(&q.x, &smoothQ[1]);
    smoothQuat(&q.y, &smoothQ[2]);
    smoothQuat(&q.z, &smoothQ[3]);    
    q0 = smoothQ[0];
    q1 = smoothQ[1];
    q2 = smoothQ[2];
    q3 = smoothQ[3]; 

    // get magnetic
    getMagnetCali();

    // rotate the initial magnetic field and subtract it!
    relQuat();


    /*fData[0][0] = q0;
    fData[0][1] = q1;
    fData[0][2] = q2;
    fData[0][3] = q3;

    fData[1][0] = 1;     
    fData[1][1] = magX[0];
    fData[1][2] = magY[0];
    fData[1][3] = magZ[0]; */

    /*for(int a=0; a<sensCnt; a++){    
    fData[a][0] = a;     
    fData[a][1] = magX[a]-rotB[a][0];
    fData[a][2] = magY[a]-rotB[a][1];
    fData[a][3] = magZ[a]-rotB[a][2];*/
    /*fData[a][1] = magX[a];
    fData[a][2] = magY[a];
    fData[a][3] = magZ[a];*/
    //}

    // comparing the rotational data and the raw data...
    fData[0][0] = 0;     
    fData[0][1] = magX[0]-rotB[0][0];
    fData[0][2] = magY[0]-rotB[0][1];
    fData[0][3] = magZ[0]-rotB[0][2];  

    fData[2][0] = 1;     
    fData[2][1] = magX[1]-rotB[1][0];
    fData[2][2] = magY[1]-rotB[1][1];
    fData[2][3] = magZ[1]-rotB[1][2]; 

    fData[1][0] = 2;     
    fData[1][1] = magX[0];
    fData[1][2] = magY[0];
    fData[1][3] = magZ[0];       

    fData[3][0] = 3;     
    fData[3][1] = magX[1];
    fData[3][2] = magY[1];
    fData[3][3] = magZ[1]; 

    // for sending via BLE
    for(int i = 0; i<sensCnt; i++){
      for(int j = 0; j<4; j++){
        memcpy(&data[j*sizeof(float)], &fData[i][j], sizeof(float));
      }      
      RFduinoBLE.send(data, 16);      
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

void relQuat(){

  // delta quat q_delta = q*(q_I**-1)
  // because q_I is a unit quaternion: q_I**-1 = conj(q_I) = q0_I; -q1_I; -q2_I; -q3_I
  /*float a = q0*q0_I - q1*q1_I - q2*q2_I - q3*q3_I;    
  float b = q0*q1_I + q1*q0_I + q2*q3_I - q3*q2_I;
  float c = q0*q2_I - q1*q3_I + q2*q0_I + q3*q1_I;
  float d = q0*q3_I + q1*q2_I - q2*q1_I + q3*q0_I;*/
  float a = q0*q0_I + q1*q1_I + q2*q2_I + q3*q3_I;    
  float b = q0*q1_I - q1*q0_I - q2*q3_I + q3*q2_I;
  float c = q0*q2_I + q1*q3_I - q2*q0_I - q3*q1_I;
  float d = q0*q3_I - q1*q2_I + q2*q1_I - q3*q0_I;
  a = 1.0*a;    // is this necessary???
  b = -1.0*b;
  c = -1.0*c;
  d = -1.0*d;

  // calculate the rotation matrix
  float rot11 = a*a+b*b-c*c-d*d;
  float rot12 = 2*(b*c+a*d);
  float rot13 = 2*(b*d-a*c);
  float rot21 = 2*(b*c-a*d);
  float rot22 = a*a-b*b+c*c-d*d;
  float rot23 = 2*(c*d+a*b);
  float rot31 = 2*(b*d+a*c);
  float rot32 = 2*(c*d-a*b);
  float rot33 = a*a-b*b-c*c+d*d;

  // invert the rotation matrix
  float rotMat[3][3];
  rotMat[0][0] = rot11;
  rotMat[0][1] = rot12;
  rotMat[0][2] = rot13;
  rotMat[1][0] = rot21;
  rotMat[1][1] = rot22;
  rotMat[1][2] = rot23;
  rotMat[2][0] = rot31;
  rotMat[2][1] = rot32;
  rotMat[2][2] = rot33;

  /*float rotMatInv[3][3];
  inverseMat(rotMat,rotMatInv);
  // exchange the two matrices...
  for(int i=0; i<3; i++){
    for(int j=0; j<3; j++){
      rotMat[i][j] = rotMatInv[i][j];
    }
  }*/
  
  //float rotB[3];
  for(int i=0; i<sensCnt; i++){
    rotB[i][0] = rotMat[0][0]*mag_I[i][0] + rotMat[0][1]*mag_I[i][1] + rotMat[0][2]*mag_I[i][2];
    rotB[i][1] = rotMat[1][0]*mag_I[i][0] + rotMat[1][1]*mag_I[i][1] + rotMat[1][2]*mag_I[i][2];
    rotB[i][2] = rotMat[2][0]*mag_I[i][0] + rotMat[2][1]*mag_I[i][1] + rotMat[2][2]*mag_I[i][2];
  }
}

void inverseMat(float a[3][3], float resMat[3][3]){
  int i,j;
  //float resMat[3][3];
  float determinant = 0.0;
  for(i=0;i<3;i++){
      determinant = determinant + (a[0][i]*(a[1][(i+1)%3]*a[2][(i+2)%3] - a[1][(i+2)%3]*a[2][(i+1)%3]));
  }

  for(int j=0;j<3;j++){
    for(int i=0;i<3;i++){
    resMat[j][i] = (((a[(i+1)%3][(j+1)%3] * a[(i+2)%3][(j+2)%3]) -
                        (a[(i+1)%3][(j+2)%3]*a[(i+2)%3][(j+1)%3]))/ determinant);
    }
  }
}


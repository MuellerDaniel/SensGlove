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

#define ToRad(x) ((x) * 0.01745329252)  // *pi/180
#define ToDeg(x) ((x) * 57.2957795131)  // *180/pi
#define PI_FLOAT     3.14159265f
#define PIBY2_FLOAT  1.5707963f
#define GYRO_SCALE 0.07f
#define betaDef    0.08f

//To find the calibration values us the sketch included with the LSM303 driver from pololu
/*Change line 11 from

 compass.enableDefault();

 to

 compass.writeMagReg(LSM303_CRA_REG_M, 0x1C);
 compass.writeMagReg(LSM303_CRB_REG_M, 0x60);
 compass.writeMagReg(LSM303_MR_REG_M, 0x00);

 Then put the calibration values below

 */

/*#define compassXMax 216.0f
#define compassXMin -345.0f
#define compassYMax 210.0f
#define compassYMin -347.0f
#define compassZMax 249.0f
#define compassZMin -305.0f*/
// min: {-412.000000, -457.759979, -587.679992}    max: { 465.919982, 386.399993, 269.119995}
#define compassXMax 382.47f
#define compassXMin -390.35f
#define compassYMax 410.19f
#define compassYMin -407.37f
#define compassZMax 388.42f
#define compassZMin -407.49f
#define inverseXRange (float)(2.0 / (compassXMax - compassXMin))
#define inverseYRange (float)(2.0 / (compassYMax - compassYMin))
#define inverseZRange (float)(2.0 / (compassZMax - compassZMin))

#define alpha 0.15f

L3G gyro;
LSM303 compass;

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

float magnitude;

float pitch,roll,yaw;

float gyroSumX,gyroSumY,gyroSumZ;
float offSetX,offSetY,offSetZ;

float floatMagX,floatMagY,floatMagZ;
float smoothAccX,smoothAccY,smoothAccZ;
float accToFilterX,accToFilterY,accToFilterZ;

int i;

float magX[4], magY[4], magZ[4], rawX[4], rawY[4], rawZ[4];
float mag_I[4][3];
float offFree[4][3] = {{-10.593081023300208, 24.579511558952198, 90.524286346616691},
                        {-279.968733070989, -37.346796794462108, -113.03551381450113},
                        {-137.35784880551591, -48.789818724974339, -191.0888554775963},
                        {-217.83551623598899, -74.78415090501646, -348.32616187395695}};
float scale[4] = {0.995697379738, 1.02370528816, 0.981540440823, 0.999971576622};
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

float conversionFactor = 0.16;

float rotB[4][3];
int s0 = 0;
int s1 = 1;
int s2 = 2;
int s3 = 3;
int led = 4;
int sensCnt = 4;

char data[16];
float fData[4][4];

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
  
  //Serial.println("Keeping the device still and level during startup will yeild the best results");
  Wire.beginOnPins(5,6);    //SCL on GPIO 5, SDA on GPIO 6
  Wire.begin();
  //TWBR = ((F_CPU / 400000) - 16) / 2;//set the I2C speed to 400KHz
  IMUinit();
  printTimer = millis();
  timer = micros();

  RFduinoBLE.deviceName = "magnetic";
  RFduinoBLE.advertisementData = "magField";
  RFduinoBLE.begin();

  //RFduinoBLE.sendInt(1);
}



void loop(){

  setChannel(0);    // sensor 0 is the "heading" sensor
  
  if (micros() - timer >= 5000){    // means after 5ms
    //this runs in 4ms on the MEGA 2560
    G_Dt = (micros() - timer)/1000000.0;    // conversion to seconds
    timer=micros();
    compass.read();
    floatMagX = ((float)compass.m.x - compassXMin) * inverseXRange - 1.0;
    floatMagY = ((float)compass.m.y - compassYMin) * inverseYRange - 1.0;
    floatMagZ = ((float)compass.m.z - compassZMin) * inverseZRange - 1.0;
    float tmpCX = (float)compass.a.x;
    float tmpCY = (float)compass.a.y;
    float tmpCZ = (float)compass.a.z;
    /*Smoothing(&compass.a.x,&smoothAccX);
    Smoothing(&compass.a.y,&smoothAccY);
    Smoothing(&compass.a.z,&smoothAccZ);*/
    Smoothing(&tmpCX,&smoothAccX);
    Smoothing(&tmpCY,&smoothAccY);
    Smoothing(&tmpCZ,&smoothAccZ);
    accToFilterX = smoothAccX;
    accToFilterY = smoothAccY;
    accToFilterZ = smoothAccZ;
    gyro.read();
    AHRSupdate(&G_Dt);
  }

    // get magnetic
    getMagnetCali();

    // rotate the initial magnetic field and subtract it!
    relQuat();

    /*for(int a=0; a<sensCnt; a++){    
    fData[a][0] = a;     
    fData[a][1] = magX[a]-rotB[a][0];
    fData[a][2] = magY[a]-rotB[a][1];
    fData[a][3] = magZ[a]-rotB[a][2];    
    }*/

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


float fastAtan2( float y, float x)
{
  static float atan;
  static float z;
  if ( x == 0.0f )
  {
    if ( y > 0.0f ) return PIBY2_FLOAT;
    if ( y == 0.0f ) return 0.0f;
    return -PIBY2_FLOAT;
  }
  z = y / x;
  if ( fabs( z ) < 1.0f )
  {
    atan = z/(1.0f + 0.28f*z*z);
    if ( x < 0.0f )
    {
      if ( y < 0.0f ) return atan - PI_FLOAT;
      return atan + PI_FLOAT;
    }
  }
  else
  {
    atan = PIBY2_FLOAT - z/(z*z + 0.28f);
    if ( y < 0.0f ) return atan - PI_FLOAT;
  }
  return atan;
}

float invSqrt(float number) {
  volatile long i;
  volatile float x, y;
  volatile const float f = 1.5F;

  x = number * 0.5F;
  y = number;
  i = * ( long * ) &y;
  i = 0x5f375a86 - ( i >> 1 );
  y = * ( float * ) &i;
  y = y * ( f - ( x * y * y ) );
  return y;
}

void Smoothing(float *raw, float *smooth){
  *smooth = (*raw * alpha) + (*smooth * (1-alpha));
  //*smooth = (*raw * (alpha)) - (*smooth * (1-alpha));   //perhaps a better solution...
}

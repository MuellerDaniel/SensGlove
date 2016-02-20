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

char data[12];

float magX, magY, magZ, rawX, rawY, rawZ;
float magX_I = 0.0;
float magY_I = 0.0;
float magZ_I = 0.0;
double hardBias[3] = {26.959991, -35.679992, -159.279998};
double softBias[3] = {0.979163, 1.018322, 1.003299};
float offFree[3] = {72.621156801701048, 7.2729417646131465, 80.228360877530477};
float smoothMagX = 0.0;
float smoothMagY = 0.0;
float smoothMagZ = 0.0;
float alphaMag = 0.15;

float conversionFactor = 0.16;

float rotB[3];

int quatPin = 8;
int quat_IPin = 9;

void setup(){
  Serial.begin(38400);
  Serial.println("Keeping the device still and level during startup will yeild the best results");
  Wire.beginOnPins(5,6);    //SCL on GPIO 5, SDA on GPIO 6
  //Wire.begin();
  //TWBR = ((F_CPU / 400000) - 16) / 2;//set the I2C speed to 400KHz
  IMUinit();
  printTimer = millis();
  timer = micros();

  /*pinMode(quatPin,OUTPUT);
  pinMode(quat_IPin,OUTPUT);*/

  /*RFduinoBLE.deviceName = "magnetic";
  RFduinoBLE.advertisementData = "magField";
  RFduinoBLE.begin();

  RFduinoBLE.sendInt(1);*/
}



void loop(){

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

    /*Serial.print("Euler:\t");
    Serial.print(roll); Serial.print("\t");
    Serial.print(pitch); Serial.print("\t");
    Serial.println(yaw);*/

    //Quaternion output
    //Serial.print("quat:\t");
    /*Serial.print(q0,4);
    Serial.print("\t");
    Serial.print(q1,4);
    Serial.print("\t");
    Serial.print(q2,4);
    Serial.print("\t");
    Serial.println(q3,4);*/

    /*Serial.print("inital quat:\t");
    Serial.print(q0_I,4);
    Serial.print("\t");
    Serial.print(q1_I,4);
    Serial.print("\t");
    Serial.print(q2_I,4);
    Serial.print("\t");
    Serial.println(q3_I,4);*/

    //print magnetic
    getMagnetCali();
    //Serial.println("--------------------------");
    //Serial.print("raw Mag:\t");
    Serial.print(0); Serial.print("\t");
    Serial.print(magX);
    Serial.print("\t");
    Serial.print(magY);
    Serial.print("\t");
    Serial.println(magZ);

    /*Serial.print("initial Mag:\t");
    Serial.print(magX_I);
    Serial.print("\t");
    Serial.print(magY_I);
    Serial.print("\t");
    Serial.println(magZ_I);*/

    relQuat();
    /*Serial.print("rot initial:\t");
    Serial.print(rotB[0]);
    Serial.print("\t");
    Serial.print(rotB[1]);
    Serial.print("\t");
    Serial.println(rotB[2]);*/

    //Serial.print("absolute mag:\t");
    Serial.print(1); Serial.print("\t");
    Serial.print(magX-rotB[0]);
    Serial.print("\t");
    Serial.print(magY-rotB[1]);
    Serial.print("\t");
    Serial.println(magZ-rotB[2]);

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

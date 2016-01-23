/*
Based on the Madgwick algorithm found at:
 See: http://www.x-io.co.uk/open-source-imu-and-ahrs-algorithms/

 This code inherits all relevant liscenses and may be freely modified and redistributed.
 The MinIMU v1 has a roughly +/- 10degree accuracy
 The MinIMU v2 has a roughly +/- 1 degree accuracy
 */
#include <Wire.h>
//#include <RFduinoBLE.h>
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
  //Wire.beginOnPins(5,6);    //SCL on GPIO 5, SDA on GPIO 6
  Wire.begin();
  //TWBR = ((F_CPU / 400000) - 16) / 2;//set the I2C speed to 400KHz
  IMUinit();
  printTimer = millis();
  timer = micros();

  pinMode(quatPin,OUTPUT);
  pinMode(quat_IPin,OUTPUT);

  /*RFduinoBLE.deviceName = "magnetic";
  RFduinoBLE.advertisementData = "magField";
  RFduinoBLE.begin();

  RFduinoBLE.sendInt(1);*/
}



void loop(){
  /*Serial.println("pitch,roll,yaw");
  Serial.println(pitch);
  Serial.println(roll);
  Serial.println(yaw);

  if(isnan(roll)) IMUinit();
  else if(isnan(pitch)) IMUinit();
  if(isnan(yaw)) IMUinit();*/

  if (micros() - timer >= 5000){
    //this runs in 4ms on the MEGA 2560
    G_Dt = (micros() - timer)/1000000.0;
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

void getMagnetCali(){
  getRawMagnet();
  /*magX = (rawX - hardBias[0]) * softBias[0];
  magY = (rawY - hardBias[1]) * softBias[1];
  magZ = (rawZ - hardBias[2]) * softBias[2];*/
  // off Freescale approach
  magX = rawX-offFree[0];
  magY = rawY-offFree[1];
  magZ = rawZ-offFree[2];
}

//in [mT]
void getRawMagnet(){
  while(compass.readReg(compass.STATUS_M) <= 0x0F);
  compass.readMag();

  smoothingMag(&compass.m.x, &smoothMagX);
  smoothingMag(&compass.m.y, &smoothMagY);
  smoothingMag(&compass.m.z, &smoothMagZ);

  rawX = smoothMagX * conversionFactor;
  rawY = smoothMagY * conversionFactor;
  rawZ = smoothMagZ * conversionFactor;

  /*rawX = compass.m.x * conversionFactor;
  rawY = compass.m.y * conversionFactor;
  rawZ = compass.m.z * conversionFactor;*/

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
  a = 1.0*a;
  b = -1.0*b;
  c = -1.0*c;
  d = -1.0*d;

  // TRY: rotate this quaternion pi/2 around z!
  /*float a_z = cos(PI_FLOAT/4);
  float b_z = 0;
  float c_z = 0;
  float d_z = sin(PI_FLOAT/4);  
  a = a*a_z - b*b_z - c*c_z - d*d_z;
  b = a*b_z + b*a_z + c*d_z - d*c_z;
  c = a*c_z - b*d_z + c*a_z + d*b_z;
  d = a*d_z + b*c_z - c*b_z + d*a_z;*/

   
  //Serial.print("dif quat:\t");
  /*Serial.print(a,4);
  Serial.print("\t");
  Serial.print(b,4);
  Serial.print("\t");
  Serial.print(c,4);
  Serial.print("\t");
  Serial.println(d,4);*/

  float rot11 = a*a+b*b-c*c-d*d;
  float rot12 = 2*(b*c+a*d);
  float rot13 = 2*(b*d-a*c);
  float rot21 = 2*(b*c-a*d);
  float rot22 = a*a-b*b+c*c-d*d;
  float rot23 = 2*(c*d+a*b);
  float rot31 = 2*(b*d+a*c);
  float rot32 = 2*(c*d-a*b);
  float rot33 = a*a-b*b-c*c+d*d;
  /*Serial.println("rotation matrix:");
  //Serial.println("q:");
  Serial.print("q\t");Serial.print(rot11);Serial.print("\t");Serial.print(rot12);Serial.print("\t");Serial.println(rot13);
  Serial.print("q\t");Serial.print(rot21);Serial.print("\t");Serial.print(rot22);Serial.print("\t");Serial.println(rot23);
  Serial.print("q\t");Serial.print(rot31);Serial.print("\t");Serial.print(rot32);Serial.print("\t");Serial.println(rot33);*/

  // verifying the assumption...
  /*float diffpitch = asin(2*(a*c-b*d));
  float diffyaw = fastAtan2((2*(b*c+a*d)),(a*a+b*b-c*c-d*d));
  float diffroll = fastAtan2((2*(c*d+a*b)),(a*a-b*b-c*c+d*d));
  Serial.println("QUAT roll, pitch, yaw");
  Serial.print(ToDeg(diffroll));Serial.print("\t");
  Serial.print(ToDeg(diffpitch));Serial.print("\t");
  Serial.println(ToDeg(diffyaw));

  float diffpitchR = -asin(rot13);
  float diffyawR = fastAtan2(rot12,rot11);
  float diffrollR = fastAtan2(rot23,rot33);
  Serial.println("ROTMAT roll, pitch, yaw");
  Serial.print(ToDeg(diffrollR));Serial.print("\t");
  Serial.print(ToDeg(diffpitchR));Serial.print("\t");
  Serial.println(ToDeg(diffyawR));*/
  //float rotB[3];
  rotB[0] = rot11*magX_I+rot12*magY_I+rot13*magZ_I;
  rotB[1] = rot21*magX_I+rot22*magY_I+rot23*magZ_I;
  rotB[2] = rot31*magX_I+rot32*magY_I+rot33*magZ_I;

}

void IMUinit(){

  float tmpMagX = 0.0;
  float tmpMagY = 0.0;
  float tmpMagZ = 0.0;
  //init devices
  compass.init();
  gyro.init();

  gyro.writeReg(gyro.CTRL_REG1, 0xCF);
  gyro.writeReg(gyro.CTRL_REG2, 0x00);
  gyro.writeReg(gyro.CTRL_REG3, 0x00);
  gyro.writeReg(gyro.CTRL_REG4, 0x20); //
  gyro.writeReg(gyro.CTRL_REG5, 0x02);

  // additional things...
  compass.enableDefault();
  compass.writeReg(compass.CTRL5, 0x74); // 100Hz
  compass.writeReg(compass.CTRL6, 0x20); // mag. scale +-4 gauss

  compass.writeAccReg(compass.CTRL_REG1_A, 0x77);//400hz all enabled
  compass.writeAccReg(compass.CTRL_REG4_A, 0x20);//+/-8g 4mg/LSB

  compass.writeMagReg(compass.CRA_REG_M, 0x1C);
  compass.writeMagReg(compass.CRB_REG_M, 0x60);
  compass.writeMagReg(compass.MR_REG_M, 0x00);

  beta = betaDef;
  //calculate initial quaternion
  //take an average of the gyro readings to remove the bias

  for (i = 0; i < 500;i++){
    gyro.read();
    compass.read();
    float tmpCX = (float)compass.a.x;
    float tmpCY = (float)compass.a.y;
    float tmpCZ = (float)compass.a.z;
    /*Smoothing(&compass.a.x,&smoothAccX);
    Smoothing(&compass.a.y,&smoothAccY);
    Smoothing(&compass.a.z,&smoothAccZ);*/
    Smoothing(&tmpCX,&smoothAccX);
    Smoothing(&tmpCY,&smoothAccY);
    Smoothing(&tmpCZ,&smoothAccZ);
    delay(3);
  }
  gyroSumX = 0;
  gyroSumY = 0;
  gyroSumZ = 0;

  for (i = 0; i < 500;i++){
    gyro.read();
    while(compass.readReg(compass.STATUS_M) <= 0x0F);
    compass.read();
    float tmpCX = (float)compass.a.x;
    float tmpCY = (float)compass.a.y;
    float tmpCZ = (float)compass.a.z;
    /*Smoothing(&compass.a.x,&smoothAccX);
    Smoothing(&compass.a.y,&smoothAccY);
    Smoothing(&compass.a.z,&smoothAccZ);*/
    Smoothing(&tmpCX,&smoothAccX);
    Smoothing(&tmpCY,&smoothAccY);
    Smoothing(&tmpCZ,&smoothAccZ);
    gyroSumX += (gyro.g.x);
    gyroSumY += (gyro.g.y);
    gyroSumZ += (gyro.g.z);

    getRawMagnet();
    tmpMagX += rawX;
    tmpMagY += rawY;
    tmpMagZ += rawZ;

    delay(3);
  }
  offSetX = gyroSumX / 500.0;
  offSetY = gyroSumY / 500.0;
  offSetZ = gyroSumZ / 500.0;

  /*magX_I = ((tmpMagX / 500.0) - hardBias[0]) * softBias[0];
  magY_I = ((tmpMagY / 500.0) - hardBias[1]) * softBias[1];
  magZ_I = ((tmpMagZ / 500.0) - hardBias[2]) * softBias[2];*/
  magX_I = (tmpMagX/500.0) - offFree[0];
  magY_I = (tmpMagY/500.0) - offFree[1];
  magZ_I = (tmpMagZ/500.0) - offFree[2];
  /*magX_I = tmpMagX/500.0;
  magY_I = tmpMagY/500.0;
  magZ_I = tmpMagZ/500.0;*/
  while(compass.readReg(compass.STATUS_M) <= 0x0F);
  compass.read();

  //calculate the initial quaternion
  //these are rough values. This calibration works a lot better if the device is kept as flat as possible
  //find the initial pitch and roll
  float tmpAX = compass.a.x;
  float tmpAY = compass.a.y;
  float tmpAZ = compass.a.z;
  pitch = ToDeg(fastAtan2(tmpAX,sqrt(tmpAY * tmpAY + tmpAZ * tmpAZ)));
  roll = ToDeg(fastAtan2(-1*tmpAY,sqrt(tmpAX * tmpAX + tmpAZ * tmpAZ)));

  if (tmpAZ > 0){
    if (tmpAX > 0){
      pitch = 180.0 - pitch;
    }
    else{
      pitch = -180.0 - pitch;
    }
    if (tmpAY > 0){
      roll = -180.0 - roll;
    }
    else{
      roll = 180.0 - roll;
    }
  }

  floatMagX = (compass.m.x - compassXMin) * inverseXRange - 1.0;
  floatMagY = (compass.m.y - compassYMin) * inverseYRange - 1.0;
  floatMagZ = (compass.m.z - compassZMin) * inverseZRange - 1.0;
  //tilt compensate the compass
  float xMag = (floatMagX * cos(ToRad(pitch))) + (floatMagZ * sin(ToRad(pitch)));
  float yMag = -1 * ((floatMagX * sin(ToRad(roll))  * sin(ToRad(pitch))) + (floatMagY * cos(ToRad(roll))) - (floatMagZ * sin(ToRad(roll)) * cos(ToRad(pitch))));

  yaw = ToDeg(fastAtan2(yMag,xMag));

  if (yaw < 0){
    yaw += 360;
  }
  //if(isnan(roll) || isnan(yaw) || isnan(pitch)) digitalWrite(quatPin,HIGH);
  Serial.println("pitch, roll, yaw");
  Serial.println(pitch);
  Serial.println(roll);
  Serial.println(yaw);
  Serial.println("xMag, yMag");
  Serial.println(xMag);
  Serial.println(yMag);

  //calculate the rotation matrix
  float cosPitch = cos(ToRad(pitch));
  float sinPitch = sin(ToRad(pitch));

  float cosRoll = cos(ToRad(roll));
  float sinRoll = sin(ToRad(roll));

  float cosYaw = cos(ToRad(yaw));
  float sinYaw = sin(ToRad(yaw));

  //need the transpose of the rotation matrix
  float r11 = cosPitch * cosYaw;
  float r21 = cosPitch * sinYaw;
  float r31 = -1.0 * sinPitch;

  float r12 = -1.0 * (cosRoll * sinYaw) + (sinRoll * sinPitch * cosYaw);
  float r22 = (cosRoll * cosYaw) + (sinRoll * sinPitch * sinYaw);
  float r32 = sinRoll * cosPitch;

  float r13 = (sinRoll * sinYaw) + (cosRoll * sinPitch * cosYaw);
  float r23 = -1.0 * (sinRoll * cosYaw) + (cosRoll * sinPitch * sinYaw);
  float r33 = cosRoll * cosPitch;

  //convert to quaternion
  //be aware, that you can get 0 for your denominator! -> check all posibilities
  if(!isnan(sqrt(1 + r11 + r22 + r33))){
    q0 = 0.5 * sqrt(1 + r11 + r22 + r33);
    q1 = (r32 - r23)/(4 * q0);
    q2 = (r13 - r31)/(4 * q0);
    q3 = (r21 - r12)/(4 * q0);
  }/*else if(!isnan(sqrt(1 + r11 - r22 - r33))){
    q1 = 0.5 * sqrt(1 + r11 - r22 - r33);
    q0 = (r23 - r32)/(4 * q1);
    q2 = (r12 + r21)/(4 * q1);
    q3 = (r31 + r13)/(4 * q1);
  }else if(!isnan(sqrt(1 - r11 + r22 - r33))){
    q2 = 0.5 * sqrt(1 - r11 + r22 - r33);
    q0 = (r31 - r13)/(4 * q2);
    q1 = (r12 - r21)/(4 * q2);
    q3 = (r23 + r32)/(4 * q2);
  }else if(!isnan(sqrt(1 - r11 - r22 + r33))){
    q3 = 0.5 * sqrt(1 - r11 - r22 + r33);
    q0 = (r12 - r21)/(4 * q3);
    q1 = (r13 + r31)/(4 * q3);
    q2 = (r23 + r32)/(4 * q3);
  }*/

  //TRY: apply the rotation around z also here...
  /*float a_z = cos(PI_FLOAT/4);
  float b_z = 0;
  float c_z = 0;
  float d_z = sin(PI_FLOAT/4);  
  q0_I = q0*a_z - q1*b_z - q2*c_z - q3*d_z;
  q1_I = -1.0*(q0*b_z + q1*a_z + q2*d_z - q3*c_z);
  q2_I = -1.0*(q0*c_z - q1*d_z + q2*a_z + q3*b_z);
  q3_I = -1.0*(q0*d_z + q1*c_z - q2*b_z + q3*a_z);*/

  // negating the quaternion, you only need it in the form of q^-1
  q0_I = q0;
  q1_I = 1.0*q1;
  q2_I = 1.0*q2;
  q3_I = 1.0*q3;
}

void IMUupdate(float *dt) {
  static float gx;
  static float gy;
  static float gz;
  static float ax;
  static float ay;
  static float az;

  static float recipNorm;
  static float s0, s1, s2, s3;
  static float qDot1, qDot2, qDot3, qDot4;
  static float _2q0, _2q1, _2q2, _2q3, _4q0, _4q1, _4q2 ,_8q1, _8q2, q0q0, q1q1, q2q2, q3q3;

  gx = ToRad((gyro.g.x - offSetX) * GYRO_SCALE);
  gy = ToRad((gyro.g.y - offSetY) * GYRO_SCALE);
  gz = ToRad((gyro.g.z - offSetZ) * GYRO_SCALE);

  ax = -1.0 * compass.a.x;
  ay = -1.0 * compass.a.y;
  az = -1.0 * compass.a.z;
  // Rate of change of quaternion from gyroscope
  qDot1 = 0.5f * (-q1 * gx - q2 * gy - q3 * gz);
  qDot2 = 0.5f * (q0 * gx + q2 * gz - q3 * gy);
  qDot3 = 0.5f * (q0 * gy - q1 * gz + q3 * gx);
  qDot4 = 0.5f * (q0 * gz + q1 * gy - q2 * gx);

  magnitude = sqrt(ax * ax + ay * ay + az * az);
  if ((magnitude > 384) || (magnitude < 128)){
    ax = 0;
    ay = 0;
    az = 0;
  }

  // Compute feedback only if accelerometer measurement valid (avoids NaN in accelerometer normalisation)
  if(!((ax == 0.0f) && (ay == 0.0f) && (az == 0.0f))) {

    // Normalise accelerometer measurement
    recipNorm = invSqrt(ax * ax + ay * ay + az * az);
    ax *= recipNorm;
    ay *= recipNorm;
    az *= recipNorm;

    // Auxiliary variables to avoid repeated arithmetic
    _2q0 = 2.0f * q0;
    _2q1 = 2.0f * q1;
    _2q2 = 2.0f * q2;
    _2q3 = 2.0f * q3;
    _4q0 = 4.0f * q0;
    _4q1 = 4.0f * q1;
    _4q2 = 4.0f * q2;
    _8q1 = 8.0f * q1;
    _8q2 = 8.0f * q2;
    q0q0 = q0 * q0;
    q1q1 = q1 * q1;
    q2q2 = q2 * q2;
    q3q3 = q3 * q3;

    // Gradient decent algorithm corrective step
    s0 = _4q0 * q2q2 + _2q2 * ax + _4q0 * q1q1 - _2q1 * ay;
    s1 = _4q1 * q3q3 - _2q3 * ax + 4.0f * q0q0 * q1 - _2q0 * ay - _4q1 + _8q1 * q1q1 + _8q1 * q2q2 + _4q1 * az;
    s2 = 4.0f * q0q0 * q2 + _2q0 * ax + _4q2 * q3q3 - _2q3 * ay - _4q2 + _8q2 * q1q1 + _8q2 * q2q2 + _4q2 * az;
    s3 = 4.0f * q1q1 * q3 - _2q1 * ax + 4.0f * q2q2 * q3 - _2q2 * ay;
    recipNorm = invSqrt(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3); // normalise step magnitude
    s0 *= recipNorm;
    s1 *= recipNorm;
    s2 *= recipNorm;
    s3 *= recipNorm;

    // Apply feedback step
    qDot1 -= beta * s0;
    qDot2 -= beta * s1;
    qDot3 -= beta * s2;
    qDot4 -= beta * s3;
  }

  // Integrate rate of change of quaternion to yield quaternion
  q0 += qDot1 * *dt;
  q1 += qDot2 * *dt;
  q2 += qDot3 * *dt;
  q3 += qDot4 * *dt;

  // Normalise quaternion
  recipNorm = invSqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3);
  q0 *= recipNorm;
  q1 *= recipNorm;
  q2 *= recipNorm;
  q3 *= recipNorm;
}

void AHRSupdate(float *dt) {
  static float gx;
  static float gy;
  static float gz;
  static float ax;
  static float ay;
  static float az;
  static float mx;
  static float my;
  static float mz;


  static float recipNorm;
  static float s0, s1, s2, s3;
  static float qDot1, qDot2, qDot3, qDot4;
  static float hx, hy;
  static float _2q0mx, _2q0my, _2q0mz, _2q1mx, _2bx, _2bz, _4bx, _4bz, _2q0, _2q1, _2q2, _2q3, _2q0q2, _2q2q3, q0q0, q0q1, q0q2, q0q3, q1q1, q1q2, q1q3, q2q2, q2q3, q3q3;

  gx = ToRad((gyro.g.x - offSetX) * GYRO_SCALE);
  gy = ToRad((gyro.g.y - offSetY) * GYRO_SCALE);
  gz = ToRad((gyro.g.z - offSetZ) * GYRO_SCALE);

  ax = -1.0 * compass.a.x;
  ay = -1.0 * compass.a.y;
  az = -1.0 * compass.a.z;

  mx = floatMagX;
  my = floatMagY;
  mz = floatMagZ;
  // Rate of change of quaternion from gyroscope
  qDot1 = 0.5f * (-q1 * gx - q2 * gy - q3 * gz);
  qDot2 = 0.5f * (q0 * gx + q2 * gz - q3 * gy);
  qDot3 = 0.5f * (q0 * gy - q1 * gz + q3 * gx);
  qDot4 = 0.5f * (q0 * gz + q1 * gy - q2 * gx);

  magnitude = sqrt(ax * ax + ay * ay + az * az);

  if ((magnitude > 384) || (magnitude < 128)){
    ax = 0;
    ay = 0;
    az = 0;
  }

  // Compute feedback only if accelerometer measurement valid (avoids NaN in accelerometer normalisation)
  if(!((ax == 0.0f) && (ay == 0.0f) && (az == 0.0f))) {


    // Normalise accelerometer measurement
    recipNorm = invSqrt(ax * ax + ay * ay + az * az);
    ax *= recipNorm;
    ay *= recipNorm;
    az *= recipNorm;
    // Normalise magnetometer measurement
    recipNorm = invSqrt(mx * mx + my * my + mz * mz);
    mx *= recipNorm;
    my *= recipNorm;
    mz *= recipNorm;
    // Auxiliary variables to avoid repeated arithmetic
    _2q0mx = 2.0f * q0 * mx;
    _2q0my = 2.0f * q0 * my;
    _2q0mz = 2.0f * q0 * mz;
    _2q1mx = 2.0f * q1 * mx;
    _2q0 = 2.0f * q0;
    _2q1 = 2.0f * q1;
    _2q2 = 2.0f * q2;
    _2q3 = 2.0f * q3;
    _2q0q2 = 2.0f * q0 * q2;
    _2q2q3 = 2.0f * q2 * q3;
    q0q0 = q0 * q0;
    q0q1 = q0 * q1;
    q0q2 = q0 * q2;
    q0q3 = q0 * q3;
    q1q1 = q1 * q1;
    q1q2 = q1 * q2;
    q1q3 = q1 * q3;
    q2q2 = q2 * q2;
    q2q3 = q2 * q3;
    q3q3 = q3 * q3;



    // Reference direction of Earth's magnetic field
    hx = mx * q0q0 - _2q0my * q3 + _2q0mz * q2 + mx * q1q1 + _2q1 * my * q2 + _2q1 * mz * q3 - mx * q2q2 - mx * q3q3;
    hy = _2q0mx * q3 + my * q0q0 - _2q0mz * q1 + _2q1mx * q2 - my * q1q1 + my * q2q2 + _2q2 * mz * q3 - my * q3q3;
    _2bx = sqrt(hx * hx + hy * hy);
    _2bz = -_2q0mx * q2 + _2q0my * q1 + mz * q0q0 + _2q1mx * q3 - mz * q1q1 + _2q2 * my * q3 - mz * q2q2 + mz * q3q3;
    _4bx = 2.0f * _2bx;
    _4bz = 2.0f * _2bz;

    // Gradient decent algorithm corrective step
    s0 = -_2q2 * (2.0f * q1q3 - _2q0q2 - ax) + _2q1 * (2.0f * q0q1 + _2q2q3 - ay) - _2bz * q2 * (_2bx * (0.5f - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (-_2bx * q3 + _2bz * q1) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + _2bx * q2 * (_2bx * (q0q2 + q1q3) + _2bz * (0.5f - q1q1 - q2q2) - mz);
    s1 = _2q3 * (2.0f * q1q3 - _2q0q2 - ax) + _2q0 * (2.0f * q0q1 + _2q2q3 - ay) - 4.0f * q1 * (1 - 2.0f * q1q1 - 2.0f * q2q2 - az) + _2bz * q3 * (_2bx * (0.5f - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (_2bx * q2 + _2bz * q0) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + (_2bx * q3 - _4bz * q1) * (_2bx * (q0q2 + q1q3) + _2bz * (0.5f - q1q1 - q2q2) - mz);
    s2 = -_2q0 * (2.0f * q1q3 - _2q0q2 - ax) + _2q3 * (2.0f * q0q1 + _2q2q3 - ay) - 4.0f * q2 * (1 - 2.0f * q1q1 - 2.0f * q2q2 - az) + (-_4bx * q2 - _2bz * q0) * (_2bx * (0.5f - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (_2bx * q1 + _2bz * q3) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + (_2bx * q0 - _4bz * q2) * (_2bx * (q0q2 + q1q3) + _2bz * (0.5f - q1q1 - q2q2) - mz);
    s3 = _2q1 * (2.0f * q1q3 - _2q0q2 - ax) + _2q2 * (2.0f * q0q1 + _2q2q3 - ay) + (-_4bx * q3 + _2bz * q1) * (_2bx * (0.5f - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (-_2bx * q0 + _2bz * q2) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + _2bx * q1 * (_2bx * (q0q2 + q1q3) + _2bz * (0.5f - q1q1 - q2q2) - mz);
    recipNorm = invSqrt(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3); // normalise step magnitude
    s0 *= recipNorm;
    s1 *= recipNorm;
    s2 *= recipNorm;
    s3 *= recipNorm;

    // Apply feedback step
    qDot1 -= beta * s0;
    qDot2 -= beta * s1;
    qDot3 -= beta * s2;
    qDot4 -= beta * s3;
  }

  // Integrate rate of change of quaternion to yield quaternion
  q0 += qDot1 * *dt;
  q1 += qDot2 * *dt;
  q2 += qDot3 * *dt;
  q3 += qDot4 * *dt;

  // Normalise quaternion
  recipNorm = invSqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3);
  q0 *= recipNorm;
  q1 *= recipNorm;
  q2 *= recipNorm;
  q3 *= recipNorm;
}

void GetEuler(void){
  // conversion to Euler sequence (1,2,3)
  roll = ToDeg(fastAtan2(2 * (q0 * q1 + q2 * q3),1 - 2 * (q1 * q1 + q2 * q2)));
  pitch = ToDeg(asin(2 * (q0 * q2 - q3 * q1)));
  yaw = ToDeg(fastAtan2(2 * (q0 * q3 + q1 * q2) , 1 - 2* (q2 * q2 + q3 * q3)));
  if (yaw < 0){
    yaw +=360;
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

void smoothingMag(int *raw, float *smooth){
  //*smooth = (*raw * alphaMag) - (*smooth * (1-alphaMag));
  *smooth = *smooth + alphaMag*(*raw-*smooth);
}

void Smoothing(float *raw, float *smooth){
  *smooth = (*raw * alpha) + (*smooth * (1-alpha));
  //*smooth = (*raw * (alpha)) - (*smooth * (1-alpha));   //perhaps a better solution...
}

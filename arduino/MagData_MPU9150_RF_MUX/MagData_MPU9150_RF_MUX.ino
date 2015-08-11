//Displaying the raw magnetometer data
#include "Wire.h"
#include <RFduinoBLE.h>
#include <stdio.h>

#include "I2Cdev.h"
#include "MPU6050.h"

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 accelgyro;
I2Cdev   I2C_M;

int16_t ax, ay, az;
int16_t gx, gy, gz;
int16_t mx, my, mz;
int16_t rawMX, rawMY, rawMZ;
float magX, magY, magZ, rawX, rawY, rawZ;
// 150701
//float hardBias[3] = {8.55, 4.50, -52.65};
//float softBias[3] = {0.98, 0.99, 1.02};
//150707
//float hardBias[3] = {-4.80, 0.15, -48.30};
//float softBias[3] = {0.95, 1.04, 1.01};
//150714
//float hardBias[3] = {-2.40, -15.75, -40.35};
//float softBias[3] = {0.87, 1.26, 0.95};
//150730 desk adverse to Philipp
//float hardBias[3] = {40.50, -7.80, -22.95};
//float softBias[3] = {0.96, 0.98,  1.06};
//150811
float hardBias[2][3] = {{-13.50, 1.65, -20.85},
                        {-0.15, 0.60,  -53.10}};
float softBias[2][3] = {{0.97, 0.96,  1.07},
                        {1.03, 0.97,  1.00}};




uint8_t buffer[14];
boolean passStat = true;
unsigned long startTime, endTime;
const int sampleNr = 1000;
unsigned long delta[sampleNr];

//datasheet p.13: resolution of 0.3 uT/LSB
float conversionFactor = 0.3;
char data[16];
//char data[12];
float one, two, three;
float fData[4];
//float fData[3];
int cnt;
int chNr = 0;
int s0 = 0;
int s1 = 1;
int s2 = 2;
int s3 = 3;
int devCnt = 2;    //total nr of sensors

void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    Wire.beginOnPins(5,6);  //SCL on GPIO 5, SDA on GPIO 6
    //TWBR = 12;    //set I2C communication to 400 kHz

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
    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
    // it's really up to you depending on your project)
    //Serial.begin(9600);

    //setChannel(0);
    //Serial.println("Initializing I2C device nr ");
    //accelgyro.initialize();
    //Serial.println("Testing device connections...");
    //Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
    
    for(int i=0; i<devCnt; i++){
    setChannel(i);
    delay(50);
    // initialize device
    //Serial.print("Initializing I2C device nr "); Serial.println(i);
    accelgyro.initialize();
    // verify connection
    //Serial.println("Testing device connections...");
    //Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
    }
    

    RFduinoBLE.deviceName = "magnetic";
    RFduinoBLE.advertisementData = "magField";
    RFduinoBLE.begin();
}

void loop() {   
  
   for(int i=0; i<devCnt; i++){
      setChannel(i);
      getMagnetCali(i);
      
      fData[0] = i;
      fData[1] = magX;
      fData[2] = magY;
      fData[3] = magZ;

      for(int i=0; i<4; i++){
        memcpy(&data[i*sizeof(float)], &fData[i], sizeof(float));
      }
      RFduinoBLE.send(data, 16);
   }
  
   
//   setChannel(chNr);
//  
//   getMagnetCali();
//   
//   //calibrated values via serial interface
//   /*Serial.print(magX); Serial.print("\t");
//   Serial.print(magY); Serial.print("\t");
//   Serial.println(magZ);*/
//   fData[0] = chNr;
//   fData[1] = magX;
//   fData[2] = magY;
//   fData[3] = magZ;
//
////   fData[0] = magX;
////   fData[1] = magY;
////   fData[2] = magZ;
//  
//   for(int i=0; i<4; i++){
////   for(int i=0; i<3; i++){
//    memcpy(&data[i*sizeof(float)], &fData[i], sizeof(float));
//   }
//   
//   RFduinoBLE.send(data, 16);
//   //RFduinoBLE.send(data, 12);
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
      // read raw accel/gyro measurements from device
    accelgyro.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);

    rawX = mx * conversionFactor;
    rawY = my * conversionFactor;
    rawZ = mz * conversionFactor;

}

void readRawMagnet(){
//  I2C_M.readBytes
  I2C_M.readBytes(MPU9150_RA_MAG_ADDRESS, MPU9150_RA_MAG_XOUT_L, 6, buffer);
    rawMX = (((int16_t)buffer[1]) << 8) | buffer[0];
    rawMY = (((int16_t)buffer[3]) << 8) | buffer[2];
    rawMZ = (((int16_t)buffer[5]) << 8) | buffer[4];
}

/*float getMean(unsigned long arr[]){
  unsigned long sum=0;
  for(int i=0; i<sizeof(arr); i++){
    sum += arr[i];
  }
 return (sum/sizeof(arr));
}

unsigned long getMax(unsigned long arr[]){
 unsigned long start=0;
 for(int i=0; i<sizeof(arr); i++){
    start=max(start,arr[i]);
 }
 return start;
}

unsigned long getMin(unsigned long arr[]){
 unsigned long start=100;
 for(int i=0; i<sizeof(arr); i++){
    start=min(start,arr[i]);
 }
 return start;
}*/

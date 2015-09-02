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
//150813 desk adverse to Philipp
//float hardBias[3] = {-6.90, -1.35, -40.05};   //lying flat
//float softBias[3] = {0.96, 1.01, 1.03};       //lying flat
//float hardBias[3] = {-6.15, 8.25,  -37.05};     //attached to hand
//float softBias[3] = {0.98, 0.99,  1.03};       //attached to hand
float hardBias[3] = {0,0,0};
float softBias[3] = {1,1,1};

uint8_t buffer[14];
boolean passStat = true;
unsigned long startTime, endTime;
const int sampleNr = 1000;
unsigned long delta[sampleNr];

//datasheet p.13: resolution of 0.3 uT/LSB
float conversionFactor = 0.3;
char data[16];
float one, two, three;
float fData[4];
int cnt;

void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    Wire.beginOnPins(5,6);  //SCL on GPIO 5, SDA on GPIO 6
    //TWBR = 12;    //set I2C communication to 400 kHz

    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
    // it's really up to you depending on your project)
    Serial.begin(9600);

    // initialize device
    //Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    // verify connection
    //Serial.println("Testing device connections...");
    //Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

    RFduinoBLE.deviceName = "magnetic";
    RFduinoBLE.advertisementData = "magField";
    RFduinoBLE.begin();
}

void loop() {
   getMagnetCali();
      
   //calibrated values via serial interface
   Serial.print("Mag\t");
   Serial.print(magX); Serial.print("\t");
   Serial.print(magY); Serial.print("\t");
   Serial.println(magZ);

   fData[0] = 0.0; 
   fData[1] = magX;
   fData[2] = magY;
   fData[3] = magZ;

   for(int i=0; i<4; i++){
    memcpy(&data[i*sizeof(float)], &fData[i], sizeof(float));
   }
  
   RFduinoBLE.send(data, 16);
   delay(100);
}

float getMean(unsigned long arr[]){
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
}

void getMagnetCali(){
 getRawMagnet();
 
 magX = (rawX - hardBias[0]) * softBias[0];
 magY = (rawY - hardBias[1]) * softBias[1];
 magZ = (rawZ - hardBias[2]) * softBias[2];
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

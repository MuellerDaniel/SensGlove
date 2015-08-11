//sketch for getting the hard and soft iron values for the sensor
#include "Wire.h"
#include <RFduinoBLE.h>
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
float magX, magY, magZ, rawX, rawY, rawZ;
float minData[3] = {10000, 10000, 10000};
float maxData[3] = {-10000, -10000, -10000};
float hardBias[3];
float softBias[3];

//datasheet p.13: resolution of 0.3 uT/LSB
float conversionFactor = 0.3;
int sampleNum = 1000;



void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
   Wire.beginOnPins(5,6);  //SCL on GPIO 5, SDA on GPIO 6

    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
    // it's really up to you depending on your project)
    Serial.begin(9600);

    // initialize device
    Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
    
    calibrateCompass();
}

void loop() {
   getMagnetCali();  
   
   //output is in uT
   //Serial.print("Cmag:\t");
   //Serial.print(magX); Serial.print("\t");
   //Serial.print(magY); Serial.print("\t");
   //Serial.println(magZ); 
}

void getMagnetCali(){
 getRawMagnet();
 
 magX = (rawX - hardBias[0]) * softBias[0];
 magY = (rawY - hardBias[1]) * softBias[1];
 magZ = (rawZ - hardBias[2]) * softBias[2];  
}

//in [uT]
void getRawMagnet(){
      // read raw accel/gyro measurements from device
    accelgyro.getMotion9(&ax, &ay, &az, &gx, &gy, &gz, &mx, &my, &mz);
    
    rawX = mx * conversionFactor;
    rawY = my * conversionFactor;
    rawZ = mz * conversionFactor; 

   /*Serial.print("Rmag:\t");
   Serial.print(rawX); Serial.print("\t");
   Serial.print(rawY); Serial.print("\t");
   Serial.println(rawZ);*/
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
  Serial.println("Waiting for user to type 'ready'. Then wave your magnetometer around to collect data");  
  while(!Serial.find("ready")){
    Serial.println("Waiting for user to type 'ready'. Then wave your magnetometer around to collect data");
    delay(1000);
  }
  getMinMaxData();
  calcHardBias();
  calcSoftBias();
}


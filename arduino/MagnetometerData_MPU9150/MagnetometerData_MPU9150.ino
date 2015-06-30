//Displaying the raw magnetometer data
#include "Wire.h"

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
float hardBias[3] = {10.5, 9.6, -51.9};
float softBias[3] = {0.97, 0.99, 1.04};

//datasheet p.13: resolution of 0.3 uT/LSB
float conversionFactor = 0.3;

void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    Wire.begin();

    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
    // it's really up to you depending on your project)
    Serial.begin(38400);

    // initialize device
    Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
    
}

void loop() {
   getMagnetCali();  
   
   //output is in uT
   //Serial.print("Cmag:\t");
   Serial.print(magX); Serial.print("\t");
   Serial.print(magY); Serial.print("\t");
   Serial.println(magZ); 
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




/*
 * COLLECTING AND SENDING THE CALIBRATED MAGNETOMETER DATA VIA BLUETOOTH
 * 
 * code for ONE sensor
 * for obtaining hard and soft iron values, run the "LSMCalibradetMag_RF.ino" script
 * 
 */
#include <Wire.h>
#include <LSM303.h>
#include <RFduinoBLE.h>

LSM303 compass;
float magX, magY, magZ, rawX, rawY, rawZ;
//float hardBias[3] = {0, 0, 0};
//float softBias[3] = {1, 1, 1};
//float hardBias[3] = {228.96, -50.77,  183.70};
//float softBias[3] = {1.03, 0.98,  0.99};
//float hardBias[3] = {134.84, -34.25,  306.56};
//float softBias[3] = {1.08, 0.97,  0.96};
float hardBias[3] = {97.96, 23.23, 260.82};
float softBias[3] = {1.01, 0.99, 1.01};

float conversionFactorMag = 0.479;   //for range +-12gauss
float conversionFactorAcc = 0.061;  //for range +-2g
uint8_t buffer[14];
char data[16];
float fData[4];

void setup()
{
  Serial.begin(9600);
  Wire.beginOnPins(5,6);    //SCL on GPIO 5, SDA on GPIO 6
  compass.init();
  compass.enableDefault();
  compass.writeReg(compass.CTRL6, 0x60);    //set magnetic range to +-12gauss

  RFduinoBLE.deviceName = "magnetic";
  RFduinoBLE.advertisementData = "magField";
  RFduinoBLE.begin();

}

void loop()
{  
   getMagnetCali();
      
   //calibrated values via serial interface
   Serial.print("Mag\t");
   Serial.print(magX); Serial.print("\t");
   Serial.print(magY); Serial.print("\t");
   Serial.println(magZ);

  // accelerometer data
   compass.readAcc();
   
   /*Serial.print("Acc\t");
   Serial.print(compass.a.x*conversionFactorAcc); Serial.print("\t");
   Serial.print(compass.a.y*conversionFactorAcc); Serial.print("\t");
   Serial.println(compass.a.z*conversionFactorAcc);*/

   fData[0] = 0.0; 
   fData[1] = magX;
   fData[2] = magY;
   fData[3] = magZ;

   for(int i=0; i<4; i++){
    memcpy(&data[i*sizeof(float)], &fData[i], sizeof(float));
   }
   unsigned long sec;
   sec = millis();
   RFduinoBLE.send(data, 16);
   Serial.println(millis()-sec);
   //delay(100);
}

void getMagnetCali(){
 getRawMagnet();
 
 magX = (rawX - hardBias[0]) * softBias[0];
 magY = (rawY - hardBias[1]) * softBias[1];
 magZ = (rawZ - hardBias[2]) * softBias[2];
  
}

//in [mT]
void getRawMagnet(){
   
  compass.readMag();

  rawX = compass.m.x * conversionFactorMag;
  rawY = compass.m.y * conversionFactorMag;
  rawZ = compass.m.z * conversionFactorMag;
}






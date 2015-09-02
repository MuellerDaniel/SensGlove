/*
The sensor outputs provided by the library are the raw 16-bit values
obtained by concatenating the 8-bit high and low accelerometer and
magnetometer data registers. They can be converted to units of g and
gauss using the conversion factors specified in the datasheet for your
particular device and full scale setting (gain).

Example: An LSM303D gives a magnetometer X axis reading of 1982 with
its default full scale setting of +/- 4 gauss. The M_GN specification
in the LSM303D datasheet (page 10) states a conversion factor of 0.160
mgauss/LSB (least significant bit) at this FS setting, so the raw
reading of -1982 corresponds to 1982 * 0.160 = 317.1 mgauss =
0.3171 gauss.

In the LSM303DLHC, LSM303DLM, and LSM303DLH, the acceleration data
registers actually contain a left-aligned 12-bit number, so the lowest
4 bits are always 0, and the values should be shifted right by 4 bits
(divided by 16) to be consistent with the conversion factors specified
in the datasheets.

Example: An LSM303DLH gives an accelerometer Z axis reading of -16144
with its default full scale setting of +/- 2 g. Dropping the lowest 4
bits gives a 12-bit raw value of -1009. The LA_So specification in the
LSM303DLH datasheet (page 11) states a conversion factor of 1 mg/digit
at this FS setting, so the value of -1009 corresponds to -1009 * 1 =
1009 mg = 1.009 g.
*/

#include <Wire.h>
#include <LSM303.h>
#include <RFduinoBLE.h>

LSM303 compass;
float magX, magY, magZ, rawX, rawY, rawZ;
//float hardBias[3] = {228.96, -50.77,  183.70};
//float softBias[3] = {1.03, 0.98,  0.99};
float hardBias[3] = {134.84, -34.25,  306.56};
float softBias[3] = {1.08, 0.97,  0.96};
//float hardBias[3] = {34.97, -8.86, 249.56};
//float softBias[3] = {1.20, 0.94,  0.90};

float conversionFactor = 0.479;   //for range +-12gauss
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

   fData[0] = 0.0; 
   fData[1] = magX;
   fData[2] = magY;
   fData[3] = magZ;

   for(int i=0; i<4; i++){
    memcpy(&data[i*sizeof(float)], &fData[i], sizeof(float));
   }
  
   RFduinoBLE.send(data, 16);
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

  rawX = compass.m.x * conversionFactor;
  rawY = compass.m.y * conversionFactor;
  rawZ = compass.m.z * conversionFactor;
}






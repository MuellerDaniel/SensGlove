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

LSM303 compass;
float magX, magY, magZ, rawX, rawY, rawZ;
float minData[3] = {10000, 10000, 10000};
float maxData[3] = {-10000, -10000, -10000};
float hardBias[3];
float softBias[3];
//datasheet p.10: resolution of 0.16 mgauss/LSB
float conversionFactor = 0.16;
int sampleNum = 1000;

void setup()
{
  Wire.begin();
  Serial.begin(9600);
  
  compass.init();
  compass.enableDefault();
  
  calibrateCompass();
}

void loop()
{  
  getMagnetCali();
  //getRawMagnet();
  //compass.readMag();
  //output is in [mgauss]
  Serial.print("mag\t");
  Serial.print(magX);
  Serial.print("\t");
  Serial.print(magY);
  Serial.print("\t");
  Serial.println(magZ); 
 
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
  //Serial.println(maxData[0]);
 }  
}

void calcHardBias(){
 hardBias[0] = (maxData[0] + minData[0])/2; 
 hardBias[1] = (maxData[1] + minData[1])/2;
 hardBias[2] = (maxData[2] + minData[2])/2;  
}

void calcSoftBias(){
  float tempX = (maxData[0] + abs(minData[0]))/2;
  float tempY = (maxData[1] + abs(minData[1]))/2;
  float tempZ = (maxData[2] + abs(minData[2]))/2;
  
  float rad = (tempX + tempY + tempZ) / 3;
  
  softBias[0] = rad/tempX;
  softBias[1] = rad/tempY;
  softBias[2] = rad/tempZ;
}

void calibrateCompass(){
  Serial.println("Waiting for user to type 'ready'. Then wave your magnetometer around to collect data");
  while(!Serial.find("ready"));
  getMinMaxData();
  calcHardBias();
  calcSoftBias();
}




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
double hardBias[3];
double softBias[3];
float alpha = 0.15;
float smoothMagX = 0.0;
float smoothMagY = 0.0;
float smoothMagZ = 0.0;

//datasheet p.10: resolution of 0.16 mgauss/LSB
#define conversionFactor .16
int sampleNum = 1000;
int maxChange = 500;
int noChange = 0;


void setup()
{  
  Serial.begin(9600);
  Wire.begin();

  pinMode(13,OUTPUT);
  
  compass.init();
  compass.enableDefault();
  compass.enableDefault();
  compass.writeReg(compass.CTRL5, 0x74);    // put magnetic data rate to 100 Hz
  //compass.writeReg(compass.CTRL6, 0x00);    // put magnetic scale to +-2 gauss
  compass.writeReg(compass.CTRL6, 0x20);    // put magnetic scale to +-4 gauss
  //compass.writeReg(compass.CTRL6, 0x40);    // put magnetic scale to +-8 gauss
  //compass.writeReg(compass.CTRL6, 0x60);    // put magnetic scale to +-12 gauss

  digitalWrite(13, HIGH);
  calibrateCompass();
}

void loop()
{  
  getMagnetCali();
  //getRawMagnet();
  //compass.readMag();
  //output is in [mgauss]
  /*Serial.print("mag\t");
  Serial.print(magX);
  Serial.print("\t");
  Serial.print(magY);
  Serial.print("\t");
  Serial.println(magZ); */
  Serial.print("hardBias: {"); Serial.print(hardBias[0],6);
  Serial.print(", "); Serial.print(hardBias[1],6);
  Serial.print(", "); Serial.print(hardBias[2],6); Serial.println("}");
  Serial.print("softBias: {"); Serial.print(softBias[0],6);
  Serial.print(", "); Serial.print(softBias[1],6);
  Serial.print(", "); Serial.print(softBias[2],6); Serial.println("}");

  Serial.print("minValues:["); Serial.print(minData[0],6);
  Serial.print(", "); Serial.print(minData[1],6);
  Serial.print(", "); Serial.print(minData[2],6); Serial.println("]");
  Serial.print("maxValues:["); Serial.print(maxData[0],6);
  Serial.print(", "); Serial.print(maxData[1],6);
  Serial.print(", "); Serial.print(maxData[2],6); Serial.println("]");
}

void getMagnetCali(){
 getRawMagnet(); 
 magX = (rawX - hardBias[0]) * softBias[0];
 magY = (rawY - hardBias[1]) * softBias[1];
 magZ = (rawZ - hardBias[2]) * softBias[2];   
}

//in [mT]
void getRawMagnet(){
  while(compass.readReg(compass.STATUS_M) <= 0x0F);
  compass.readMag();

  smoothing(&compass.m.x, &smoothMagX);
  smoothing(&compass.m.y, &smoothMagY);
  smoothing(&compass.m.z, &smoothMagZ);
  rawX = smoothMagX * conversionFactor;
  rawY = smoothMagY * conversionFactor;
  rawZ = smoothMagZ * conversionFactor;
  
  /*rawX = compass.m.x * conversionFactor;  
  rawY = compass.m.y * conversionFactor;  
  rawZ = compass.m.z * conversionFactor;*/

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

void collectMinMax(int cnt){
  while(noChange < maxChange){
    getRawMagnet();
    if((minData[0] > rawX) || (minData[1] > rawY) || (minData[2] > rawZ) || 
       (maxData[0] < rawX) || (maxData[1] < rawY) || (maxData[2] < rawZ))
       //if(minData[0] > rawX)
       {
          noChange = 0;
          
          minData[0] = min(minData[0], rawX);
          minData[1] = min(minData[1], rawY);
          minData[2] = min(minData[2], rawZ);
          //finding the maximum
          maxData[0] = max(maxData[0], rawX);
          maxData[1] = max(maxData[1], rawY);
          maxData[2] = max(maxData[2], rawZ);  
          
          /*Serial.print("MinX: ");
          Serial.print(minData[0]);
          Serial.print("MaxX: ");
          Serial.println(maxData[0]);
          Serial.print("MinY: ");
          Serial.print(minData[1]);
          Serial.print("MaxY: ");
          Serial.println(maxData[1]);
          Serial.print("MinZ: ");
          Serial.print(minData[2]);
          Serial.print("MaxZ: ");
          Serial.println(maxData[2]);*/
       }       
      else{
        noChange += 1;
        Serial.print("Nochange: "); Serial.println(noChange);
        //digitalWrite(13,LOW);
     }
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
  //Serial.println("Waiting for user to type 'ready'. Then wave your magnetometer around to collect data");
  //while(!Serial.find("ready"));
  //getMinMaxData();
  collectMinMax(maxChange);
  calcHardBias();
  calcSoftBias();
}

void smoothing(int *raw, float *smooth){  
  *smooth = *smooth + alpha*(*raw-*smooth);
}



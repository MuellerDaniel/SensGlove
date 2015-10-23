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
float hardBias[4][3] = {{36.64,  -3.11, 199.26},
                        {48.86, 27.30, 321.65},
                        {17.48, -38.56,  234.71},
                        {-30.42, 54.37, -179.39}};
float softBias[4][3] = {{0.99, 1.02, 1.00},
                         {0.97,  0.98,  1.05},
                         {1.06,  0.94,  1.01},
                         {1.00,  0.99,  1.01}};

float conversionFactorMag = 0.479;   //for range +-12gauss
float conversionFactorAcc = 0.061;  //for range +-2g
char data[16];
float fData[4];
int sensCnt = 0;

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

    //prepare and send them via BT
    fData[0] = 0; 
    fData[1] = magX;
    fData[2] = magY;
    fData[3] = magZ;
        
    for(int j=0; j<4; j++){
    memcpy(&data[j*sizeof(float)], &fData[j], sizeof(float));
    }
    //unsigned long sec;
    //sec = millis();
    RFduinoBLE.send(data, 16);
    
    /*Serial.print("Mag\t");
    Serial.print(magX); Serial.print("\t");
    Serial.print(magY); Serial.print("\t");
    Serial.println(magZ);*/
    
    
   //Serial.println(millis()-sec);
   //delay(100);
}

void getMagnetCali(float *hardMag, float *softMag){
 getRawMagnet();
 
 magX = (rawX - hardMag[0]) * softMag[0];
 magY = (rawY - hardMag[1]) * softMag[1];
 magZ = (rawZ - hardMag[2]) * softMag[2];
  
}

//in [mT]
void getRawMagnet(){
   
  compass.readMag();
  //Serial.println("Read magnet...");
  rawX = compass.m.x * conversionFactorMag;
  rawY = compass.m.y * conversionFactorMag;
  rawZ = compass.m.z * conversionFactorMag;
}






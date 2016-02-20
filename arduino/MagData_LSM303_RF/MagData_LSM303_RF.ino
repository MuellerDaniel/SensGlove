/*
 * COLLECTING AND SENDING THE CALIBRATED MAGNETOMETER DATA VIA BLUETOOTH
 * 
 * code for ONE sensor
 * for obtaining hard and soft iron values, run the "LSMCalibradetMag_RF.ino" script
 * 
 */
#include <Wire.h>
#include <LSM303.h>
//#include <RFduinoBLE.h>

LSM303 compass;
float magX, magY, magZ, rawX, rawY, rawZ;
//float off[3] = {-57.2928643216, -231.811859296, -506.202211055};
float off[3] = {0.0,0.0,0.0};
float hardBias[3] = {20.62589379, -25.19287093, -74.15009193};
float softBias[3] = {0.99091757,  1.00286099,  1.00635296};
float offFree[3] = {72.621156801701048, 7.2729417646131465, 80.228360877530477};
//float offFree[3] = {0.0,  0.0 , 0.0};
//float hardBias[3] = {0.0,0.0,0.0};
//float softBias[3] = {1.0,1.0,1.0};
/*float hardBias[4][3] = {{36.64,  -3.11, 199.26},
                        {48.86, 27.30, 321.65},
                        {17.48, -38.56,  234.71},
                        {-30.42, 54.37, -179.39}};
float softBias[4][3] = {{0.99, 1.02, 1.00},
                         {0.97,  0.98,  1.05},
                         {1.06,  0.94,  1.01},
                         {1.00,  0.99,  1.01}};*/

//float conversionFactorMag = 0.479;   //for range +-12gauss
float conversionFactor = 0.16;   //for range +-4gauss
//float conversionFactorAcc = 0.061;  //for range +-2g
char data[16];
float fData[4];
int sensCnt = 0;

float smoothMagX = 0.0;
float smoothMagY = 0.0;
float smoothMagZ = 0.0;
float alphaMag = 0.15;
//float alphaMag = 1.0;
float p[3] = {1.0,1.0,1.0};
float k[3] = {0.0,0.0,0.0};
float r[3] = {6.32,7.12,17.12};

void setup()
{
  Serial.begin(115200);
  //Wire.beginOnPins(5,6);    //SCL on GPIO 5, SDA on GPIO 6
  Wire.begin();
  compass.init();
  compass.enableDefault();
  compass.writeReg(compass.CTRL5, 0x74);    // put magnetic data rate to 100 Hz
  //compass.writeReg(compass.CTRL6, 0x00);    // put magnetic scale to +-2 gauss
  compass.writeReg(compass.CTRL6, 0x20);    // put magnetic scale to +-4 gauss
  //compass.writeReg(compass.CTRL6, 0x40);    // put magnetic scale to +-8 gauss
  //compass.writeReg(compass.CTRL6, 0x60);    // put magnetic scale to +-12 gauss

  /*RFduinoBLE.deviceName = "magnetic";
  RFduinoBLE.advertisementData = "magField";
  RFduinoBLE.begin();*/
}

void loop()
{    
    //curr_t = millis();
    getMagnetCali();
    
    //prepare and send them via BT
    /*fData[0] = 0; 
    fData[1] = magX;
    fData[2] = magY;
    fData[3] = magZ;*/
        
    /*for(int j=0; j<4; j++){
    memcpy(&data[j*sizeof(float)], &fData[j], sizeof(float));
    }
    //unsigned long sec;
    //sec = millis();
    RFduinoBLE.send(data, 16);*/
    
    //Serial.print("Mag\t");
    //Serial.println(millis()-curr_t);
    //Serial.print(0);Serial.print("\t");
    Serial.print(magX); Serial.print("\t");
    Serial.print(magY); Serial.print("\t");
    Serial.println(magZ);
    
    
   //Serial.println(millis()-sec);
   //delay(100);
}

void getMagnetCali(){
 getRawMagnet();

 // hard - soft bias approach
 /*magX = (rawX - hardBias[0]) * softBias[0] - off[0];
 magY = (rawY - hardBias[1]) * softBias[1] - off[1];
 magZ = (rawZ - hardBias[2]) * softBias[2] - off[2];*/
 /*magX = (rawX - hardMag[0]) * softMag[0];
 magY = (rawY - hardMag[1]) * softMag[1];
 magZ = (rawZ - hardMag[2]) * softMag[2];*/

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
  //smoothKF(&compass.m.x,&compass.m.y,&compass.m.z,&smoothMagX,&smoothMagY,&smoothMagZ);

  rawX = smoothMagX * conversionFactor;
  rawY = smoothMagY * conversionFactor;
  rawZ = smoothMagZ * conversionFactor;
  
  /*rawX = compass.m.x * conversionFactorMag;
  rawY = compass.m.y * conversionFactorMag;
  rawZ = compass.m.z * conversionFactorMag;*/
}

void smoothingMag(int *raw, float *smooth){
  //*smooth = (*raw * alphaMag) - (*smooth * (1-alphaMag));
  *smooth = *smooth + alphaMag*(*raw-*smooth);
  //*smooth = *raw;
}

void smoothKF(int *rawX, int *rawY, int *rawZ, float *smoothX,float *smoothY,float *smoothZ){
  // simple kalman filter
  k[0] = p[0]/(p[0]+r[0]);
  *smoothX = *smoothX + k[0]*(*rawX-*smoothX);
  p[0] = (1-k[0])*p[0];
  k[1] = p[1]/(p[1]+r[1]);
  *smoothY = *smoothY + k[1]*(*rawY-*smoothY);
  p[1] = (1-k[1])*p[1];
  k[2] = p[2]/(p[2]+r[2]);
  *smoothZ = *smoothZ + k[2]*(*rawZ-*smoothZ);
  p[2] = (1-k[2])*p[2];
}






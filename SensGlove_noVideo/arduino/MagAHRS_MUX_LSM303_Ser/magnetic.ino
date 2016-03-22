

//in [mT]
void getRawMagnet(int channel, bool smooth){
  //setChannel(channel);
  while(compass.readReg(compass.STATUS_M) <= 0x0F);
  compass.readMag();

  if(smooth){
    smoothingMag(&compass.m.x, &smoothMagX[channel]);
    smoothingMag(&compass.m.y, &smoothMagY[channel]);
    smoothingMag(&compass.m.z, &smoothMagZ[channel]);
  
    rawX[channel] = smoothMagX[channel] * conversionFactor;
    rawY[channel] = smoothMagY[channel] * conversionFactor;
    rawZ[channel] = smoothMagZ[channel] * conversionFactor;
  } else {    
    rawX[channel] = compass.m.x * conversionFactor;
    rawY[channel] = compass.m.y * conversionFactor;
    rawZ[channel] = compass.m.z * conversionFactor;
  }
}

// updates all 4 sensor readings
void getMagnetCali(){   
  for(int i=0; i<sensCnt; i++){
    setChannel(i);
    getRawMagnet(i,true);
    // off Freescale approach
    magX[i] = (rawX[i]-offFree[i][0])*scale[i];
    magY[i] = (rawY[i]-offFree[i][1])*scale[i];
    magZ[i] = (rawZ[i]-offFree[i][2])*scale[i];
  }
}

void smoothingMag(short int *raw, float *smooth){
  //*smooth = (*raw * alphaMag) - (*smooth * (1-alphaMag));
  *smooth = *smooth + alphaMag*(*raw-*smooth);
}


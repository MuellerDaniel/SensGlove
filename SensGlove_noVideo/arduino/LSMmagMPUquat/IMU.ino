

void InitEarthMag(){
  digitalWrite(led,HIGH);

  initLSM();

  getEarthOff(50);

  initMPU();

  getQuat();
  q0_I = q.w;
  q1_I = 1.0*q.x;
  q2_I = 1.0*q.y;
  q3_I = 1.0*q.z;
  
  digitalWrite(led,LOW);
}



void getEarthOff(int collect){

  float tmpMagX[4] = {0.0, 0.0, 0.0, 0.0};
  float tmpMagY[4] = {0.0, 0.0, 0.0, 0.0};
  float tmpMagZ[4] = {0.0, 0.0, 0.0, 0.0};

  //int collect = 5;
  for(int i=0; i<collect; i++){    
    for(int j=0; j<sensCnt; j++){
      setChannel(j);
      getRawMagnet(j,false);
      tmpMagX[j] += rawX[j];
      tmpMagY[j] += rawY[j];
      tmpMagZ[j] += rawZ[j];          
    }
  }
    
  for(int i=0; i<sensCnt; i++){
    mag_I[i][0] = ((tmpMagX[i]/collect) - offFree[i][0])*scale[i];
    mag_I[i][1] = ((tmpMagY[i]/collect) - offFree[i][1])*scale[i];
    mag_I[i][2] = ((tmpMagZ[i]/collect) - offFree[i][2])*scale[i];
  }  
}


void initLSM(){
  // Initialization of LSM
  // additional things...
  for(int i=0; i<sensCnt; i++){
    setChannel(i);
    //delay(50);
    compass.init();

    compass.enableDefault();
    compass.writeReg(compass.CTRL5, 0x74);  //100Hz
    compass.writeReg(compass.CTRL6, 0x20);  //scale +-4

  }
}


void initMPU(){
  setChannel(chMPU);
  delay(50);
  
  //initialization of MPU
  mpu.initialize();
  devStatus = mpu.dmpInitialize();

  if (devStatus == 0) {
        // turn on the DMP, now that it's ready
        //Serial.println(F("Enabling DMP..."));
        mpu.setDMPEnabled(true);

        // set our DMP Ready flag so the main loop() function knows it's okay to use it
        //Serial.println(F("DMP ready! Waiting for first interrupt..."));
        dmpReady = true;

        // get expected DMP packet size for later comparison
        packetSize = mpu.dmpGetFIFOPacketSize();
        
    }
}


void getQuat(){
  
  setChannel(chMPU);
  
  if (!dmpReady) return;   

  // reset interrupt flag and get INT_STATUS byte
  mpuInterrupt = false;
  mpuIntStatus = mpu.getIntStatus();

  // get current FIFO count
  fifoCount = mpu.getFIFOCount();

  while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();

      // read a packet from FIFO
  mpu.getFIFOBytes(fifoBuffer, packetSize);

  // display quaternion values in easy matrix form: w x y z
  mpu.dmpGetQuaternion(&q, fifoBuffer);  
  
}


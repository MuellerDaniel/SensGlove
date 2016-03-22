
void IMUinit(){
  digitalWrite(led,HIGH);

  float tmpMagX[4] = {0.0, 0.0, 0.0, 0.0};
  float tmpMagY[4] = {0.0, 0.0, 0.0, 0.0};
  float tmpMagZ[4] = {0.0, 0.0, 0.0, 0.0};
  //init devices
  setChannel(0);    // sensor 0 is the "heading reference" sensor
  
  compass.init();
  gyro.init();

  gyro.writeReg(gyro.CTRL_REG1, 0xCF);
  gyro.writeReg(gyro.CTRL_REG2, 0x00);
  gyro.writeReg(gyro.CTRL_REG3, 0x00);
  gyro.writeReg(gyro.CTRL_REG4, 0x20); //
  gyro.writeReg(gyro.CTRL_REG5, 0x02);

  compass.writeAccReg(compass.CTRL_REG1_A, 0x77);//400hz all enabled
  compass.writeAccReg(compass.CTRL_REG4_A, 0x20);//+/-8g 

  // additional things...
  for(int i=0; i<4; i++){
    setChannel(i);
    compass.enableDefault();
    compass.writeReg(compass.CTRL5, 0x74); // 100Hz
    compass.writeReg(compass.CTRL6, 0x20); // mag. scale +-4 gauss    // perhaps this after writeAccReg action ???  
  
    compass.writeMagReg(compass.CRA_REG_M, 0x1C);     // leave it out???
    compass.writeMagReg(compass.CRB_REG_M, 0x60);
    compass.writeMagReg(compass.MR_REG_M, 0x00);
  }

  beta = betaDef;
  //calculate initial quaternion
  //take an average of the gyro readings to remove the bias

  setChannel(0);    
  
  for (i = 0; i < 500;i++){
    gyro.read();
    compass.read();
    float tmpCX = (float)compass.a.x;
    float tmpCY = (float)compass.a.y;
    float tmpCZ = (float)compass.a.z;
    /*Smoothing(&compass.a.x,&smoothAccX);
    Smoothing(&compass.a.y,&smoothAccY);
    Smoothing(&compass.a.z,&smoothAccZ);*/
    Smoothing(&tmpCX,&smoothAccX);
    Smoothing(&tmpCY,&smoothAccY);
    Smoothing(&tmpCZ,&smoothAccZ);
    delay(3);
  }
  gyroSumX = 0;
  gyroSumY = 0;
  gyroSumZ = 0;

  for (i = 0; i < 500;i++){
    gyro.read();
    while(compass.readReg(compass.STATUS_M) <= 0x0F);
    compass.read();
    float tmpCX = (float)compass.a.x;
    float tmpCY = (float)compass.a.y;
    float tmpCZ = (float)compass.a.z;
    /*Smoothing(&compass.a.x,&smoothAccX);
    Smoothing(&compass.a.y,&smoothAccY);
    Smoothing(&compass.a.z,&smoothAccZ);*/
    Smoothing(&tmpCX,&smoothAccX);
    Smoothing(&tmpCY,&smoothAccY);
    Smoothing(&tmpCZ,&smoothAccZ);
    gyroSumX += (gyro.g.x);
    gyroSumY += (gyro.g.y);
    gyroSumZ += (gyro.g.z);

    delay(3);
  }
  offSetX = gyroSumX / 500.0;
  offSetY = gyroSumY / 500.0;
  offSetZ = gyroSumZ / 500.0;

  

  // measure sorounding magnetic field to determine the initial offset
  int collect = 50;
  for(int i=0; i<collect; i++){
    //digitalWrite(led,LOW);
    for(int j=0; j<sensCnt; j++){
      setChannel(j);
      getRawMagnet(j,false);
      tmpMagX[j] += rawX[j];
      tmpMagY[j] += rawY[j];
      tmpMagZ[j] += rawZ[j];          
    }
    //digitalWrite(led,HIGH);
  }  
  for(int i=0; i<sensCnt; i++){
    mag_I[i][0] = ((tmpMagX[i]/collect) - offFree[i][0])*scale[i];
    mag_I[i][1] = ((tmpMagY[i]/collect) - offFree[i][1])*scale[i];
    mag_I[i][2] = ((tmpMagZ[i]/collect) - offFree[i][2])*scale[i];
  }
  
  setChannel(0);
  
  while(compass.readReg(compass.STATUS_M) <= 0x0F);
  compass.read();

  //calculate the initial quaternion
  //these are rough values. This calibration works a lot better if the device is kept as flat as possible
  //find the initial pitch and roll
  float tmpAX = compass.a.x;
  float tmpAY = compass.a.y;
  float tmpAZ = compass.a.z;
  pitch = ToDeg(fastAtan2(tmpAX,sqrt(tmpAY * tmpAY + tmpAZ * tmpAZ)));
  roll = ToDeg(fastAtan2(-1*tmpAY,sqrt(tmpAX * tmpAX + tmpAZ * tmpAZ)));

  if (tmpAZ > 0){
    if (tmpAX > 0){
      pitch = 180.0 - pitch;
    }
    else{
      pitch = -180.0 - pitch;
    }
    if (tmpAY > 0){
      roll = -180.0 - roll;
    }
    else{
      roll = 180.0 - roll;
    }
  }

  floatMagX = (compass.m.x - compassXMin) * inverseXRange - 1.0;
  floatMagY = (compass.m.y - compassYMin) * inverseYRange - 1.0;
  floatMagZ = (compass.m.z - compassZMin) * inverseZRange - 1.0;
  //tilt compensate the compass
  float xMag = (floatMagX * cos(ToRad(pitch))) + (floatMagZ * sin(ToRad(pitch)));
  float yMag = -1 * ((floatMagX * sin(ToRad(roll))  * sin(ToRad(pitch))) + (floatMagY * cos(ToRad(roll))) - (floatMagZ * sin(ToRad(roll)) * cos(ToRad(pitch))));

  yaw = ToDeg(fastAtan2(yMag,xMag));

  if (yaw < 0){
    yaw += 360;
  }

  //calculate the rotation matrix
  float cosPitch = cos(ToRad(pitch));
  float sinPitch = sin(ToRad(pitch));

  float cosRoll = cos(ToRad(roll));
  float sinRoll = sin(ToRad(roll));

  float cosYaw = cos(ToRad(yaw));
  float sinYaw = sin(ToRad(yaw));

  //need the transpose of the rotation matrix
  /*float r11 = cosPitch * cosYaw;
  float r21 = cosPitch * sinYaw;
  float r31 = -1.0 * sinPitch;

  float r12 = -1.0 * (cosRoll * sinYaw) + (sinRoll * sinPitch * cosYaw);
  float r22 = (cosRoll * cosYaw) + (sinRoll * sinPitch * sinYaw);
  float r32 = sinRoll * cosPitch;

  float r13 = (sinRoll * sinYaw) + (cosRoll * sinPitch * cosYaw);
  float r23 = -1.0 * (sinRoll * cosYaw) + (cosRoll * sinPitch * sinYaw);
  float r33 = cosRoll * cosPitch;*/

  float r11 = cosPitch * cosYaw;
  float r12 = cosPitch * sinYaw;
  float r13 = -1.0 * sinPitch;

  float r21 = -1.0 * (cosRoll * sinYaw) + (sinRoll * sinPitch * cosYaw);
  float r22 = (cosRoll * cosYaw) + (sinRoll * sinPitch * sinYaw);
  float r23 = sinRoll * cosPitch;

  float r31 = (sinRoll * sinYaw) + (cosRoll * sinPitch * cosYaw);
  float r32 = -1.0 * (sinRoll * cosYaw) + (cosRoll * sinPitch * sinYaw);
  float r33 = cosRoll * cosPitch;

  //convert to quaternion
  //be aware, that you can get 0 for your denominator! -> check all posibilities
  if(!isnan(sqrt(1 + r11 + r22 + r33))){
    q0 = 0.5 * sqrt(1 + r11 + r22 + r33);
    q1 = (r23 - r32)/(4 * q0);
    q2 = (r31 - r13)/(4 * q0);
    q3 = (r12 - r21)/(4 * q0);
  }


  // negating the quaternion, you only need it in the form of q^-1
  q0_I = q0;
  q1_I = 1.0*q1;
  q2_I = 1.0*q2;
  q3_I = 1.0*q3;

  digitalWrite(led,LOW);
}

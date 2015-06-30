import processing.serial.*;

import peasy.test.*;
import peasy.org.apache.commons.math.*;
import peasy.*;
import peasy.org.apache.commons.math.geometry.*;

Serial mserialPort;
PeasyCam pcam;
ArrayList<PVector> magPoints;
String[] list;
String serialMsg = "";
int maxPoints = 500;

void setup () {
  size(900, 900, P3D);
  mserialPort = new Serial(this, Serial.list()[0], 115200);
  mserialPort.bufferUntil(10);
  
 // f = createFont("Arial", 8, true);

  pcam = new PeasyCam(this,500);
  pcam.lookAt(0,0,0,500);
  
  magPoints = new ArrayList<PVector>();
 // calMagPoints = new ArrayList<PVector>();
}


void serialEvent(Serial serialPort){
  try{    
    serialMsg = serialPort.readString();
    //System.out.println("SerialEvent: " + serialMsg);      
    serialMsg = serialMsg.trim();
    list = split(serialMsg, '\t');
    if (list.length >= 3){         
      float x = Float.parseFloat(list[1]);   
      float y = Float.parseFloat(list[2]);
      float z = Float.parseFloat(list[3]);
      PVector tmpPVector = new PVector(x, y, z);
      magPoints.add(tmpPVector);     
      System.out.println("added a point! " + magPoints.size());
      if(magPoints.size() == maxPoints){

      }
  }//else System.out.println("Too less arguments! " + list.length);
  
  } catch(RuntimeException e){
     System.out.println("Bad...");
  } 
  
}

void draw(){
  boolean calibrated = false;  
  PVector hardBias = new PVector(0,0,0);
  PVector softBias = new PVector(0,0,0);
  PVector softBiasA = new PVector(0,0,0);
  background(20);
  
  
   //drawing the raw data
   for(int i = 0; i < magPoints.size(); i++){
     PVector tmpV = magPoints.get(i);
     point(tmpV.x, tmpV.y, tmpV.z);
     stroke(255,0,0);
     strokeWeight(2);
    }
    
  //  if(magPoints.size() == maxPoints){
  //    mserialPort.stop();
      //drawCoordinates(500);
  //  }
  drawCoordinates(500);
}

void drawCoordinates(int len)
{
  strokeWeight(1);
  stroke(255,0,0);
  line(0,0,0,len,0,0);
  text("x",len,0,0);
  stroke(0,255,0);
  line(0,0,0,0,-len,0);
  text("z", 0, -len,0);
  stroke(0,0,255);
  line(0,0,0,0,0,len);
  text("y", 0,0,len);
}

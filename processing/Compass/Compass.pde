import processing.serial.*;

import peasy.test.*;
import peasy.org.apache.commons.math.*;
import peasy.*;
import peasy.org.apache.commons.math.geometry.*;


Serial mserialPort;
PFont f;
PeasyCam pcam;
String[] list;
String serialMsg = "";
PVector magPoint;

float magX, magY, magZ;


void setup () {
  size(500, 500, P3D);
  mserialPort = new Serial(this, Serial.list()[0], 115200);
  mserialPort.bufferUntil(10);
  
  f = createFont("Arial", 8, true);

  pcam = new PeasyCam(this,300);
  pcam.lookAt(0,0,0,300);
  magPoint = new PVector(0.0, 0.0, 0.0);
}

void serialEvent(Serial serialPort){
  try{    
    serialMsg = serialPort.readString();
    //System.out.println("SerialEvent: " + serialMsg);      
    serialMsg = serialMsg.trim();
    list = split(serialMsg, '\t');
    if (list.length >= 3){
     magX = Float.parseFloat(list[1]);
     magY = Float.parseFloat(list[2]);
     magZ = Float.parseFloat(list[3]);
  }//else System.out.println("Too less arguments! " + list.length);
  
  } catch(RuntimeException e){
     System.out.println("Bad...");
  } 
  
}

void draw(){
  background(20);
  textFont(f);
  fill(255);
  
  magPoint.x = magX;
  magPoint.y = -magZ;
  magPoint.z = magY;

  float len = magPoint.mag();
  text(len, -100,-100,0);  
  
  
  //normalizing the vector
  magPoint.normalize();
  magPoint.mult(50);

 // translate(width/2, height/2);
  line(0,0,0,magPoint.x, magPoint.y, magPoint.z);
  stroke(255,255,0);
  strokeWeight(2);
  
  pushMatrix();
  translate(magPoint.x, magPoint.y, magPoint.z);
  sphere(5);  
  stroke(255,0,255);
  popMatrix();
    
  drawCoordinates(100);
}

void drawCoordinates(int len)
{
  strokeWeight(1);
  stroke(255,0,0);
  line(0,0,0,-len,0,0);
  text("x",-len,0,0);
  stroke(0,255,0);
  line(0,0,0,0,len,0);
  text("z", 0, len,0);
  stroke(0,0,255);
  line(0,0,0,0,0,-len);
  text("y", 0,0,-len);
}



import processing.serial.*;

//import jpcap.*;
//import jpcap.packet.*;

import processing.opengl.*;

import peasy.test.*;
import peasy.org.apache.commons.math.*;
import peasy.*;
import peasy.org.apache.commons.math.geometry.*;

import shapes3d.utils.*;
import shapes3d.animation.*;
import shapes3d.*;

Box box;
Rot nullrot=new Rot(1,0,0,0,false),
        rot=new Rot(1,0,0,0,false);
PeasyCam pCamera;
PMatrix3D baseMat;

Serial rx;

void setup()
{
  size(500, 500, P3D);
  
  rx = new Serial(this, Serial.list()[0], 38400);
//  rx = new Serial(this, "COM14", 38400);
  rx.bufferUntil('\n'); 

  box = new Box(this);
  box.setSize(50,100,20);
  baseMat = g.getMatrix(baseMat);
  
  pCamera = new PeasyCam(this, 300);
  pCamera.rotateX(PI/2);
  pCamera.lookAt(0, 0, 0, 280);
}

void keyPressed() {
  //System.out.println("key Pressed!");
}

void serialEvent(Serial p)
{
  String msg = "";
  float ts,q0,q1,q2,q3;
 
 if (p==null)
   return;
 
  msg = p.readString(); 
    
  System.out.println(msg);
  
  String[] list;
  msg = msg.trim();
  list = split(msg, '\t');
  
  if (list.length >= 4)
  {
    //ts=Float.parseFloat(list[0]);
    q0=Float.parseFloat(list[0+1]);
    q1=Float.parseFloat(list[1+1]);
    q2=Float.parseFloat(list[2+1]);
    q3=Float.parseFloat(list[3+1]);
    //System.out.println(list[0]);
    /*q0=Float.parseFloat(list[0]);
    q1=Float.parseFloat(list[1]);
    q2=Float.parseFloat(list[2]);
    q3=Float.parseFloat(list[3]);*/
    rot=new Rot(q0,q1,q2,q3,true);
    rot=rot.applyInverseTo(nullrot); // calculate inverse
   // System.out.println(list[list.length-1]);
  }
}

void draw()
{
  background(20);
  
 
  
//  // stage lighting
  pushMatrix();
  g.setMatrix(baseMat);
  directionalLight(200, 200, 200, 100, 150, -100);
  ambientLight(160, 160, 160);
  popMatrix();
  
  /* to align the axes of the jNode to the processing world 
   * coordinates, we have to:
   *  (a) mirror the z-axis
   *  (b) use the inverse rotation (which is calculated in clientEvent) */
  scale(1,1,1); // mirror on z-axis
  
  /* apply the rotation */
  rotateX(rot.getAngles(RotOrder.XYZ)[0]);
  rotateY(rot.getAngles(RotOrder.XYZ)[1]);
  rotateZ(rot.getAngles(RotOrder.XYZ)[2]);
  
  drawCoordinates(1);
  box.draw();
}

void drawCoordinates(int x)
{
  strokeWeight(x);
  stroke(255,0,0);
  line(0,0,0,400,0,0);
  stroke(0,255,0);
  line(0,0,0,0,400,0);
  stroke(0,0,255);
  line(0,0,0,0,0,400);
}

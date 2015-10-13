import jpcap.*;
import jpcap.packet.*;

import processing.serial.*;

import processing.opengl.*;

import peasy.test.*;
import peasy.org.apache.commons.math.*;
import peasy.*;
import peasy.org.apache.commons.math.geometry.*;

import shapes3d.utils.*;
import shapes3d.animation.*;
import shapes3d.*;

import java.util.*;

PMatrix3D baseMat;
PeasyCam pcam;
BezTube tubes[];
PVector cpts[];
Rot nullrot=new Rot(1,0,0,0,false),
        rot=new Rot(1,0,0,0,false);
        
BufferedReader reader;
//String line;
float angles[];





LinkedHashMap<Integer,Rot> map = new LinkedHashMap<Integer,Rot>();

static final float RADIUS=5, HALFR=30;  // RADIUS for beztube, HALFR distance between joints
static int i=0;
boolean serialUp = false;
static int id = 5 ;	//variable for indicating the IMU (IDs range from 0 to 15)
PFont f;

//Rot nullrot=new Rot(1,0,0,0,false);

void setup()
{
  //size(1920,1080,P3D);
  size(500,500,P3D);

  f = createFont("Arial", 8, true);
  textFont(f);
  fill(255);
  
  reader = createReader("myPath5");
  //rx = new Serial(this, Serial.list()[0], 38400);
  //System.out.println(Serial.list());

  //rx.bufferUntil('\n');

 // initSerial();

  //baseMat=g.getMatrix(baseMat);

  pcam = new PeasyCam(this,300);  
  pcam.lookAt(60,0,0);
  pcam.rotateZ(-PI/2);
  pcam.rotateX(PI);
  
  cpts = makeCtrlPts();  
}


void draw()
{

  background(20);
  textFont(f);
  fill(255);  
  scale(1,1,1);
  // stage lighting
  pushMatrix();
  directionalLight(200, 200, 200, 100, 100, 100);
  ambientLight(160, 160, 160);
  popMatrix();
  
  String line;
  
  /*try{
    line = reader.readLine();
  }catch (IOException e) {
    e.printStackTrace();
    line = null;
  }
  if (line == null) {
    // Stop reading because of an error or file is empty
    System.out.println("END!!!");
    noLoop();  
  } else {
    System.out.println(line);
    //and now apply the angles to your points...
    extractAngles(line);
    //updateCtrlPts();
  }*/

  //"make" the tubes
  updateTubes(cpts);

  for (BezTube tube : tubes ){
	tube.draw();		//draw them!
}
  // points
  drawPoints(cpts);
  // draw lines between the points/dots
  drawLines(cpts);
  drawCoordinates(300);

}

void extractAngles(String line){
  String[] list;  
  list = split(line,' ');
  System.out.println(list.length);
  angles = new float[list.length];
  for(int i = 0; i<list.length; i++){
     angles[i] = Float.parseFloat(list[i]);
     System.out.println(angles[i]);
  }
}

void updateCtrlPts(){
  // apply the angles 
  
  
}


float getAngle(PVector startP, PVector angleP, PVector endP){
  PVector dir1 = PVector.sub(angleP,startP);
  PVector dir2 = PVector.sub(endP,angleP);
  return acos((abs(dir1.dot(dir2)))/(dir1.mag() * dir2.mag()));
}

/*void updateCtrlPts(LinkedHashMap<Integer,Rot> rotation){
//int n = 0;
  int thumbOffX = -40;
  int indexOffX = -30;
  int middleOffX = -10;
  int ringOffX = 10;
  int littleOffX = 30;

  PVector finger[][] ={
      { new PVector(thumbOffX,20,0),  //thumb
      new PVector(0,-20,0),
      new PVector(0,-20,0),
      new PVector(0,-20,0)},
      {new PVector(indexOffX,0,0),  //index
      new PVector(0,-HALFR,0),
      new PVector(0,-HALFR,0),
      new PVector(0,-HALFR,0)},
      {new PVector(middleOffX,0,0),  //middle
      new PVector(0,-HALFR,0),
      new PVector(0,-HALFR,0),
      new PVector(0,-HALFR,0)},
      {new PVector(ringOffX,0,0),    //ring
      new PVector(0,-HALFR,0),
      new PVector(0,-HALFR,0),
      new PVector(0,-HALFR,0)},
      {new PVector(littleOffX,0,0),  //little
      new PVector(0,-HALFR,0),
      new PVector(0,-HALFR,0),
      new PVector(0,-HALFR,0)}};

  List<PVector> tmp = new ArrayList<PVector>();
  //you have the CtrlPts in cpts!
  //for each finger 4 points  (o----)o----o----o----o
  //              (palm)  MCP  DIP  PIP  nail
  Set entrySet = rotation.entrySet();
  Iterator it = entrySet.iterator();
  //iterate over the rotation map
  while(it.hasNext()){
    Map.Entry entry = (Map.Entry)it.next();
    Rot rot = (Rot)entry.getValue();
    Integer key = (Integer)entry.getKey();
    int cptskey = 0;

    if(key == 15){          //apply rot to whole figure
      rot.applyTo(new PVector(0,0,0)); //rot camera
    }

    if((key+3)%3 == 0 ){      //apply rot to DIP/PIP/nail
      //System.out.println("apply rot to DIP/PIP/nail");
      if(key == 3)   cptskey = key+1;
      if(key == 6)   cptskey = key+2;
      if(key == 9)   cptskey = key+3;
      if(key == 12)  cptskey = key+4;
      //openGL rotation Matrix

      cpts[cptskey] = finger[key/3][0];
      finger[key/3][1] = rot.applyTo(finger[key/3][1]);
      finger[key/3][0] = PVector.add(finger[key/3][0], finger[key/3][1]);
      cpts[cptskey+1] = finger[key/3][0];
      finger[key/3][2] = rot.applyTo(finger[key/3][2]);
      finger[key/3][0] = PVector.add(finger[key/3][0], finger[key/3][2]);
      cpts[cptskey+2] = finger[key/3][0];
      finger[key/3][3] = rot.applyTo(finger[key/3][3]);
      finger[key/3][0] = PVector.add(finger[key/3][0], finger[key/3][3]);
      cpts[cptskey+3] = finger[key/3][0];

      //TODO palm representation???
      //getAngle(cpts[], cpts[], cpts[cptskey], cpts[cptskey+1]);
      //      ---(palm)---

    }else if((key+2)%3 == 0){  //apply rot to PIP/nail
      //System.out.println("apply rot to PIP/nail");
      if(key != 1) key -= 1;
      if(key == 3)   cptskey = key+1;
      if(key == 6)   cptskey = key+2;
      if(key == 9)   cptskey = key+3;
      if(key == 12)  cptskey = key+4;

      cpts[cptskey] = finger[key/3][0];
      //finger[key/3][1] = rot.applyTo(finger[key/3][1]);
      finger[key/3][0] = PVector.add(finger[key/3][0], finger[key/3][1]);
      cpts[cptskey+1] = finger[key/3][0];
      finger[key/3][2] = rot.applyTo(finger[key/3][2]);
      finger[key/3][0] = PVector.add(finger[key/3][0], finger[key/3][2]);
      cpts[cptskey+2] = finger[key/3][0];
      finger[key/3][3] = rot.applyTo(finger[key/3][3]);
      finger[key/3][0] = PVector.add(finger[key/3][0], finger[key/3][3]);
      cpts[cptskey+3] = finger[key/3][0];

      float angle = getAngle(cpts[cptskey], cpts[cptskey+1], cpts[cptskey+2]);
      System.out.println("angle: " + angle);

    }else if((key+1)%3 == 0){  //apply rot to nail
      //System.out.println("apply rot to nail");
      if(key != 2) key -= 2;
      if(key == 3)   cptskey = key+1;
      if(key == 6)   cptskey = key+2;
      if(key == 9)   cptskey = key+3;
      if(key == 12)  cptskey = key+4;

      cpts[cptskey] = finger[key/3][0];
      //finger[key/3][1] = rot.applyTo(finger[key/3][1]);
      finger[key/3][0] = PVector.add(finger[key/3][0], finger[key/3][1]);
      cpts[cptskey+1] = finger[key/3][0];
      //finger[key/3][2] = rot.applyTo(finger[key/3][2]);
      finger[key/3][0] = PVector.add(finger[key/3][0], finger[key/3][2]);
      cpts[cptskey+2] = finger[key/3][0];
      finger[key/3][3] = rot.applyTo(finger[key/3][3]);
      finger[key/3][0] = PVector.add(finger[key/3][0], finger[key/3][3]);
      cpts[cptskey+3] = finger[key/3][0];

      float angle = getAngle(cpts[cptskey+1], cpts[cptskey+2], cpts[cptskey+3]);
      System.out.println("angle: " + angle);
    }
  }
}*/

//draw the x-, y-, z-lines
void drawCoordinates(int len)
{
  strokeWeight(1);
  stroke(255,0,0);
  line(0,0,0,len,0,0);
  stroke(0,255,0);
  line(0,0,0,0,len,0);
  stroke(0,0,255);
  line(0,0,0,0,0,len);
}

void drawPoints(PVector[] cpts){
  strokeWeight(1);
  noFill();
  beginShape(POINTS);
  int cnt = 1;
  for (PVector cp : cpts) {
    pushMatrix();
    translate(cp.x,cp.y,cp.z);
	//trying to color the first point different...
	if((cnt%4 == 0)){
		stroke(0,0,255);
		//System.out.println("do it!");
	}else stroke(255,255,0);
	//stroke(255,255,0);
    sphere(2);
    popMatrix();
    cnt += 1;
  }
  endShape();

  beginShape(POINTS);
  pushMatrix();
  sphere(2);
  popMatrix();
  endShape();
}

void drawLines(PVector[] cpts){
  int cnt = 0;
  if(cpts.length%4 != 0) System.out.println("Wrong nr of points!");
  stroke(color(255,255,255));
  strokeWeight(1);
  noFill();
  beginShape();
  for (PVector cp : cpts) {
	cnt++;
    vertex(cp.x,cp.y,cp.z);
	if(cnt%4 == 0){
		endShape();
		if(cnt != cpts.length) beginShape();
	}
  }
  //drawPalm();
}

void drawPalm(){
  stroke(color(255,255,255));
  pushMatrix();
  translate(5,25,0);
  box(90,50,10);
  popMatrix();
}

//Later not needed, CtrlPts get declared in updateCtrlPts
PVector[] makeCtrlPts()
{
 // Rot rots[] = map.values().toArray(new Rot[0]);
  List<PVector> p = new ArrayList<PVector>();
  //index finger
  //int indexOffX = -30;
  /*PVector cur = new PVector(indexOffX, 0,0),		//the current point to modify (also starting point)
            r1 = new PVector(indexOffX,-HALFR,0),	//second point of the beztube
			      r2 = new PVector(indexOffX,-HALFR,0),	//third point of the beztube
			      r3 = new PVector(indexOffX,-HALFR,0);	//fourth point of the beztube*/

 

  //index finger
  /*int indexOffX = -30;
  p.add(new PVector(indexOffX,0,0));
  p.add(new PVector(indexOffX,-HALFR,0));
  p.add(new PVector(indexOffX,-HALFR*2,0));
  p.add(new PVector(indexOffX,-HALFR*3,0));

  //add the other ctrlPts!
  //middle finger
  int middleOffX = -10;
  p.add(new PVector(middleOffX,0,0));
  p.add(new PVector(middleOffX,-HALFR,0));
  p.add(new PVector(middleOffX,-HALFR*2,0));
  p.add(new PVector(middleOffX,-HALFR*3,0));

  //ring finger
  int ringOffX = 10;
  p.add(new PVector(ringOffX,0,0));
  p.add(new PVector(ringOffX,-HALFR,0));
  p.add(new PVector(ringOffX,-HALFR*2,0));
  p.add(new PVector(ringOffX,-HALFR*3,0));

  //little finger
  int littleOffX = 30;
  p.add(new PVector(littleOffX,0,0));
  p.add(new PVector(littleOffX,-HALFR,0));
  p.add(new PVector(littleOffX,-HALFR*2,0));
  p.add(new PVector(littleOffX,-HALFR*3,0));*/
  
  int factor = 1000;
  float offX = 0.09138*factor;
  float offZ = -0.01087*factor;
  
  //thumb
  float offX_thumb = 0.07138*factor;
  float tOffsetY = 0.0500*factor; //thumb offset
  p.add(new PVector(offX_thumb,tOffsetY,offZ));      //MCP
  p.add(new PVector(offX_thumb+10,tOffsetY+10,offZ));  //PIP
  p.add(new PVector(offX_thumb+20,tOffsetY+20,offZ));  //DIP
  p.add(new PVector(offX_thumb+30,tOffsetY+30,offZ));  //nail
  
  
 //index finger
  float indexOffY = 0.02957*factor;
  float[] phalInd = {0.03038*factor, 0.02728*factor, 0.02234*factor};  
  p.add(new PVector(offX,indexOffY,offZ));  //MCP
  p.add(new PVector(offX+phalInd[0],indexOffY,offZ));  //PIP
  p.add(new PVector(offX+phalInd[0]+phalInd[1],indexOffY,offZ));  //DIP
  p.add(new PVector(offX+phalInd[0]+phalInd[1]+phalInd[2],indexOffY,offZ));  //nail

  //add the other ctrlPts!
  //middle finger
  float middleOffY = 0.00920*factor;
  float[] phalMid = {0.03640*factor, 0.03075*factor, 0.02114*factor};
  p.add(new PVector(offX,middleOffY,offZ));
  p.add(new PVector(offX+phalMid[0],middleOffY,offZ));
  p.add(new PVector(offX+phalMid[0]+phalMid[1],middleOffY,offZ));
  p.add(new PVector(offX+phalMid[0]+phalMid[1]+phalMid[2],middleOffY,offZ));

  //ring finger
  float ringOffY = -0.01117*factor;
  float[] phalRin = {0.03344*factor, 0.02782*factor, 0.01853*factor};
  p.add(new PVector(offX,ringOffY,offZ));
  p.add(new PVector(offX+phalRin[0],ringOffY,offZ));
  p.add(new PVector(offX+phalRin[0]+phalRin[1],ringOffY,offZ));
  p.add(new PVector(offX+phalRin[0]+phalRin[1]+phalRin[2],ringOffY,offZ));

  //little finger
  float pinkyOffY = -0.03154*factor;
  float[] phalPin = {0.02896*factor, 0.02541*factor, 0.01778*factor};
  p.add(new PVector(offX,pinkyOffY,offZ));
  p.add(new PVector(offX+phalPin[0],pinkyOffY,offZ));
  p.add(new PVector(offX+phalPin[0]+phalPin[1],pinkyOffY,offZ));
  p.add(new PVector(offX+phalPin[0]+phalPin[1]+phalPin[2],pinkyOffY,offZ));  
  
  return (PVector[]) p.toArray(new PVector[0]);
}





static int oldlen=0;

// draw the bezier tubes again
void updateTubes(PVector[] ctrlpts)
{
  int n = 4;	//number of ctrlpts per finger/beztube
  //"initial" case
  if (tubes==null || oldlen!=ctrlpts.length) {
    tubes = new BezTube[ctrlpts.length/n];
    oldlen=ctrlpts.length;
  }

  if (ctrlpts.length%n!=0)
    System.out.println("need controlpoint array %3==0");

  //list reflects the n points in space along the beztube is aligned
  PVector[] list = new PVector[n];
  for (int i=0; i<ctrlpts.length; i++) {
    if (i%n==0) list = new PVector[n];
    list[i%n] = ctrlpts[i];
    if (i%n==(n-1)) {
	  //"initial" case
      if (tubes[i/n]==null){
        tubes[i/n] = new BezTube(this,new Bezier3D(list,list.length),RADIUS,30,30);
		}
      else{
        tubes[i/n].setBez(new Bezier3D(list,list.length));
		}
    }
  }
}

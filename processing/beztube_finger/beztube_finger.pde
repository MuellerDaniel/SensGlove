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




Serial rx;

LinkedHashMap<Integer,Rot> map = new LinkedHashMap<Integer,Rot>();

static final float RADIUS=5, HALFR=30;
static int i=0;
//int cnt = 1;
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

  rx = new Serial(this, Serial.list()[0], 38400);
  System.out.println(Serial.list());

  rx.bufferUntil('\n');

 // initSerial();

  baseMat=g.getMatrix(baseMat);
  while(!serialUp){
	System.out.println("waiting...");
  }
  pcam = new PeasyCam(this,300);
  //pcam.rotateY(PI/2);
  pcam.lookAt(0,0,0,280);

  cpts = makeCtrlPts();
}

/*void initSerial(){
	try{
		rx = new Serial(this, Serial.list()[0], 38400);
		rx.bufferUntil('\n');
		serialUp = true;
	} catch (RuntimeException e) {
        if (e.getMessage().contains("<init>")) {
            System.out.println("port in use, trying again later...");
            serialUp = false;
        }
	}
}*/

void serialEvent(Serial p)
//void readSerial(Serial p)
{
  try{
  //serialUp = true;	//indicating a working serialEvent
  String msg = "";
  float ts,q0,q1,q2,q3;

 if (p==null)
   return;

  msg = p.readString();

 // System.out.println("Counter: " + cnt);
  System.out.println("SerialEvent: " + msg);

  String[] list;
  msg = msg.trim();
  list = split(msg, '\t');
  Rot rot;

  if (list.length >= 4)
  {
	serialUp = true;
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
    rot=new Rot(q0,q1,q3,-q2,true);
    rot=rot.applyInverseTo(nullrot); // calculate inverse
   // System.out.println(list[list.length-1]);

   map.put(id, rot);
  }else System.out.println("not enough!");
  } catch (RuntimeException e){
	System.out.println("!!!!!Somethin somewhere went wrong!!!!!");
	rx.stop();
	rx = new Serial(this, Serial.list()[0], 38400);
	rx.bufferUntil('\n');
	e.printStackTrace();
  }
}

void draw()
{

  background(20);
  textFont(f);
  fill(255);

  //text("hello draw()", 40, 40);

  //rxpacket();
  scale(1,1,1);
  //scale(1,1,1);

  // stage lighting
  pushMatrix();
  g.setMatrix(baseMat);
  directionalLight(200, 200, 200, 100, 100, 100);
  ambientLight(160, 160, 160);
  popMatrix();

  //TODO: make a check, whether you read ALL IMUs
  Rot     rots[] = map.values().toArray(new Rot[0]);
  updateCtrlPts(map);
  //System.out.println("Number of ctrlPts: " + cpts.length);


  //"make" the tubes
  updateTubes(cpts);


  //System.out.println("nr of tubes: " + tubes.length);
  for (BezTube tube : tubes ){
	tube.draw();		//draw them!
}
  // points
  drawPoints(cpts);

  // draw lines between the three points/dots
  drawLines(cpts);

  //draw coordinate system
  //apply the rotation-routine

  for (int i=0; i<map.values().size(); i++) {

	Rot rot    = rots[i];
	text("X-rotation: " + rot.getAngles(RotOrder.XYZ)[0] +
		"\nY-rotation: " + rot.getAngles(RotOrder.XYZ)[1] +
		"\nZ-rotation: " + rot.getAngles(RotOrder.XYZ)[2], -150, -150);

    pushMatrix();
    translate(5,25,07);

    /* apply the rotation */
    rotateX(rot.getAngles(RotOrder.XYZ)[0]);
    rotateY(rot.getAngles(RotOrder.XYZ)[1]);
    rotateZ(rot.getAngles(RotOrder.XYZ)[2]);
	System.out.println("X- rotated: " + rot.getAngles(RotOrder.XYZ)[0]);
	System.out.println("Y- rotated: " + rot.getAngles(RotOrder.XYZ)[1]);
	System.out.println("Z rotated: " + rot.getAngles(RotOrder.XYZ)[2]);
    strokeWeight(2);
    drawCoordinates(300);
	//System.out.println("Drawing! " + map.values().size());
    popMatrix();
  }
}

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
  for (PVector cp : cpts) {
    pushMatrix();
    translate(cp.x,cp.y,cp.z);
	//trying to color the first point different...
/*	if((cnt%4 == 0)){
		stroke(255,0,0);
		//System.out.println("do it!");
	}else stroke(255,255,0);*/
	stroke(255,255,0);
    sphere(2);
    popMatrix();
  }
  endShape();

  beginShape(POINTS);
  pushMatrix();
  translate(5,25,0);
  stroke(255,0,0);
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
  drawPalm();
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
  int indexOffX = -30;
  PVector cur = new PVector(indexOffX, 0,0),		//the current point to modify (also starting point)
            r1 = new PVector(indexOffX,-HALFR,0),	//second point of the beztube
			r2 = new PVector(indexOffX,-HALFR,0),	//third point of the beztube
			r3 = new PVector(indexOffX,-HALFR,0);	//fourth point of the beztube

  //thumb
  int tOffset = -40; //thumb offset
  p.add(new PVector(tOffset,20,0));
  p.add(new PVector(tOffset-10,0,0));
  p.add(new PVector(tOffset-20,-20,0));
  p.add(new PVector(tOffset-30,-40,0));

  //index finger
  //int indexOffX = -30;
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
  p.add(new PVector(littleOffX,-HALFR*3,0));

  return (PVector[]) p.toArray(new PVector[0]);
}


void updateCtrlPts(LinkedHashMap<Integer,Rot> rotation){
	int n = 0;

	int thumbOffX = -40;
	int indexOffX = -30;
	int middleOffX = -10;
	int ringOffX = 10;
	int littleOffX = 30;

	PVector finger[][] ={
					{ new PVector(thumbOffX,20,0),	//thumb
					new PVector(0,-20,0),
					new PVector(0,-20,0),
					new PVector(0,-20,0)},
					{new PVector(indexOffX,0,0),	//index
					new PVector(0,-HALFR,0),
					new PVector(0,-HALFR,0),
					new PVector(0,-HALFR,0)},
					{new PVector(middleOffX,0,0),	//middle
					new PVector(0,-HALFR,0),
					new PVector(0,-HALFR,0),
					new PVector(0,-HALFR,0)},
					{new PVector(ringOffX,0,0),		//ring
					new PVector(0,-HALFR,0),
					new PVector(0,-HALFR,0),
					new PVector(0,-HALFR,0)},
					{new PVector(littleOffX,0,0),	//little
					new PVector(0,-HALFR,0),
					new PVector(0,-HALFR,0),
					new PVector(0,-HALFR,0)}};

	List<PVector> tmp = new ArrayList<PVector>();
	//you have the CtrlPts in cpts!
	//for each finger 4 points	(o----)o----o----o----o
	//						  (palm)  MCP  DIP  PIP  nail
	Set entrySet = rotation.entrySet();
	Iterator it = entrySet.iterator();
	//iterate over the rotation map
	while(it.hasNext()){
		Map.Entry entry = (Map.Entry)it.next();
		Rot rot = (Rot)entry.getValue();
		Integer key = (Integer)entry.getKey();
		int cptskey = 0;

		if(key == 15){					//apply rot to whole figure
			rot.applyTo(new PVector(0,0,0)); //rot camera
		}

		if((key+3)%3 == 0 ){			//apply rot to DIP/PIP/nail
			//System.out.println("apply rot to DIP/PIP/nail");
			if(key == 3) 	cptskey = key+1;
			if(key == 6) 	cptskey = key+2;
			if(key == 9) 	cptskey = key+3;
			if(key == 12)	cptskey = key+4;
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
			//			---(palm)---

		}else if((key+2)%3 == 0){	//apply rot to PIP/nail
			//System.out.println("apply rot to PIP/nail");
			if(key != 1) key -= 1;
			if(key == 3) 	cptskey = key+1;
			if(key == 6) 	cptskey = key+2;
			if(key == 9) 	cptskey = key+3;
			if(key == 12)	cptskey = key+4;

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

		}else if((key+1)%3 == 0){	//apply rot to nail
			//System.out.println("apply rot to nail");
			if(key != 2) key -= 2;
			if(key == 3) 	cptskey = key+1;
			if(key == 6) 	cptskey = key+2;
			if(key == 9) 	cptskey = key+3;
			if(key == 12)	cptskey = key+4;

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
}


float getAngle(PVector startP, PVector angleP, PVector endP){
	PVector dir1 = PVector.sub(angleP,startP);
	PVector dir2 = PVector.sub(endP,angleP);

	return acos((abs(dir1.dot(dir2)))/(dir1.mag() * dir2.mag()));

}



static int oldlen=0;

void updateTubes(PVector[] ctrlpts)
{
  int n = 4;	//number of ctrlpts per finger/beztube
  //"initial" case
  if (tubes==null || oldlen!=ctrlpts.length) {
    tubes = new BezTube[ctrlpts.length/n];
    oldlen=ctrlpts.length;
	//System.out.println("initial? " + ctrlpts.length/n);
  }

  if (ctrlpts.length%n!=0)
    System.out.println("need controlpoint array %3==0");

  //list reflects the n points in space along the beztube is aligned
  PVector[] list = new PVector[n];
  for (int i=0; i<ctrlpts.length; i++) {
    if (i%n==0) list = new PVector[n];
    list[i%n] = ctrlpts[i];
	//System.out.println("list[0]: " + list[0] + " ctrlpts[i] " + ctrlpts[0]);
	//if it is the "last" one, i=2 (i.e. I have all the ctrlpts added to the list)
    if (i%n==(n-1)) {
	  //"initial" case
	  //System.out.println("Here1!i: " + i + " (i-3)%n" + (int)i/n);

      if (tubes[i/n]==null){
		//System.out.println("Here2!list.length: " + list[0]);
        tubes[i/n] = new BezTube(this,new Bezier3D(list,list.length),RADIUS,30,30);
		//System.out.println("Radius and so on...");
		}
      else{
        tubes[i/n].setBez(new Bezier3D(list,list.length));
		//System.out.println("setting the tube number! " + ctrlpts.length);
		}
    }
  }
}

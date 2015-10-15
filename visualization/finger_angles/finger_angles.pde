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
import java.io.*;
//mport java.lang.Object;

PMatrix3D baseMat;
PeasyCam pcam;
BezTube tubes[];
PVector cpts[];
Rot nullrot=new Rot(1,0,0,0,false),
        rot=new Rot(1,0,0,0,false);
        
BufferedReader reader;
//String pipePath = "../../../python/estimatedAngles";
String pipePath = "estimatedAngles";
//String pipePath = "myPath5";
float angles[];

// finger lengths/coordinates
int factor = 1000;
float offX = 0.09138*factor;    // level of MCPs
float offZ = -0.01087*factor;   // level of MCPs
float offX_thumb = 0.07138*factor;  //thumb 
float thumbOffY = 0.0490*factor; 
float[] phalThumb = {0.02038*factor, 0.01728*factor, 0.01234*factor};
float indexOffY = 0.02957*factor;    //index
float[] phalInd = {0.03038*factor, 0.02728*factor, 0.02234*factor};
float middleOffY = 0.00920*factor;   //middle
float[] phalMid = {0.03640*factor, 0.03075*factor, 0.02114*factor};
float ringOffY = -0.01117*factor;    //ring
float[] phalRin = {0.03344*factor, 0.02782*factor, 0.01853*factor};
float pinkyOffY = -0.03154*factor;  //pinky
float[] phalPin = {0.02896*factor, 0.02541*factor, 0.01778*factor};

LinkedHashMap<Integer,Rot> map = new LinkedHashMap<Integer,Rot>();

static final float RADIUS=5, HALFR=30;  // RADIUS for beztube, HALFR distance between joints
static int i=0;
boolean serialUp = false;
static int id = 5 ;	//variable for indicating the IMU (IDs range from 0 to 15)
PFont f;

void setup()
{
  //size(1920,1080,P3D);
  size(500,500,P3D);

  f = createFont("Arial", 8, true);
  textFont(f);
  fill(255);
  
  reader = createReader(pipePath);

  pcam = new PeasyCam(this,300);  
  pcam.lookAt(60,0,0);
  pcam.rotateZ(PI/2);
  pcam.rotateY(-PI);
  
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
  try{
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
    //and now apply the angles to your points...
    extractAngles(line);
    updateCtrlPts();
  }

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
  angles = new float[list.length];
  for(int i = 0; i<list.length; i++){
     angles[i] = Float.parseFloat(list[i]);
     System.out.println(angles[i]);
  }
}

float sumAngles(int angleCnt, int amount){
  float res = 0.0; 
  for (int i = 0; i<=amount; i++){
      res += angles[angleCnt-i];
   } 
   return res;
}

void updateCtrlPts(){
  // apply the angles   
  float[] phal = new float[3];
  int cnt = 0;
  int pt = -2;
  for (int i=0; i<angles.length; i++) {
     if((i%3) == 0){    //change the finger
       switch (i){
         case 0: phal = phalThumb;
                 cnt = 0;
                 break;
         case 3: phal = phalInd;
                 cnt = 0;
                 break;
         case 6: phal = phalMid;
                 cnt = 0;
                 break;
         case 9: phal = phalRin;
                 cnt = 0;
                 break;
         case 12: phal = phalPin;
                 cnt = 0;
                 break; 
         default: System.out.println("default..."); 
                  break;         
       }  
     } 
    if(cnt == 0){
     pt += 2;     
    } else {
      pt += 1;       
    }
    // for angles transported in deg
    //cpts[pt+1].x = cpts[pt].x+phal[cnt]*cos(radians(sumAngles(i,cnt)));
    //cpts[pt+1].z = cpts[pt].z-phal[cnt]*sin(radians(sumAngles(i,cnt)));
    // for angles transported in rad
    cpts[pt+1].x = cpts[pt].x+phal[cnt]*cos(sumAngles(i,cnt));
    cpts[pt+1].z = cpts[pt].z-phal[cnt]*sin(sumAngles(i,cnt));
    cnt += 1;
  }  
}


float getAngle(PVector startP, PVector angleP, PVector endP){
  PVector dir1 = PVector.sub(angleP,startP);
  PVector dir2 = PVector.sub(endP,angleP);
  return acos((abs(dir1.dot(dir2)))/(dir1.mag() * dir2.mag()));
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
    
  //thumb  
  p.add(new PVector(offX-30,thumbOffY,offZ));      //MCP
  p.add(new PVector(offX-30+phalThumb[0],thumbOffY,offZ));  //PIP
  p.add(new PVector(offX-30+phalThumb[0]+phalThumb[1],thumbOffY,offZ));  //DIP
  p.add(new PVector(offX-30+phalThumb[0]+phalThumb[1]+phalThumb[2],thumbOffY,offZ));  //nail
  
  
 //index finger  
  p.add(new PVector(offX,indexOffY,offZ));  //MCP
  p.add(new PVector(offX+phalInd[0],indexOffY,offZ));  //PIP
  p.add(new PVector(offX+phalInd[0]+phalInd[1],indexOffY,offZ));  //DIP
  p.add(new PVector(offX+phalInd[0]+phalInd[1]+phalInd[2],indexOffY,offZ));  //nail

  //add the other ctrlPts!
  //middle finger  
  p.add(new PVector(offX,middleOffY,offZ));
  p.add(new PVector(offX+phalMid[0],middleOffY,offZ));
  p.add(new PVector(offX+phalMid[0]+phalMid[1],middleOffY,offZ));
  p.add(new PVector(offX+phalMid[0]+phalMid[1]+phalMid[2],middleOffY,offZ));

  //ring finger  
  p.add(new PVector(offX,ringOffY,offZ));
  p.add(new PVector(offX+phalRin[0],ringOffY,offZ));
  p.add(new PVector(offX+phalRin[0]+phalRin[1],ringOffY,offZ));
  p.add(new PVector(offX+phalRin[0]+phalRin[1]+phalRin[2],ringOffY,offZ));

  //little finger  
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

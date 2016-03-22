
module sensorSlot(){
	difference(){
		cube([15.0,15.7,6.0],false);		//outer cube
		translate([1,0,3.7])					//inner cube
			//cube([12.9,14.7,1.2],false);		
			cube([13.0,14.7,1.2],false);		
		translate([1.6,0,4.8])				//upper cube
			cube([11.8,14.3,1.3]);		
		
	}
}

distY = 20;
distX = 20.3;

//the four sensor slots
translate([0,distY,0])
	sensorSlot();
translate([distX,distY,0])
	sensorSlot();
translate([2*distX,distY,0])
		sensorSlot();
translate([3*distX,distY,0])
		sensorSlot();

//the "ground plate"
groundHeigth = 3;
translate([-2,0,-groundHeigth])
		color("blue") cube([79.7,35.7,groundHeigth]);

//for the strap
translate([-8,3.7,-groundHeigth])
	difference(){
		cube([6,32,groundHeigth]);
		translate([3,3,0])
			cube([3,26,groundHeigth]);
}

translate([83.7,3.7,-groundHeigth])
	mirror(){
	difference(){
		cube([6,32,groundHeigth]);
		translate([3,3,0])
			cube([3,26,groundHeigth]);
}
}

module sensorSlot(){
	difference(){
		cube([14.9,15.7,5.9],false);		//outer cube
		translate([1,0,3.7])					//inner cube
			cube([12.9,14.7,1.2],false);		
		translate([1.4,0,4.9])				//upper cube
			cube([12.1,14.3,1]);		
		
	}
}

distY = 20;
distX = 20.3;

//the four sensor slots
translate([0,distY,0])
	sensorSlot();
translate([distX,0,0])
	sensorSlot();
translate([2*distX,distY,0])
		sensorSlot();
translate([3*distX,0,0])
		sensorSlot();

//the "ground plate"
translate([-2,0,-2])
		color("blue") cube([79.7,35.7,2]);

//for the strap
translate([-7,5.7,-2])
	difference(){
		cube([5,30,2]);
		translate([2,2,0])
			cube([3,26,2]);
}

translate([82.7,5.7,-2])
	mirror(){
	difference(){
		cube([5,30,2]);
		translate([2,2,0])
			cube([3,26,2]);
}
}
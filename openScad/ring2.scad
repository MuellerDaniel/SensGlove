$fn=100;
module ring(heigth,radius){
	// the ring itself
	radius = radius+1;
	difference(){
		cylinder(h=heigth,r=radius+1,center=true);
		cylinder(h=heigth+1,r=radius,center=true);
		// the hole...
   		rotate([0,0,0]) translate([-radius,0,0]) cube([3,7,heigth+2],center=true);
	}

	// the magnet holder
	rMag = 2.5;
	translate([radius+rMag+0.5,0,0])
	difference(){
		cube([rMag*2+1,rMag*2+2,heigth],center=true);
		translate([0.7,0,0.5]) 
		union(){						
			cylinder(h=heigth-0.5,r1=rMag+0.2,r2=rMag,center=true);	//inner cylinder
			translate([rMag,0,0]) cube([3,3.8,heigth-0.5],center=true);	//upper hole
		}
	}
	// the connection/stabilization thing
	// for radius = 7.5
	translate([radius,-(rMag*2+2)/2,0])		
	linear_extrude(height = heigth, center = true, convexity = 10, twist = 0)
	polygon(points=[[0,0],[-3,-4],[(rMag*2+1)/2,0]], paths=[[0,1,2]]);
	mirror([0,1,0])
	translate([radius,-(rMag*2+2)/2,0])
	linear_extrude(height = heigth, center = true, convexity = 10, twist = 0)
	polygon(points=[[0,0],[-3,-4],[(rMag*2+1)/2,0]], paths=[[0,1,2]]);
}


/* radi for (my)fingers:
	index: 7.5
	middle: 8 
	ring: 7.5
	pinky: 6

	wooden hand:
	index: 7.5
	middle: 7.5 
	ring: 7.5
	pinky: 7	


	dimensions of magnet: 
	radius = 2.5
	length = 15
*/
ring(16,7.5);
//translate([0,0,20])
//cylinder(h=16-0.5,r1=2.5+0.2,r2=2.5-0.1,center=true);





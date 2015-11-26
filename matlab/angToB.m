function b = angToB(theta,finger,s,yOff)
p = angToP(theta,finger,yOff);
r = s-p;
h = angToH(theta);
% b = (((3*dot(h,r)*r)/(norm(r)^5)) - (h/norm(r)^3)).*[1, 1, 1];
b = calcB(r,h);








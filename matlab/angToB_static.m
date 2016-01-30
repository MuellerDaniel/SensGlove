function b = angToB_static(theta)
r = angToP_static(theta);
% r = s-p;
h = angToH(theta);
% b = (((3*dot(h,r)*r)/(norm(r)^5)) - (h/norm(r)^3)).*[1, 1, 1];
b = calcB_dip(r,h);








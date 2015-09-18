function b = evalfuncMag_sim(P,S)
H = P-S;
R = S-P;
factor = -1;
% b = ((3*(cross(H,R))*R'/(norm(R)^5))-H/(norm(R)^3)).*factor';
b = ((3*(dot(H,R))*R/(norm(R)^5))-H/(norm(R)^3)).*factor';
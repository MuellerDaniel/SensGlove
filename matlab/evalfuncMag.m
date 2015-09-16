function b = evalfuncMag(P,S)
H = P-S;
R = S-P;
factor = [-1 -1 -1];
% (3*(cross(H,R)*R/(norm(R)^5))-H/(norm(R)^3))
b = (3*(dot(H,R)*R/(norm(R)^5))-H/(norm(R)^3)).*factor;
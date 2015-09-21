function b = evalfuncMag_HR(H,R)
% H = P-S;
% R = S-P;
factor = -1;
% disp('dot product ');
% disp(dot(H,R));
% b = ((3*(cross(H,R))*R'/(norm(R)^5))-H/(norm(R)^3)).*factor';
b = ((3*(dot(H,R))*R/(norm(R)^5))-H/(norm(R)^3)).*factor;
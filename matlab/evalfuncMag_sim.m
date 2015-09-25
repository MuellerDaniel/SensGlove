function b = evalfuncMag_sim(P,S)
H = P-S;
R = S-P;
factor = 2.4e-4;
% disp('dot product ');
% disp(dot(H,R));
% b = ((3*(cross(H,R))*R'/(norm(R)^5))-H/(norm(R)^3)).*factor';
b = ((3*(dot(H,R))*R/(norm(R)^5))-H/(norm(R)^3)).*factor;
% written form
% b(1) = (3*(dot(H,R)*R(1)/norm(R)^5)-(H(1)/norm(R)^3))*factor;
% b(2) = (3*(dot(H,R)*R(2)/norm(R)^5)-(H(2)/norm(R)^3))*factor;
% b(3) = (3*(dot(H,R)*R(3)/norm(R)^5)-(H(3)/norm(R)^3))*factor;
% b = b';

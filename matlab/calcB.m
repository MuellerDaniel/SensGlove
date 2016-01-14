function b = calcB(p,r,h)
% function b = calcB(r,h)
factor = [1 1 1];
% factor = [3.0593e-04 1 1];
Br = 12.6e+03;
mu_0 = 4*pi*1e-07;
mu_r = 1.05;
% addFact = 0.2312;
addFact = 1;
lambda = (Br*mu_0*mu_r)/(4*pi)*addFact;
% lambda = 1;
off = [0 0 0];
d = p-r;
% d = r;
b = (((3*d.*dot(h,d))/(norm(d)^5)) - (h/norm(d)^3)).*lambda + off;
% b = (((3*r.*dot(h,r))/(norm(r)^5)) - (h/norm(r)^3)).*factor;


%approach with normed direction vector
% b = (r./norm(r)*3*dot(h,(r./norm(r)))-h).*(1/(4*pi*norm(r)^3)); 
% approach from wikipedia
% b = (1/(4*pi*norm(r)^2))*(((r.*3*dot(h,r))-(h.*norm(r)^2))/(norm(r)^3));
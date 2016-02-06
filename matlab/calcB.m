function b = calcB(p,r,h)
% function b = calcB(r,h)
% factor = [1 1 1];
% factor = [3.0593e-04 1 1];


d = p-r;

b = calcB_dip(d,h);
% b = (((3*r.*dot(h,r))/(norm(r)^5)) - (h/norm(r)^3)).*factor;


%approach with normed direction vector
% b = (r./norm(r)*3*dot(h,(r./norm(r)))-h).*(1/(4*pi*norm(r)^3)); 
% approach from wikipedia
% b = (1/(4*pi*norm(r)^2))*(((r.*3*dot(h,r))-(h.*norm(r)^2))/(norm(r)^3));
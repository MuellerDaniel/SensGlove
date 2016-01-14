function b = calcB_lect(x,l_mag,h)
r_mag = 0.0025;
Br = 1.26e4;
% b = (r_mag^2*l_mag)/(4*pi*norm(x)^3)*(x/norm(x));
b = (2*cos(h).*(x/(norm(x)))+(h/norm(h)).*sin(h)).*((Br*r_mag^2*l_mag)/(4*pi*norm(x)^3));
% b = (2*cos(h).*(x/(norm(x)))+(h/1).*sin(h)).*((Br*r_mag^2*l_mag)/(4*norm(x)^3));
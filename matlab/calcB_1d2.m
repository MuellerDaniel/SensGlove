% aproach from magnet web page
function b = calcB_1d2(x)
% cylinder magnet
l_mag = 0.015;  
% l_mag = 0.0002;
r_mag = 0.0025;
Br = 1.26;
% r_mag = 0.0001;
% factor = 1.2368e+07;
b = (Br/2)*((l_mag+x)/sqrt(r_mag^2+(l_mag+x)^2) - (x/sqrt(r_mag^2+x^2)));
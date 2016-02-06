% aproach from lecture page
function b = calcB_1d(x)
% cylinder magnet
l_mag = 0.015;  
% l_mag = 0.0002;
r_mag = 0.0025;
Br = 1.26;
% Br = 2;
b_mag = l_mag/2;
% b = (Br/2)*((l_mag+x)/sqrt(r_mag^2+(l_mag+x)^2) - (x/sqrt(r_mag^2+x^2)));
% b = (Br/2)*((x)/sqrt(x^2+r_mag^2)-((x-l_mag)/sqrt((x-l_mag)^2+r_mag^2)));

b = (Br/2) * ((x+b_mag)/sqrt(r_mag^2+(x+b_mag)^2) -...
                (x-b_mag)/sqrt(r_mag^2+(x-b_mag)^2));


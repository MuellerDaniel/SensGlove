% function B = calcB_cyl(z,rho)     % approach for passing the real z and rho values in [m]
function B = calcB_cyl(p,ang)       % approach for passing the position of the center and the angle between orientation and coSys
ang = ang/1;
rotMat = [cos(ang) -sin(ang); sin(ang) cos(ang)];
cylCo = p*rotMat;
z = cylCo(1);
rho = cylCo(2);

z
rho

a = 0.0025;     % radius in m
b = 0.015/2;    % half length of magnet
% magic value...
Bo = 1.0e+3*4.0107;      % magnetic constant

% component calculations
z_pos = z+b;
z_neg = z-b;

alpha_pos = a/sqrt(z_pos^2+(rho+a)^2);
alpha_neg = a/sqrt(z_neg^2+(rho+a)^2);

beta_pos = z_pos/sqrt(z_pos^2+(rho+a)^2);
beta_neg = z_neg/sqrt(z_neg^2+(rho+a)^2);

gamma = (a-rho)/(a+rho);

k_pos = sqrt((z_pos^2+(a-rho)^2)/(z_pos^2+(a+rho)^2));
k_neg = sqrt((z_neg^2+(a-rho)^2)/(z_neg^2+(a+rho)^2));

B_rho = Bo*(alpha_pos*cel(k_pos,1,1,-1)-alpha_neg*cel(k_neg,1,1,-1));
B_z   = (Bo*a)/(a+rho)*(beta_pos*cel(k_pos,gamma^2,1,gamma)-beta_neg*cel(k_neg,gamma^2,1,gamma));

B = [B_z B_rho]*rotMat^-1;
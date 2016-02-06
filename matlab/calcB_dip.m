function b = calcB_dip(r,h)

Br = 1.26;
mu_0 = 4*pi*1e-07;
mu_r = 1.32*1e-06;
l_mag = 0.015;
r_mag = 0.0025;
% addFact = 1;
addFact = Br*(pi*r_mag^2*l_mag)/mu_0;
h = h*addFact;
lambda = mu_0/(4*pi);
% lambda = (Br*mu_0*mu_r)/(4*pi)*addFact;
% lambda = addFact*mu_r/(4*pi);
% lambda = 1;

% h = [1 0 0];

b = (((3*r.*dot(h,r))/(norm(r)^5)) - (h/norm(r)^3)).*lambda;
function bS = angToB_sym_T(theta)

r = angToP_sym(theta);
h = angToH_sym(theta);

Br = 12.6e+03;
mu_0 = 4*pi*1e-07;
mu_r = 1.05;
% addFact = 0.2312;
addFact = 1;
lam = (Br*mu_0*mu_r)/(4*pi)*addFact;
lambda = [lam -lam lam];

bS = symfun([(((3*r*(h*r'))/(norm(r)^5)) -...
                (h/norm(r)^3))], [theta(1) theta(2)]);

% bS = symfun([3*r ],[theta(1) theta(2)]);
%% for a variable sensor-finger combination

function bS = varAngToB_A_sym(theta, index_s, index_m)

r = varAngToP_A_sym(theta, index_s, index_m);
h = angToH_A_sym(theta);

Br = 12.6e+03;
mu_0 = 4*pi*1e-07;
mu_r = 1.05;
% addFact = 0.2312;
addFact = 1;
lam = (Br*mu_0*mu_r)/(4*pi)*addFact;
lambda = [lam -lam lam];

b = symfun((((3*r*(h*r'))/(norm(r)^5)) -...
                (h/norm(r)^3)).*lambda, [theta(1) theta(2) theta(3)]);
            
bS = formula(b)';            
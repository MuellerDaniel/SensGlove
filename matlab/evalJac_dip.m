%% calculating and evaluating the jacobian of the DIP model
function jac_evN = evalJac_dip(R_k, H_k)

syms hx hy hz rx ry rz
H = [hx; hy; hz];
R = [rx; ry; rz];

model = symfun((3*dot(H,R)*R)/(norm(R)^5) - H/(norm(R)^3), [R; H]);

jac = jacobian(model,([R;H]));

e_rx = R_k(1);
e_ry = R_k(2);
e_rz = R_k(3);
e_hx = H_k(1);
e_hy = H_k(2);
e_hz = H_k(3);

jac_evS = jac(e_rx, e_ry, e_rz,...
                e_hx, e_hy, e_hz)';

jac_evN = double(jac_evS);            
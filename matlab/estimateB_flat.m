function n = estimateB_flat(r,p,h,b)
% r3d = [r 0 0];
% calcB(r3d,h);
% b3d = [b(1) 0 0];
dif = b - calcB(r,p,h);
n = norm(dif)^2;
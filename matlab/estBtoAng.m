function n = estBtoAng(theta,finger,s,B,yOff)
estimated = angToB(theta,finger,s,yOff);
n = norm(B-estimated)^2;
    
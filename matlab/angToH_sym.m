function h = angToH_sym(theta)

thetaS = [theta(1) theta(2) theta(2)*2/3];

h = symfun([cos(-thetaS(1)-thetaS(2)-thetaS(3)),...    
             0,...
             1*sin(-thetaS(1)-thetaS(2)-thetaS(3))],[theta(1) theta(2)]);
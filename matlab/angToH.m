function h = angToH(theta)

theta = [theta(1) theta(2) theta(2)*2/3];

h = [cos(-theta(1)-theta(2)-theta(3)),...    
     0,...
     1*sin(-theta(1)-theta(2)-theta(3))];
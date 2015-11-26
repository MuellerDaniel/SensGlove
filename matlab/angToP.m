function p = angToP(theta,finger,yOff)

%% approach/alignment from paper (sensor at wrist) WORKS!
%   finger_0 = off(3);    % length of back of hand
  finger_0 = 0.0;    % length of back of hand
  theta_0 = pi/2;    % angle of wrist
  theta_k = 0.0;   % fixed angle between sensor and hand x-z plane 
  dk = yOff; % y postion of "joint-axis"
  
%   rot = [0 0 -1;    % rotate 270° around y axis
%         0 1 0;
%         1 0 0];
  
% the hand is aligned at 90° in the plane! so subtract all the angles from
% pi/2!
p = [1*((finger_0*sin(pi/2) + finger(1)*sin(pi/2-theta(1)) +...    % x
    finger(2)*sin(pi/2-theta(1)-theta(2)) +...
    finger(3)*sin(pi/2-theta(1)-theta(2)-theta(3)))),...                 
    (finger(1)*cos(pi/2-theta(1)) +...   % y
    finger(2)*cos(pi/2-theta(1)-theta(2)) +...
    finger(3)*cos(pi/2-theta(1)-theta(2)-theta(3)))*sin(theta_k)+dk,...
    -1*((finger(1)*cos(pi/2-theta(1)) +...       % z (*-1 because you move in neg. z-direction)
    finger(2)*cos(pi/2-theta(1)-theta(2))+...
    finger(3)*cos(pi/2-theta(1)-theta(2)-theta(3)))*cos(theta_k))];
 

    
    
  
% function x = xPos(angle,phal,off)
% x = phal(1)*cos(angle(1))+...
%     phal(2)*cos((angle(1))+(angle(2)))+...
%     phal(3)*cos((angle(1))+(angle(2))+(angle(3)))+off;
% 
% function y = yPos(~,~,off)
% y = off;
% 
% function z = zPos(angle,phal,off)
% z = (-1*phal(1)*sin(angle(1))-...
%     phal(2)*sin((angle(1))+(angle(2)))-...
%     phal(3)*sin((angle(1))+(angle(2))+(angle(3))))+off;
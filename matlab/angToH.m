function h = angToH(theta)
% % my version...
% h = [cos(pi-theta(1)-theta(2)-theta(3))*cos(0),...
%       0,...
%       1*sin(pi-theta(1)-theta(2)-theta(3))];

% with fixed orientation...
% h = [-0.5 0.1 -0.1];

% % approach from paper
finger_0 = 0.0841;    % length of back of hand
finger_0 = 0.03;    % length of back of hand
theta_0 = pi/2;    % angle of wrist
theta_k = 0.0;   % fixed angle between sensor and hand x-z plane ???
dk = 0.0; % y postiont of "joint-axis"

rot1 = [0 0 1;
        0 1 0;
        -1 0 0];
rot2 = [0 0 1;    
        0 1 0;
        -1 0 0];
 
%% alignment as in paper... WORKS!
h = [cos(-theta(1)-theta(2)-theta(3)),...    
     0,...
     1*sin(-theta(1)-theta(2)-theta(3))].*1;
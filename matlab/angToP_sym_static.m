%% for a fixed sensor-finger combination

function pS = angToP_sym_static(theta)

thetaS = [theta(1) theta(2) theta(2)*2/3];

% declaring the various fingerlengths
phalInd = [0.03080 0.02581 0.01678];
phalMid = [0.03593 0.03137 0.01684];
phalRin = [0.03404 0.02589 0.01820];
phalPin = [0.02892 0.02493 0.01601];
finger = phalInd;

% declaring the sensor positions
sInd_car = [-0.02 -0.0  0.004];    % rack1
sMid_car = [-0.02 -0.02 0.004];
sRin_car = [-0.02 -0.04 0.004];
sPin_car = [-0.02 -0.06 0.004];
sPos = sInd_car;

% declaring the joint positions
jointInd_car = [0.0 0.0 -0.0];
jointMid_car = [0.0 -0.02 0.0];
jointRin_car = [0.0 -0.04 0.0];
jointPin_car = [0.0 -0.06 -0.0];
off = jointInd_car;


finger_0 = 0.;
theta_k = 0.0;

pS = symfun( sPos - [(1*(finger_0*sin(pi/2.) + finger(1)*sin(pi/2-thetaS(1)) +...              % x
                finger(2)*sin(pi/2-thetaS(1)-thetaS(2)) +...
                finger(3)*sin(pi/2-thetaS(1)-thetaS(2)-thetaS(3))+off(1))),...
                ((finger(1)*cos(pi/2-thetaS(1)) +...                  % y
                finger(2)*cos(pi/2-thetaS(1)-thetaS(2)) +...
                finger(3)*cos(pi/2-thetaS(1)-thetaS(2)-thetaS(3)))*sin(theta_k)+off(2)),...
                (-1*(finger(1)*cos(pi/2-thetaS(1)) +...               % z (*-1 because you move in neg. z-direction)
                finger(2)*cos(pi/2-thetaS(1)-thetaS(2)) +...
                finger(3)*cos(pi/2-thetaS(1)-thetaS(2)-thetaS(3)))*cos(theta_k)+off(3))],...
                [theta(1) theta(2)]);        
        
% p = sPos - p_abs;


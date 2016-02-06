%% for a variable sensor-finger combination

function pS = varAngToP_A_sym(theta, index_s, index_m)
psi = theta(3);
thetaS = [theta(1) theta(2) theta(2)*2/3];

sInd = sym('sInd', [1 3]);
sMid = sym('sMid', [1 3]);
sRin = sym('sRin', [1 3]);
sPin = sym('sPin', [1 3]);

jointInd = sym('jointInd', [1 3]);
jointMid = sym('jointMid', [1 3]);
jointRin = sym('jointRin', [1 3]);
jointPin = sym('jointPin', [1 3]);

phalInd = sym('phalInd', [1 3]);
phalMid = sym('phalMid', [1 3]);
phalRin = sym('phalRin', [1 3]);
phalPin = sym('phalPin', [1 3]);


% assigning the sensorposition
switch index_s      
    case 1
        sPos = sInd;
    case 2        
        sPos = sMid;
    case 3
        sPos = sRin;
    case 4
        sPos = sPin;
    otherwise
        warning('Unexpected sensor number %d!!!', index_s);        
        sPos = [0 0 0];        
end

% assigning the fingerlengths and jointpositions
switch index_m
    case 1
        finger = phalInd;
        off = jointInd;
    case 2
        finger = phalMid;
        off = jointMid;
    case 3
        finger = phalRin;
        off = jointRin;
    case 4
        finger = phalPin;
        off = jointPin;
    otherwise
        warning('Unexpected finger number %d!!!', index_m);        
        finger = [0 0 0];
        off = [0 0 0];
end


finger_0 = 0.;
% theta_k = 0.0;

pS = symfun([(1*(finger_0*sin(pi/2.) + finger(1)*sin(pi/2-thetaS(1)) +...              % x
                    finger(2)*sin(pi/2-thetaS(1)-thetaS(2)) +...
                    finger(3)*sin(pi/2-thetaS(1)-thetaS(2)-thetaS(3))+off(1))),...                    
                    (finger(1)*cos(pi/2-theta(1)) + ...
                    finger(2)*cos(pi/2-theta(1)-theta(2)) + ...
                    finger(3)*cos(pi/2-theta(1)-theta(2)-theta(3)))*sin(psi) + off(2),...                    
                    (-1*(finger(1)*cos(pi/2-thetaS(1)) +...               % z (*-1 because you move in neg. z-direction)
                    finger(2)*cos(pi/2-thetaS(1)-thetaS(2)) +...
                    finger(3)*cos(pi/2-thetaS(1)-thetaS(2)-thetaS(3)))*cos(psi) + off(3))] - sPos,...
                    [theta(1) theta(2) theta(3)]);        
        
% p = sPos - p_abs;




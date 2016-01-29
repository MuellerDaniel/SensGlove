%% the prediction step...
function [x_now, P_now] = EKF_update_dip2(jacSim, meas, x_pred, P_pred, R)

% % 6 state case...
% c = jacSim(x_pred(1),x_pred(2),x_pred(3),...
%             x_pred(4),x_pred(5),x_pred(6))';

% 3 state case
c = jacSim(x_pred(1),x_pred(2),x_pred(3));
% disp('jacobi');
% disp(num2str(double(c)));

g = P_pred * transpose(c) * ((c * P_pred * transpose(c) + R)^-1);
% disp('g');
% disp(num2str(double(g)));

% % 6 state case...
% x_now = x_pred + g' * (meas - calcB_dip(x_pred(1:3),x_pred(4:6)));
x_now = x_pred + g * (meas - calcB_dip(x_pred(1:3)',[1 0 0])');
dif = meas - calcB_dip(x_pred(1:3)',[1 0 0])'

P_now = (eye(3) - g * c) * P_pred;

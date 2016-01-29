%% the prediction step...
function [x_now, P_now] = EKF_update_dip(jacSim, meas, x_pred, P_pred, R)

% 3 state case
y = meas - calcB_dip(x_pred(1:3)',[1 0 0])';
tmp = jacSim(x_pred(1), x_pred(2), x_pred(3));

% % 6 state case...
% y = meas - calcB_dip(x_pred(:,1:3),x_pred(:,4:6));
% tmp = jacSim(x_pred(:,1:3),x_pred(:,4:6));

S = tmp * P_pred * transpose(tmp) + R;

K = P_pred * transpose(tmp) * S^-1;

P_now = (eye(3) - K * tmp)*P_pred;

x_now = x_pred + K * y;  % with K it doesn't work (although it is explained with it... K' * meas

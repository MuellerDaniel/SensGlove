%% the update step...
function [x_pred, P_pred] = EKF_prediction_dip(x, P_old, Q)

x_pred = x;
P_pred = P_old + Q;



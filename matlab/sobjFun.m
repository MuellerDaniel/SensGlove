%% for one magnet and one sensor
function estPos = sobjFun(P,S,B)
% this is the straight forward approach, but it works
estPos = norm(B - evalfuncMag_sim(P,S));      
% the 'advanced' approach with pseudo inverse and so on...
% estPos = norm((eye(3)-P*pinv(P))*B);
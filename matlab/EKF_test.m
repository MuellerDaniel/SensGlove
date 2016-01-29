%% testing the effects of EKF...

% data simulation
p = 0.5;
h = [1 0 0];
t = 0.04:0.001:0.1;
r = zeros(length(t),3);
b_sim = zeros(length(t),3);
b_sim_noise = zeros(length(t),3);

for i = 1:length(t)
    r(i,:) = [t(i) 0. 0.];
    b_sim(i,:) = calcB_dip(r(i,:),h);
%     b_sim_noise(i,:) = calcB_dip(r(i,:),h) + [-4 7 9];
    b_sim_noise(i,:) = calcB_dip(r(i,:),h) + p*randn(3,1)';
end

close all
figure;
plot(t,b_sim(:,1),'r',t,b_sim(:,2),'r--',t,b_sim(:,3),'r:',...
      t,b_sim_noise(:,1),'b',t,b_sim_noise(:,2),'b--',t,b_sim_noise(:,3),'b:')
legend('x clean', 'y clean', 'z clean',...
        'x noisy', 'y noisy', 'z noisy');
title('clean vs noisy measurements');  




%% assuming you pass in 6 states (rx ry rz hx hy hz)
% no good results though...

%% deriving the jacobian 
% 6 state variables

% syms hx hy hz rx ry rz
% H = [hx; hy; hz];
% R = [rx; ry; rz];
% 
% model = symfun((3*dot(H,R)*R)/(norm(R)^5) - H/(norm(R)^3), [R; H]);
% 
% jacSim = jacobian(model,([R;H]));

%% deriving the jacobian
% 3 state variables (simpler and more realistic...)

syms rx ry rz
R = [rx; ry; rz];
H = [1; 0; 0];

Br = 12.6e+03;
mu_0 = 4*pi*1e-07;
mu_r = 1.05;
% addFact = 0.2312;
addFact = 1;
lambda = (Br*mu_0*mu_r)/(4*pi)*addFact;

model = symfun(lambda*((3*dot(H,R)*R)/(norm(R)^5) - H/(norm(R)^3)), R);

jacSim = jacobian(model,R);

%% Kalman stuff...
% initial error covariance matrix (3x3)
% not soooo important, since it gets estimated...
P = diag([1 1 1]);  

% process noise covariance matrix (3x3)
% a diagnal one simply???    
% Q = diag([1e+2 1e-2 1e-2 ]); 
Q = [[1e+4 1e+1 1e+1];
    [1e+1 1e+2 1e+1];
    [1e+1 1e+1 1e+2]];

% % 6 state case...
% % measurement noise covariance matrix (6x6)
% % also just a diagonal one?
% R = diag([20 20 20 20 20 20]);

% 3 state case; R = (3x3)
% R = diag([1e-3 1e-3 1e-3]);
% R = [[10 1e-10 1e-10];
%     [1e-10 10 1e-10];
%     [1e-10 1e-10 10]];
R = zeros(3,3);

% % 6 state case...
% x = ones(6,length(t));
% x(:,1) = [r(1,:) h]';

% 3 state case
x = ones(3,length(t));
x(:,1) = r(1,:)';

cnt = 2;
for i = b_sim_noise'
% for i = b_sim'
    disp('-------------step---------------');
    disp(cnt);
    
    [x_pre, P_pre] = EKF_prediction_dip(x(:,cnt-1), P, Q);
    disp('x_pre:');
    disp(num2str(x_pre));
    disp('P_pre');
    disp(num2str(double(P_pre)));
    
%     [x(:,cnt), P] = EKF_update_dip2(jacSim, i, x_pre, P_pre, R);
%     disp('x_now');
%     disp(num2str(x(:,cnt)));
%     disp('new P:');
%     disp(num2str(double(P)));
    
%     [x(:,cnt), P] = EKF_update_dip(jacSim, i, x(:,cnt), P, R);
    
%     k = waitforbuttonpress;    
    
    cnt = cnt+1;
end

t = [t 0.101];
figure;
plot(t,x(1,:),'r',t,x(2,:),'g',t,x(3,:),'b')
legend('r_x', 'r_y', 'r_z');
title('filtered pos')

% % 6 states representation
% figure;
% plot(t,x(4,:),'r',t,x(5,:),'g',t,x(6,:),'b')
% legend('h_x','h_y','h_z');
% title('filtered orien')

%% the measurements for the estimated states...
b_filtered = zeros(length(t),3);
cnt = 1;
for i = x
   b_filtered(cnt,:) = calcB_dip(i(1:3)',[1 0 0]);   
   cnt = cnt+1;
end

figure;
plot(t,b_filtered(:,1),'r',t,b_filtered(:,2),'g',t,b_filtered(:,3),'b')
title('b field for filtered position...');
    
    

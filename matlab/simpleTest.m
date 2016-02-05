close all

l_mag = 0.015;
r_mag = 0.0025;

h = [1 0 0];  % for calcB
t = 0.05:0.001:0.15;
a = 0:0.001:pi;
% t = fliplr(t);
r = zeros(length(t),3);
r_N = zeros(length(t),3);
r_S = zeros(length(t),3);
r_con = zeros(length(t),1);
nu = [0 0 0];
for i = 1:length(t)
   r(i,:) = [0 t(i) 0];
   r_N(i,:) = [t(i)+(l_mag/2-r_mag) 0 0];
   r_S(i,:) = [t(i)+(r_mag-l_mag/2) 0 0];
   r_con(i) = t(i);
end

b = zeros(length(t),3);
b1 = zeros(length(t),3);
b_cyl = zeros(length(a),2);
b_con = zeros(length(t),3);

for i = 1:length(t)
    b(i,:) = calcB(nu,r(i,:),[1 0 0]);    
%     b1(i,:) = calcB(nu,r_S(i,:),h) - calcB(nu,r_N(i,:),h);

%     b_cyl(i,:) = calcB_cyl(0.06,-0.1+r_con(i));
%     b_cyl(i,:) = calcB_cyl(0,r_con(i));
%     b_cyl(i,:) = calcB_cyl([r_con(i) 0],0);
    
    b_con(i,:) = [calcB_1d(r_con(i),0.015) 0 0];
end

for i = 1:length(a)
    b_cyl(i,:) = calcB_cyl([r_con(1), 0], a(i));
end

% b_model = b;
% range_m = max(b(:,1)) - min(b(:,1));
% range_s = max(b_con) - min(b_con);
% scaleModel = range_s/range_m
% b_model = b_model(:,1)*(scaleModel);
% offsetModel = b_con(1) - b_model(1)
% b_model = b_model + offsetModel;

% fitting cylinder model
% b_model = b_cyl(:,2);
% range_m = max(b_model) - min(b_model);
% range_s = max(b_con) - min(b_con);
% scaleModel = range_s/range_m
% b_model = b_model*(scaleModel);
% offsetModel = b_con(1) - b_model(1)
% b_model = b_model + offsetModel;

c = 1:1:length(t);

% figure
% plot(c,b(:,1),'r',c,b(:,2),'g')
% title('B-field dipole - model[G]')

figure
plot(r_con,b_con(:,1))
title('B-field con[G]')

figure
plot(a,b_cyl(:,1),'r',a,b_cyl(:,2),'g')
title('B-field cyl')

% figure
% plot(r_con,b_model(:,1),'r',r_con,b_con(:,1),'g')
% title('B-field dipole - cyl FITTED[G]')

% dif = b_model(:,1)-b_con(:,1);
% figure
% plot(c,dif,'r')
% title('dif')
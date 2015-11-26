close all

t = 0:0.01:pi/2;

sInd = [-0.07, 0.0, -0.0];
sMid = [-0.071, -0.022, 0.024];
sRin = [-0.07, -0.022*2, -0.0];
sPin = [-0.07, -0.022*3, -0.0];

yInd = 0;
yMid = -0.022;
yRin = -0.022*2;
yPin = -0.022*3;
% s2 = [0,0,0];
% jointMid = [0,0,0];

phalInd = [0.03080, 0.02581, 0.01678];
phalMid = [0.03593, 0.03137, 0.01684];
phalRin = [0.03404, 0.02589, 0.01820];
phalPin = [0.02892, 0.02493, 0.01601];

% angles = zeros(length(t),3);
angles = zeros(length(t)*2,3);

cnt = 1;
for i = t
   angles(cnt,:) = [i 0 0];
   cnt = cnt+1;
end

t = fliplr(t);
cnt = 1;
for i = t
   angles(cnt+length(t),:) = [i 0 0];
   cnt = cnt+1;
end 

calcBFing = zeros(length(angles),3);
calcB_2 = zeros(length(angles),3);
pos = zeros(length(angles),3);
orien = zeros(length(angles),3);
r = zeros(length(angles),3);
cnt = 1;
for i = 1:length(angles)
   calcBFing(i,:) = angToB(angles(i,:),phalMid,sMid,yMid);
   pos(i,:) = angToP(angles(i,:),phalMid,yMid);
   orien(i,:) = angToH(angles(i,:));   
   r(i,:) = sMid-pos(i,:);
%    calcB_2(i,:) = calcB(r(i,:),orien(i,:));
end

c = 1:1:length(angles);
figure
plot(c,calcBFing(:,1),'r',c,calcBFing(:,2),'g',c,calcBFing(:,3),'b');
title('B-field (all in one fcn)')
% figure
% plot(c,calcB_2(:,1),'r',c,calcB_2(:,2),'g',c,calcB_2(:,3),'b');
% title('B-field')
figure
plot(c,pos(:,1),'r',c,pos(:,2),'g',c,pos(:,3),'b');
title('position')
figure
plot(c,r(:,1),'r',c,r(:,2),'g',c,r(:,3),'b');
title('R-vector')
figure
plot(c,orien(:,1),'r',c,orien(:,2),'g',c,orien(:,3),'b');
title('orientation')
% figure
% plot(c,angles(:,1),'r',c,angles(:,2),'g',c,angles(:,3),'b');
% title('angles')

%% acquiring the data...
% data = load('../python/151125_mid1');
% data(:,1)=[];
% % values for 151125_mid1
% scale = [0.54974468 0 1.27798783];
% offset = [125.74566767 0 71.2578344 ];
% 
% for i = 1:1:length(data)
%    data(i,:) = data(i,:).*scale+offset; 
% end
% 
% fitted = data(70:160,:);

%% estimation...
Aineq = [];
bineq = [];
Aeq = [];
beq = [];
lb = [0, 0, 0];
ub = [pi/2, pi/(180/110), pi/2];
optopt = optimoptions(@fmincon,'Algorithm','sqp');

% for the perfect B-field
estAng = zeros(length(angles),3);
fval = zeros(length(angles),3);
for i = 2:length(angles)
    f = @(angle)estBtoAng(angle,phalMid,sMid,calcBFing(i,:),yMid);
%     [estAng(i,:), fval(i,:)] = fminunc(f,estAng(i-1,:));
    [estAng(i,:), fval(i,:)] = fmincon(f,estAng(i-1,:),...
                            Aineq,bineq,Aeq,beq,lb,ub,[],optopt);
end

% for the measured values
% estAngMeas = zeros(length(fitted),3);
% fval = zeros(length(fitted),3);
% for i = 2:length(fitted)
%     f = @(angle)estBtoAng(angle,phalMid,sMid,fitted(i,:),yMid);
%     estAngMeas(i,:) = fmincon(f,estAngMeas(i-1,:),...
%                             Aineq,bineq,Aeq,beq,lb,ub,[],optopt);
% end

figure
plot(c,estAng(:,1),'r',c,estAng(:,2),'g',c,estAng(:,3),'b')
title('estimated Ang')
% u = 1:1:length(fitted);
% figure
% plot(u,estAngMeas(:,1),'r',u,estAngMeas(:,2),'g',u,estAngMeas(:,3),'b')
% title('estimated Ang')
% figure
% plot(u,fitted(:,1),'r',u,fitted(:,2),'g',u,fitted(:,3),'b')
% title('meas B')

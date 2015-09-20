% script for estimating 'perfect' position of 4 magnets and 4 sensors

%% 
% position values for wodden hand...
angInd =[0.02957 0.09138 0.01087];
angMid =[0.00920 0.09138 0.01087];
angRing=[-0.01117, 0.09138, 0.01087];
angPin =[-0.03154 0.09138 0.01087];

rInd =0.08;
rMid =0.08829;
rRing=0.07979;
rPin =0.07215;

sInd=[0.02957 0.06755 0.];
sMid=[0.00920 0.06755 0.];
sRin=[-0.01117 0.06755 0.];
sPin=[-0.03154 0.06755 0.];

t=0:0.01:0.5*pi;
index = zeros(3,length(t));
middle = zeros(3,length(t));
ring = zeros(3,length(t));
pinky = zeros(3,length(t));

%% 
% calculate all the finger positions
cnt=1;
for i = t
    index(:,cnt)=[angInd(1);
                    angInd(2)+rInd*cos(i);
                    angInd(3)+rInd*sin(i)];
    middle(:,cnt)=[angMid(1);
                    angInd(2)+rMid*cos(i);
                    angInd(3)+rMid*sin(i)];
    ring(:,cnt)=[angRing(1);
                    angInd(2)+rPin*cos(i);
                    angInd(3)+rPin*sin(i)];
    pinky(:,cnt)=[angPin(1);
                    angPin(2)+rPin*cos(i);
                    angPin(3)+rPin*sin(i)];
    cnt=cnt+1;   
end

%% 
% calculate all the (perfect) measured (cummulative) B-fields for the 4
% sensors
bInd=zeros(3,length(t));
bMid=zeros(3,length(t));
bRin=zeros(3,length(t));
bPin=zeros(3,length(t));

for i = 1:length(t)
   bInd(:,i)=evalfuncMag_sim(index(:,i),sInd')+...
             evalfuncMag_sim(middle(:,i),sInd')+...
             evalfuncMag_sim(ring(:,i),sInd')+...
             evalfuncMag_sim(pinky(:,i),sInd');
   
    bMid(:,i)=evalfuncMag_sim(index(:,i),sMid')+...
              evalfuncMag_sim(middle(:,i),sMid')+...
              evalfuncMag_sim(ring(:,i),sMid')+...
              evalfuncMag_sim(pinky(:,i),sMid');
          
    bRin(:,i)=evalfuncMag_sim(index(:,i),sRin')+...
              evalfuncMag_sim(middle(:,i),sRin')+...
              evalfuncMag_sim(ring(:,i),sRin')+...
              evalfuncMag_sim(pinky(:,i),sRin');
         
    bPin(:,i)=evalfuncMag_sim(index(:,i),sPin')+...
              evalfuncMag_sim(middle(:,i),sPin')+...
              evalfuncMag_sim(ring(:,i),sPin')+...
              evalfuncMag_sim(pinky(:,i),sPin');
end
disp('Finished calculating the artificial data')
%% 
% plot the things...
% figure
% subplot(1,4,1)
% plot(t,bInd(1,:),'-b',t,bInd(2,:),'-.b',t,bInd(3,:),':b')
% title('B-Field Index')
% subplot(1,4,2)
% plot(t,bMid(1,:),'-b',t,bMid(2,:),'-.b',t,bMid(3,:),':b')
% title('B-Field Middle')
% subplot(1,4,3)
% plot(t,bRin(1,:),'-b',t,bRin(2,:),'-.b',t,bRin(3,:),':b')
% title('B-Field Ring')
% subplot(1,4,4)
% plot(t,bPin(1,:),'-b',t,bPin(2,:),'-.b',t,bPin(3,:),':b')
% legend('x','y','z')
% title('B-Field Pinky')

%%
% estimating positions with fminunc

% preparing the matrices...
s = [sInd';     % version 1&2
    sMid';
    sRin';
    sPin'];
b = [bInd;      % version 1
    bMid;
    bRin;
    bPin];
% b = zeros(length(t)*4,3);   % version 2
% for i = 1:4:length(t)
%     b(i:i+3,:) = [bInd(:,i)';     
%                 bMid(:,i)';
%                 bRin(:,i)';
%                 bPin(:,i)'];
% end

estPos=zeros(12,length(t));     % version 1
estPos(:,1)=[index(:,1);        % version 1
            middle(:,1);
            ring(:,1);
            pinky(:,1)];
% estPos = zeros(4*length(t),3);  % version 2
% estPos(1:4,:)=[index(:,1)';
%                 middle(:,1)';
%                 ring(:,1)';
%                 pinky(:,1)'];

fval=zeros(1,length(t));
cnt=2;
% for unconstrained method
% options=optimoptions(@fminunc, 'Display','none','Algorithm','quasi-newton');  
% for constrained method
options=optimoptions(@fmincon,'Algorithm','sqp');  

% adding bounds
A = [];
b = [];
Aeq = [];
beq = [];
lb = [index(1)-0.04; index(2)-0.005; index(3)-0.005;...
        middle(1)-0.04; middle(2)-0.005; middle(3)-0.005;...
        ring(1)-0.04; ring(2)-0.005; ring(3)-0.005;...
        pinky(1)-0.04; pinky(2)-0.005; pinky(3)-0.005];        
ub = [index(1)+0.04; index(2)+rInd; index(3)+rInd;...
        middle(1)+0.04; middle(2)+rMid; middle(3)+rMid;...
        ring(1)+0.04; ring(2)+rRing; ring(3)+rRing;...
        pinky(1)+0.04; pinky(2)+rPin; pinky(3)+rPin];      

for i = b(:,2:end)  % version 1
% for i = 1:4:length(b)   % version 2
%     bEst = b(i:i+3,:);
    f = @(P)solfuncMagONE(P,s,i);   % version 1
%     f = @(P)solfuncMagONE(P,s,bEst);   % version 2
%     [estPos(:,cnt), fval(:,cnt)] = fminunc(f,estPos(:,cnt-1),options);      % unconstrained method
    [estPos(:,cnt), fval(:,cnt)] = fmincon(f,estPos(:,cnt-1),...
                                        A,b,Aeq,beq,lb,ub,options);    % constrained method
    text = ['Pos Nr ',num2str(cnt)];
    printmat(estPos(:,cnt),text, ... 
            'Index_x Index_y Index_z Middle_x Middle_y Middle_z Ring_x Ring_y Ring_z Pinky_x Pinky_y Pinky_z','');
    cnt=cnt+1;
end

%% 
% plotting the positions (version 1)
figure
grid on
subplot(2,2,1)
plot3(estPos(1,:),estPos(2,:),estPos(3,:),'r',...
        index(1,:),index(2,:),index(3,:),'g')
grid on
title('index')
xlabel('x [m]')
ylabel('y [m]')
zlabel('z [m]')

subplot(2,2,2)
plot3(estPos(4,:),estPos(5,:),estPos(6,:),'r',...
        middle(1,:),middle(2,:),middle(3,:),'g')
grid on
title('middle')
xlabel('x [m]')
ylabel('y [m]')
zlabel('z [m]')

subplot(2,2,3)
plot3(estPos(7,:),estPos(8,:),estPos(9,:),'r',...
        ring(1,:),ring(2,:),ring(3,:),'g')
grid on
title('ring')
xlabel('x [m]')
ylabel('y [m]')
zlabel('z [m]')

subplot(2,2,4)
plot3(estPos(10,:),estPos(11,:),estPos(12,:),'r',...
        pinky(1,:),pinky(2,:),pinky(3,:),'g')
grid on
title('ring')
xlabel('x [m]')
ylabel('y [m]')
zlabel('z [m]')


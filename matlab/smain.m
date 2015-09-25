% script for estimating 'perfect' position of 1 magnets and 1 sensor(index)


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

rTest = 0.08;

sInd=[0.02957 0.06755 0.];
sMid=[0.00920 0.06755 0.];
sRin=[-0.01117 0.06755 0.];
sPin=[-0.03154 0.06755 0.];

sTest=[1 2 3];

t = 0:0.01:0.5*pi;
ttest = (2+0):0.001:(2+0.1);

index = zeros(3,length(t));
middle = zeros(3,length(t));
ring = zeros(3,length(t));
pinky = zeros(3,length(t));

test = [1+zeros(1,length(ttest));
        ttest;
        3+zeros(1,length(ttest))];

%% 
% calculate all the finger positions
cnt=1;
for i = t
    index(:,cnt)=[angInd(1);
                    angInd(2)+rInd*cos(i);
                    angInd(3)+rInd*sin(i)];
    middle(:,cnt)=[angMid(1);
                    angMid(2)+rMid*cos(i);
                    angMid(3)+rMid*sin(i)];
    ring(:,cnt)=[angRing(1);
                    angRing(2)+rPin*cos(i);
                    angRing(3)+rPin*sin(i)];
    pinky(:,cnt)=[angPin(1);
                    angPin(2)+rPin*cos(i);
                    angPin(3)+rPin*sin(i)];
             
    cnt=cnt+1;   
end

%% calculate all the (perfect) measured B-fields 
bInd=zeros(3,length(t));
bRin=zeros(3,length(t));
bMid=zeros(3,length(t));
bPin=zeros(3,length(t));

% bTest=zeros(3,length(t));
% bTest2=zeros(3,length(t));
H=zeros(3,length(t));
R=zeros(3,length(t));

for i = 1:length(t)
   bInd(:,i)=evalfuncMag_sim(index(:,i),sInd');
   bMid(:,i)=evalfuncMag_sim(middle(:,i),sMid');
   bRin(:,i)=evalfuncMag_sim(ring(:,i),sRin');
   bPin(:,i)=evalfuncMag_sim(pinky(:,i),sPin');
   
%    bTest(:,i)=evalfuncMag_sim(test(:,i),sTest');
%    H(:,i)=test(:,i)-sTest';
%    R(:,i)=sTest'-test(:,i);   
end

bTest = zeros(3,length(ttest));
for i = 1:length(ttest)
    bTest(:,i)=evalfuncMag_sim(test(:,i),sTest');
end

% calculating H and R by myself...
% H = H*-1;
% row2=H(2,:);
% row3=H(3,:);
% H(2,:)=row3;
% H(3,:)=row2;
% for i = 1:length(t)
%     bTest2(:,i)=evalfuncMag_HR(H(:,i),R(:,i));
% end

% figure
% plot(t,R(1,:),'r',t,R(2,:),'g',t,R(3,:),'b')
% title('R')
% legend('x','y','z')
% 
% figure
% plot(t,H(1,:),'r',t,H(2,:),'g',t,H(3,:),'b')
% title('H')
% legend('x','y','z')

figure
plot(ttest,bTest(1,:),'r',ttest,bTest(2,:),'g',ttest,bTest(3,:),'b')
title('b')
legend('bx','by','bz')
% figure
% plot(t,bTest2(1,:),'r',t,bTest2(2,:),'g',t,bTest2(3,:),'b')
% title('b2')
% legend('bx','by','bz')
%% estimate the positions with fminunc
% estPos=zeros(3,length(t));
% estPos(:,1)=index(:,1);
% estPos=zeros(3,length(ttest));
% estPos(:,1)=test(:,1);
% fval=zeros(1,length(ttest));
% fval=zeros(1,length(t));
% cnt=2;
% options=optimoptions(@fminunc, 'Display','none','Algorithm','quasi-newton');
% % adding bounds
% % Aineq = [];
% % bineq = [];
% % Aeq = [];
% % beq = [];
% % lb = [index(1)-0.004; index(2)-0.005; index(3)-0.005];        
% % ub = [index(1)+0.004; index(2)+rInd+0.005; index(3)+rInd+0.005];      
% 
% for i = bTest(:,2:end)
% f = @(P)sobjFun(P,sInd',i);
% f = @(P)sobjFun(P,sTest',i);
% [estPos(:,cnt), fval(:,cnt)] = fminunc(f,estPos(:,cnt-1));
% cnt=cnt+1;
% end
% 
% %% plotting stuff...
% subplot(2,2,1)
% plot(t,index(1,:),'-b',t,index(2,:),'-.b',t,index(3,:),':b')
% title('Index')
% subplot(2,2,2)
% plot(t,estPos(1,:),'-b',t,estPos(2,:),'-.b',t,estPos(3,:),':b')
% title('estimated')
% subplot(2,2,3)
% plot(t,bInd(1,:),t,bInd(2,:),t,bInd(3,:))
% subplot(2,2,4)
% plot3(estPos(1,:),estPos(2,:),estPos(3,:),'g',index(1,:),index(2,:),index(3,:),'r')
% grid on
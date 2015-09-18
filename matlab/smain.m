% script for estimating 'perfect' position of 1 magnets and 1 sensor(index)


%% position values for wodden hand...
%
angInd =[0.02957 0.09138 0.01087];

rInd =0.08;

sInd=[0.02957 0.06755 0.];

t=0:0.01:0.5*pi;
index = zeros(3,length(t));

% calculate all the finger positions
cnt=1;
for i = t
    index(:,cnt)=[angInd(1);
                    angInd(2)+rInd*cos(i);
                    angInd(3)+rInd*sin(i)];
    
    cnt=cnt+1;   
end

%% calculate all the (perfect) measured B-fields 
bInd=zeros(3,length(t));

for i = 1:length(t)
   bInd(:,i)=evalfuncMag_sim(index(:,i),sInd');
end


%% estimate the positions with fminunc
estPos=zeros(3,length(t));
estPos(:,1)=index(:,1);
fval=zeros(1,length(t));
cnt=2;
options=optimoptions(@fminunc, 'Display','none','Algorithm','quasi-newton');
for i = bInd(:,2:end)
f = @(P)sobjFun(P,sInd',i);
[estPos(:,cnt), fval(:,cnt)] = fminunc(f,estPos(:,cnt-1),options);
cnt=cnt+1;
end

%% plotting stuff...

subplot(2,2,1)
plot(t,index(1,:),'-b',t,index(2,:),'-.b',t,index(3,:),':b')
title('Index')
subplot(2,2,2)
plot(t,estPos(1,:),'-b',t,estPos(2,:),'-.b',t,estPos(3,:),':b')
title('estimated')
subplot(2,2,3)
plot(t,fval)
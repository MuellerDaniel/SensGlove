% script for estimating 'perfect' position of 4 magnets and 4 sensors

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

% calculate all the finger positions
cnt=1;
for i = t
    index(:,cnt)=[angInd(1);
                    angInd(2)+rInd*cos(i);
                    angInd(3)+rInd*sin(i)];
    middle(:,cnt)=[angInd(1);
                    angInd(2)+rMid*cos(i);
                    angInd(3)+rMid*sin(i)];
    ring(:,cnt)=[angInd(1);
                    angInd(2)+rPin*cos(i);
                    angInd(3)+rPin*sin(i)];
    pinky(:,cnt)=[angPin(1);
                    angPin(2)+rPin*cos(i);
                    angPin(3)+rPin*sin(i)];
    cnt=cnt+1;   
end

% calculate all the (perfect) measured B-fields
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

% plot the things...
figure
subplot(1,4,1)
plot(t,bInd(1,:),'-b',t,bInd(2,:),'-.b',t,bInd(3,:),':b')
title('Index')
subplot(1,4,2)
plot(t,bMid(1,:),'-b',t,bMid(2,:),'-.b',t,bMid(3,:),':b')
title('Middle')
subplot(1,4,3)
plot(t,bRin(1,:),'-b',t,bRin(2,:),'-.b',t,bRin(3,:),':b')
title('Ring')
subplot(1,4,4)
plot(t,bPin(1,:),'-b',t,bPin(2,:),'-.b',t,bPin(3,:),':b')
legend('x','y','z')
title('Pinky')
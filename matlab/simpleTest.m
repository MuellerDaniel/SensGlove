close all

% h = [pi/2 pi/2 0];  % for calcB_lect
h = [1 0 0];  % for calcB
t = 0.05:0.001:0.15;
tr = fliplr(t);
r = zeros(length(t),3);
r_con = zeros(length(t),1);
for i = 1:length(t)
   r(i,:) = [t(i)+0.015/2 0 0.0025/2]; % for calcB h = [1 0 0]
%    r(i,:) = [t(i)+0.0025/2 0 -0.015/2]; % for calcB h = [0 0 1]
%    r(i,:) = [t(i) 0 0];
%    r(i,:) = [0 0 t(i)]; % for calcB_lect
   r_con(i) = t(i);
end

b = zeros(length(t),3);
b1 = zeros(length(t),3);
b1r = zeros(length(t),3);
b2 = zeros(length(t),3);
b_con = zeros(length(t),3);

for i = 1:length(t)
    b(i,:) = calcB(r(i,:),h);
%     b(i,:) = calcB(r(i,:),h);
%     b1(i,:) = calcB(r(i,:)+[0.015/2 0.0025/2 0],h);    % this version I would take...
%     b1r(i,:) = calcB(r(i,:)+[0.015/2 0.0025/2 0.0025/2],h);
%     b2(i,:) = calcB(r(i,:)+[0 0.015/2 0],h);
%     b(i,:) = calcB_lect(r(i,:)+[0 0 0.015/2],0.015,h);
    b_con(i,:) = [calcB_1d2(r_con(i),0.015) 0 0];
end

factor = b(1)/b_con(1)
% factor = 260.7851;
b(:,1) = b(:,1)*factor^-1;
b(:,2) = b(:,2)*factor^-1;
b(:,3) = b(:,3)*factor^-1;


c = 1:1:length(t);
figure
plot(c,b(:,1),'r',c,b_con(:,1),'g');
title('B-field compared')

figure
plot(c,b(:,1),'r',c,b(:,2),'g',c,b(:,3),'b');
title('B-field whole b') 


% figure
% plot(c,b1(:,1),'r',c,b_con(:,1),'g');
% title('B-field whole b1')
% figure
% plot(c,b1r(:,1),'r',c,b_con(:,1),'g');
% title('B-field reverse')
% figure
% plot(c,b2(:,1),'r',c,b2(:,2),'g',c,b2(:,3),'b');
% title('B-field whole b2')

% figure
% plot(c,b(:,1))
% title('B-field [G]')
figure
plot(c,b_con(:,1))
title('B-field con[G]')

dif = b(:,1)-b_con(:,1);
figure
plot(c,(b(:,1)-b_con(:,1)),'r')
title('dif')
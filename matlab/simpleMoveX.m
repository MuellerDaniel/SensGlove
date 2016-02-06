%%  VERIFYING THAT STH IS WRONG WITH MY MODEL...    
close all

r = 0.07:0.00125:0.17;
% r = 0.05:0.001:0.07;
% r2 = 0.07:0.001:0.1;
p = [0 0 0];
h = [1 0 0];
ang = 0;
l_mag = 0.015;
r_mag = 0.0025;

%% calculating the b-field

b_dip = zeros(length(r),3);
b_cyl = zeros(length(r),3);
b_simple = zeros(length(r),1);
% b_model = zeros(length(r)+25+length(r2),3);
% b_model2 = zeros(length(r)+25+length(r2),3);
% b_simple = zeros(length(r)+25+length(r2),1);

for i = 1:length(r)
%     b_model1(i,:) = calcB(p-[r(i) 0 0],h);    % fixed orientation
%     b_model2(i,:) = calcB(p-[r(i)+l_mag/2 0 0],h);    % fixed orientation
%     b_model3(i,:) = calcB(p-[r(i)+l_mag 0 0],h);    % fixed orientation
%     b_model1(i,:) = calcB(p-[r(i)+l_mag/2 0 0],h);
    b_dip(i,:) = calcB_dip([r(i) 0 0],h);
    b_cyl(i,:) = calcB_cyl([r(i) 0],ang);
    b_simple(i) = calcB_1d(r(i));     % simple approach
end

% for i = 1:25
%    b_model(i+length(r),:) = calcB(p,[r(end)+l_mag*0.5 0 0],h);
%    b_model2(i+length(r),:) = calcB(p,[r(end) 0 0],h);
%    b_simple(i+length(r)) = calcB_1d2(r(end),l_mag);
% end
% 
% for i = 1:length(r2)
%     b_model(i+length(r)+25,:) = calcB(p,[r2(i)+l_mag*0.5 0 0],h);    % fixed orientation
%     b_model2(i+length(r)+25,:) = calcB(p,[r2(i) 0 0],h);
%     b_simple(i+length(r)+25) = calcB_1d2(r2(i),l_mag);     % simple approach
% end

%% the measured b-field
meas = importdata('../python/151216_xMove2');
meas(:,1) = [];
meas = meas*0.001;

%% fitting

% fit model to simple
% range_m = max(b_model(:,1)) - min(b_model(:,1));
% range_s = max(b_simple) - min(b_simple);
% scaleModel = range_s/range_m
% b_model = b_model(:,1)*scaleModel;
% offsetModel = b_simple(1) - b_model(1)
% b_model = b_model + offsetModel;

% range_m = max(b_model1(:,1)) - min(b_model1(:,1));
% range_s = max(b_simple) - min(b_simple);
% scale = range_s/range_m
% b_m_fit1 = b_model1(:,1)*scale;
% offset = b_simple(1) - b_m_fit1(1)
% b_m_fit1 = b_m_fit1 + offset;

% range_m = max(b_model2(:,1)) - min(b_model2(:,1));
% range_s = max(b_simple) - min(b_simple);
% scale = range_s/range_m
% b_m_fit2 = b_model2(:,1)*scale;
% offset = b_simple(1) - b_m_fit2(1)
% b_m_fit2 = b_m_fit2 + offset;
% 
% range_m = max(b_model3(:,1)) - min(b_model3(:,1));
% range_s = max(b_simple) - min(b_simple);
% scale = range_s/range_m
% b_m_fit3 = b_model3(:,1)*scale;
% offset = b_simple(1) - b_m_fit3(1)
% b_m_fit3 = b_m_fit3 + offset;

% fit simple to model
% range_m = max(b_model(:,1)) - min(b_model(:,1));
% range_s = max(b_simple) - min(b_simple);
% scaleModel = range_m/range_s
% b_simple = b_simple(:,1)*scaleModel;
% offsetModel = b_model(1) - b_simple(1)
% b_simple = b_simple + offsetModel;

% fit meas to model
% range_m = max(meas(:,1)) - min(meas(:,1));
% range_s = max(b_model) - min(b_model);
% scaleMeas = range_s/range_m
% meas = meas(:,1)*scaleMeas;
% offsetMeas = b_model(1) - meas(1)
% meas = meas + offsetMeas;

% fit meas to simple
% range_m = max(meas(:,1)) - min(meas(:,1));
% range_s = max(b_simple) - min(b_simple);
% scaleMeas = range_s/range_m
% meas = meas(:,1)*scaleMeas;
% offsetMeas = b_simple(1) - meas(1)
% meas = meas + offsetMeas;



%% plotting
close all

% a = 1:1:(length(r)+25+length(r2));
a = r;

figure
plot(a,b_cyl(:,1),'r',a,b_cyl(:,2),'g',a,b_cyl(:,3),'b')
title('cylindrical model')

figure
plot(a,b_dip(:,1),'r',a,b_dip(:,2),'g',a,b_dip(:,3),'b')
title('dipole model')

figure
plot(a,b_dip(:,1),'r',a,b_cyl(:,1),'g')
title('dip vs cyl')

% figure
% plot(a,b_simple(:,1),'r')
% title('flat model')



% figure
% plot(a,b_model2(:,1),'r',a,b_model(:,1),'g',a,b_simple,'b')
% title('other approach...')

% figure
% plot(r,b_model1(:,1),'r',r,b_model1(:,2),'g',r,b_model1(:,3),'b')
% plot(a,b_model(:,1),'r',a,b_model(:,2),'g',a,b_model(:,3),'b')
% title('Model unscaled')
% figure
% % plot(r,b_simple,'r',r,b_m_fit1,'g',r,b_m_fit2,'b',r,b_m_fit3,'y')
% plot(a,b_simple,'r',a,b_m_fit,'g')
% plot(a,b_simple,'r',a,b_model(:,1),'g')
% title('Model scaled')
% ylabel('B-field [G]')

% b_m_fit1 = b_m_fit;

% dif1 = zeros(length(a),1);
% dif1(:,1) = abs(b_m_fit1-b_simple);
% maxDif1 = max(dif1)
% dif2 = zeros(length(r),1);
% dif2(:,1) = abs(b_m_fit2-b_simple);
% maxDif2 = max(dif2)
% dif3 = zeros(length(r),1);
% dif3(:,1) = abs(b_m_fit3-b_simple);
% maxDif3 = max(dif3)

% figure
% plot(r,dif1,'r',r,dif2,'g',r,dif3,'b')
% legend('origin at north pole','origin at centre','origin at south pole')
% % plot(a,dif,'r')
% title('Difference between dipole field and bar magnet field')
% xlabel('Distance to magnetic sensor [m]')
% ylabel('Difference [G]')

% figure
% plot(a(1:end-1),meas(:,1),'r',a(1:end-1),b_model(1:end-1,1),'g',a(1:end-1),b_simple(1:end-1,1),'b')%,1:1:length(meas),meas(:,2),1:1:length(meas),meas(:,3))
% title('Measured vs Model')
% ylabel('B-field [G]')
% xlabel('distance in x-direction [m]')

%% estimation

% b_model = b_model(1:end-1,:);
% % a = a(1:end-1);
% a = 1:1:length(a(1:end-1));
% 
% estPosModel = zeros(length(b_model),3);
% estPosModel(1,:) = [0.05+l_mag/2 0 0];
% estPosMeas = zeros(length(meas),3);
% estPosMeas(1,:) = [0.05+l_mag/2 0 0];
% % estPosModel_simple = zeros(length(b_simple),3);
% % estPosModel_simple(1,:) = [0.05 0 0];
% 
% Aineq = [];
% bineq = [];
% Aeq = [];
% beq = [];
% lb = [0.04, 0, 0];
% ub = [0.2, 0, 0];
% optopt = optimoptions(@fmincon,'Algorithm','sqp');
% 
% % % the perfect values
% for i = 2:length(b_model)    
%     fModel = @(pos)estimateB_flat(p,pos,h,b_model(i));    
% %     estPosModel(i,:) = fminunc(fModel,estPosModel(i-1,:)); 
%     estPosModel(i,:) = fmincon(fModel,estPosModel(i-1,:),...
%                         Aineq,bineq,Aeq,beq,lb,ub,[],optopt);
% end
% % 
% % % % the bar magnet values
% % % % for i = 2:length(b_simple)    
% % % %     fModel = @(pos)estimateB_flat(pos,h,b_simple(i));    
% % % % %     estPosModel(i,:) = fminunc(fModel,estPosModel(i-1,:)); 
% % % %     estPosModel_simple(i,:) = fmincon(fModel,estPosModel_simple(i-1,:),...
% % % %                         Aineq,bineq,Aeq,beq,lb,ub,[],optopt);
% % % % end
% % % 
% % % the measured values
% for i = 2:length(meas)
%    fMeas = @(pos)estimateB_flat(p,pos,h,meas(i));
% %    estPosMeas(i,:) = fminunc(fMeas,estPosMeas(i-1,:));
%     estPosMeas(i,:) = fmincon(fMeas,estPosMeas(i-1,:),...
%                         Aineq,bineq,Aeq,beq,lb,ub,[],optopt);
% end
% 
% figure
% plot(a,estPosMeas(:,1),'r',a,estPosModel(:,1),'g')
% title('estPosMeas vs estPosModel')

% figure
% plot(a,estPosModel(:,1),'r',a,estPosModel(:,2),'g',a,estPosModel(:,3),'b')
% title('estPosModel')
% 
% % figure
% % plot(a,estPosModel_simple(:,1),'r',a,estPosModel_simple(:,2),'g',a,estPosModel_simple(:,3),'b')
% % title('estPosModel_simple')
% 
% figure
% plot(1:1:length(meas),estPosMeas(:,1),'r',...
%         1:1:length(meas),estPosMeas(:,2),'g',...
%         1:1:length(meas),estPosMeas(:,3),'b')
% title('estPosMeas')


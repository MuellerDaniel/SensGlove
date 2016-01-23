%% script for comparing the results for magneto calibration
clc
clear
close all

%% read in the datasets
d0 = load('160111_calData0');
d0 = d0(:,2:end);
d1 = load('160111_calData1');
d1 = d1(:,2:end);
d2 = load('160111_calData2');
d2 = d2(:,2:end);
dc = load('160115_caliWaving');
dc = dc(:,2:end);

%% offset scale approach (github page)

disp('dataset 160111_calData0');
[d0_off, d0_soft, d0_radii, d0_git] = calcHardSoft(d0);
[beta_d0, off_d0, geo_d0, d0_free] = caliFreescale(d0);
fprintf('\n\n');
disp('dataset 160111_calData1');
[d1_off, d1_soft, d1_radii,d1_git] = calcHardSoft(d1);
[beta_d1, off_d1, geo_d1, d1_free] = caliFreescale(d1);
fprintf('\n\n');
disp('dataset 160111_calData2');
[d2_off, d2_soft, d2_radii, d2_git] = calcHardSoft(d2);
[beta_d2, off_d2, geo_d2, d2_free] = caliFreescale(d2);
fprintf('\n\n');
disp('dataset 160115_caliWaving');
[dc_off, dc_soft, dc_radii, dc_git] = calcHardSoft(dc);
[beta_dc, off_dc, geo_dc, dc_free] = caliFreescale(dc);


% setting them into relations...
maxValues = [max(d0(:,1)) max(d0(:,2)) max(d0(:,3));
            max(d1(:,1)) max(d1(:,2)) max(d1(:,3));
            max(d2(:,1)) max(d2(:,2)) max(d2(:,3))];
        
rangeMax = [max(maxValues(:,1))-min(maxValues(:,1))
            max(maxValues(:,2))-min(maxValues(:,2))
            max(maxValues(:,3))-min(maxValues(:,3))];
        
meanMax = [mean(maxValues(:,1)) mean(maxValues(:,2)) mean(maxValues(:,3))];

devMax = (rangeMax./meanMax').*100;
disp('max deviation from uncalibrated max-values [%]');
disp(devMax);
  
minValues = [min(d0(:,1)) min(d0(:,2)) min(d0(:,3));
            min(d1(:,1)) min(d1(:,2)) min(d1(:,3));
            min(d2(:,1)) min(d2(:,2)) min(d2(:,3))];

rangeMin = [max(minValues(:,1))-min(minValues(:,1))
            max(minValues(:,2))-min(minValues(:,2))
            max(minValues(:,3))-min(minValues(:,3))];

meanMin = [mean(minValues(:,1)) mean(minValues(:,2)) mean(minValues(:,3))];

devMin = (rangeMin./meanMin').*100;
disp('max deviation from uncalibrated min-values [%]');
disp(devMin);
    
        
        
%% visualizing the results

% % compared with raw data
% [ex,ey,ez]= ellipsoid(d0_off(1),d0_off(2),d0_off(3),...
%                         d0_scale(1),d0_scale(2),d0_scale(3),100);    
% figure
% surf(ex,ey,ez)
% % h = surf(ex,ey,ez);
% % colormap([1 0 1 ; 1 0 1])
% % alpha(h,0.1);
% hold on
% % plot3(d0_git(:,1),d0_git(:,2),d0_git(:,3),'b.')
% % plot3(d0_free(:,1),d0_free(:,2),d0_free(:,3),'r.')
% axis equal
% xlabel('x')
% title('raw ellips vs scaled meas')


%% ellipsoid centered; radi by scale factors
% compared with full scaled datapoints


figure
r = sum(d2_radii)/3;
% sphere with same radii
[s_ex,s_ey,s_ez]= ellipsoid(0,0,0,...
                    r,r,r,100);
h = surf(s_ex,s_ey,s_ez,'Linestyle','none');
colormap([1 1 0 ; 1 1 0])
alpha(h,0.5);

hold all

% scaled data points...
plot3(d2_git(:,1),d2_git(:,2),d2_git(:,3),'b.')
plot3(d2_free(:,1),d2_free(:,2),d2_free(:,3),'r.')
legend('centered ellipsoid, avgRadii','hard-soft-fit','Freescale fit');
axis equal
grid on
xlabel('x')
ylabel('y')
title('centered')

%% unscaled data points vs fitted ellipsoid

figure
r = sum(d2_radii)/3;
% sphere with same radii
[s_ex,s_ey,s_ez]= ellipsoid(0,0,0,...
                    r,r,r,100);
h = surf(s_ex,s_ey,s_ez,'Linestyle','none');
colormap([1 1 0 ; 1 1 0])
alpha(h,0.5);

hold all

plot3(d2(:,1),d2(:,2),d2(:,3),'b.')
legend('centered ellipsoid, avgRadii','raw datapoints');
axis equal
grid on
xlabel('x')
ylabel('y')
title('unscaled data vs centered ellipsoid')

%% scaled vs unscaled ellipsoid
r = sum(d2_radii)/3;
figure

[s_ex,s_ey,s_ez]= ellipsoid(0,0,0,...
                    d2_radii(1),d2_radii(2),d2_radii(3),100);
%                     r,r,r,100);
h1 = surf(s_ex,s_ey,s_ez,'Linestyle','none');
% colormap([1 1 0 ; 1 1 0])
set(h1,'Facecolor', [1 0 0]);
alpha(h1,0.5);

hold all

[ex,ey,ez]= ellipsoid(0,0,0,...
                    geo_d2,geo_d2,geo_d2,100);
h2 = surf(ex,ey,ez,'Linestyle','none');
set(h2,'Facecolor', [0 0 1]);
% colormap([0 1 0 ; 0 1 0])
alpha(h2,0.5);

legend('hard-soft-fit', 'Freescale fit');
axis equal
grid on
xlabel('x')
ylabel('y')
title('hard-soft vs freescale ellipsoid')                


%% difference of hard-soft and Freescale

delta = d2_git-d2_free;

figure

plot(delta(:,1));
hold on
plot(delta(:,2));
hold on
plot(delta(:,3));
grid on
title('delta');

%%

figure
r = sum(dc_radii)/3;
% sphere with same radii
[s_ex,s_ey,s_ez]= ellipsoid(0,0,0,...
                    r,r,r,100);
h = surf(s_ex,s_ey,s_ez,'Linestyle','none');
colormap([1 1 0 ; 1 1 0])
alpha(h,0.5);

hold all

% scaled data points...
plot3(dc(:,1),dc(:,2),dc(:,3),'b.')
plot3(dc_free(:,1),dc_free(:,2),dc_free(:,3),'r.')
legend('SCALED DATA centered ellipsoid, radi=geo_dc','un-fit','Freescale fit');
axis equal
grid on
xlabel('x')
ylabel('y')
title('centered')



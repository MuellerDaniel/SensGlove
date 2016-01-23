function [hard,soft, radii, data_scaled] = calcHardSoft(data)
%% TODO
% pack it in a proper m-file... where you acquire the data and then call
% the calcHardSoft and the hardFreescale function...

maxX = max(data(:,1));
minX = min(data(:,1));
maxY = max(data(:,2));
minY = min(data(:,2));
maxZ = max(data(:,3));
minZ = min(data(:,3));

hard = [(maxX+minX)/2 (maxY+minY)/2 (maxZ+minZ)/2];
disp('hard iron offset:');
disp(hard);

scaleX = (maxX-minX)/2;
scaleY = (maxY-minY)/2;
scaleZ = (maxZ-minZ)/2;

radii = [scaleX scaleY scaleZ];

avgRad = (scaleX+scaleY+scaleZ)/3;

disp('avg radius: ');
disp( avgRad);

soft = [avgRad/scaleX avgRad/scaleY avgRad/scaleZ];
disp('soft iron scale factor:');
disp(soft);

% to show that the impact of the soft iron effects is small...
% disp('impact of soft iron scale [%]:');   
% disp((1.-soft).*100);

tmp = zeros(length(data),3);
% data_off = zeros(length(data),3);
% hardFreescale = [25.6589927994 -13.3991186727 -80.52266039];
for i = 1:length(data)
   tmp(i,:) =  (data(i,:)-hard).*soft;
%    data_off(i,:) = (data(i,:)-hardFreescale);
end

data_scaled = tmp;
%% TODO 
% make a nice visualization with the raw values (perhaps the one below is
% already sufficient...)


                    
%% ellipsoid shifted by hard offsets, radi by scale factors
% compared with raw data
% [ex,ey,ez]= ellipsoid(hard(1),hard(2),hard(3),...
%                         scaleX,scaleY,scaleZ,100);    
% figure
% surf(ex,ey,ez)
% h = surf(ex,ey,ez,'Linestyle','none');
% %colormap([1 1 1 ; 1 1 1])
% alpha(h,0.5);
% hold on
% % raw data points...
% plot3(data(:,1),data(:,2),data(:,3),'b.')
% axis equal
% xlabel('x')
% title('shifted')


%% ellipsoid centered; radi by scale factors
% compared with full scaled datapoints
% [ex,ey,ez]= ellipsoid(0,0,0,...
%                         scaleX,scaleY,scaleZ,100);   
% figure
% surf(ex,ey,ez)
% h = surf(ex,ey,ez,'Linestyle','none');
% %colormap([1 1 1 ; 1 1 1])
% alpha(h,0.5);
% hold on
% % scaled data points...
% plot3(data_scaled(:,1),data_scaled(:,2),data_scaled(:,3),'b.')
% plot3(data_off(:,1),data_off(:,2),data_off(:,3),'r.')
% axis equal
% xlabel('x')
% title('centered')

%% centered sphere with radius avgRad
% full scaled datapoints
% figure
% [x,y,z] = sphere;
% x = avgRad*x;
% y = avgRad*y;
% z = avgRad*z;
% surf(x,y,z)
% h = surf(ex,ey,ez,'Linestyle','none');
% colormap([1 1 1; 1 1 1])
% alpha(h,0.5);
% hold on
% % data points...
% plot3(data_scaled(:,1),data_scaled(:,2),data_scaled(:,3),'b.')
% plot3(data_off(:,1),data_off(:,2),data_off(:,3),'r.')
% axis equal
% xlabel('x')
% title('sphere')

%% centered sphere vs centered ellipsoid
% figure
% [x,y,z] = sphere(90);
% x = avgRad*x;
% y = avgRad*y;
% z = avgRad*z;
% surf(x,y,z)
% h = surf(x,y,z,'Linestyle','none');
% colormap([0 1 1; 0 1 1]);
% alpha(h,0.5);
% hold on
% % ellipsoid...
% %[ex,ey,ez]= ellipsoid(hard(1),hard(2),hard(3),...
% [ex,ey,ez]= ellipsoid(0,0,0,...
%                         scaleX,scaleY,scaleZ,90);                    
%                     
% surf(ex,ey,ez)
% h = surf(ex,ey,ez,'Linestyle','none');
% colormap([1 1 0; 1 1 0]);
% % alpha(h,0.5);
% % data points scaled
% % plot3(data_scaled(:,1),data_scaled(:,2),data_scaled(:,3),'b.')
% % plot3(data_off(:,1),data_off(:,2),data_off(:,3),'r.')
% axis equal
% xlabel('x')
% title('sphere vs ellipsoid')





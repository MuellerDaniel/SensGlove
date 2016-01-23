function [beta, offFree, geomag, data_scaled] = caliFreescale(data)

Y = zeros(length(data),1);

cnt = 1;
for r = data'
    t = 0;
    for c = r'
        t = t+c^2;
    end
    Y(cnt) = t;   
    cnt = cnt+1;
end
% disp(size(Y));
X = [data ones(length(data),1)];
% disp(size(X));

beta = ((X'*X)^-1)*X'*Y;

offFree = [0.5*beta(1) 0.5*beta(2) 0.5*beta(3)];
disp('off freescale:');
disp(offFree);


geomag = sqrt(beta(4)+offFree(1)^2+offFree(2)^2+offFree(3)^2);
disp('geomag B');
disp(geomag);

tmp = data;
for i = 1:length(data)
    tmp(i,:) = tmp(i,:)-offFree;
    cnt = cnt+1;
end

data_scaled = tmp;




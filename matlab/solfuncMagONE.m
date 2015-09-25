function m = solfuncMagONE(P,S,B)
%%  
% advanced approach...
F = zeros(length(S),length(P)/3);   % version 1 F.shape(12x4)
% F = zeros(length(S)/3,length(P));   % version 2 F.shape(4x12)

% cnt=1;      % version 2
for i = 1:3:length(S)
   for j = 1:3:length(P)
       F(i:i+2,j) = evalfuncMag_sim(P(j:j+2),S(i:i+2));     % version 1
%        F(cnt,j:j+2) = evalfuncMag_sim(P(j:j+2),S(i:i+2))';     % version 2
   end
%    cnt=cnt+1;       % version 2
end
% printmat(F)
m = norm((eye(length(S))-F*pinv(F))*B);   % version 1
% m = norm((eye(length(S)/3)-F*pinv(F))*B);  % version 2

%%
% straight forward approach
% F = zeros(length(S),1);
% for i = 1:3:length(S)
%     for j = 1:3:length(P)
%         F(i:i+2,:) = F(i:i+2,:) + evalfuncMag_sim(P(j:j+2),S(i:i+2));
%     end
% end
% % printmat(F);
% m = (B - F);

function m = solfuncMagONE(P,S,B)
% H = P-S;
% R = S-P;
% factor = -1;
F = zeros(length(S),length(P)/3);   % version 1
% F = zeros(length(S)/3,length(P));   % version 2

for i = 1:(length(S)/3)
   for j = 1:(length(P)/3 )
       F(i:i+2,j) = evalfuncMag_sim(P(j:j+2),S(i:i+2));     % version 1
%        F(i,j:j+2) = evalfuncMag_sim(P(j:j+2),S(i:i+2)';     % version 2
   end
end

m = norm((eye(length(S))-F*pinv(F))*B);   % version 1
% m = norm(ident(length(S)/3)-F*pinv(F))*B);  % version 2
% m = F;
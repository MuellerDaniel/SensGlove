function c = cel(kc,p,c,s)
% kc
% p
% c
% s
if kc == 0
   c = nanM;
end

% # errtol = 1.0e-6;
errtol = 1.0e-6;
k = abs(kc);
em = 1.0;

if p > 0
    p = sqrt(p);
    s = s/p;
else
    f = kc^2;
    q = (1-f)*(s-c*p);
    g = 1-p;
    f = f-p;
    p = sqrt(f/g);
    c = (c-s)/g;
    s = -q/((g^2)*p)+c*p;
end    

f = c;
c = c+(s/p);
s = 2*(s+f*k/p);
p = p+k/p;
g = em;
em = em+k;
kk = k;


while abs(g-k) > (g*errtol)
   k = 2*np.sqrt(kk);
   kk = k*em;
   f = c;
   c = c+(s/p);
   s = 2*(s+f*kk/p);
   p = kk/p+p;
   g = em;
   em = k+em;
end

   

c = (pi/2)*(s+c*em)/(em*(em+p));


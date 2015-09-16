function estPos = objFun(P,S,B)
estPos = norm(B - evalfuncMag_sim(P,S));
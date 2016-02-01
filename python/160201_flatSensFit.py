import numpy as np
import modelDip as modD
import modelCyl as modC
import plotting as plo
import matplotlib.pyplot as plt


''' simulation of perfect data '''
l_mag = 0.015
r_mag = 0.0025

h0  = np.array([1.,0.,0.])
h90 = np.array([0.,1.,0.])

# s0 is the origin
s0 = np.array([0.,  0.,   0.])
s1 = np.array([0., -0.02, 0.])
s2 = np.array([0., -0.04, 0.])
s3 = np.array([0., -0.06, 0.])

zOff = np.array([0., 0., -0.02])

r = np.arange(0.04, 0.1, 0.001)

p_dip = np.zeros((len(r),3))

cnt = 0
for i in r:
    p_dip[cnt] = np.array([i, -0.02, 0.])
    
    cnt += 1
#plo.plotter2d((p_dip,),("p",))

b_dip0 = np.zeros((len(r),3))    
b_dip1 = np.zeros((len(r),3))    
b_dip2 = np.zeros((len(r),3))    
b_dip3 = np.zeros((len(r),3))    
b_cyl0 = np.zeros((len(r),3))    
b_cyl1 = np.zeros((len(r),3))    
b_cyl2 = np.zeros((len(r),3))    
b_cyl3 = np.zeros((len(r),3))  

cnt = 0
for i in p_dip:
    b_dip0[cnt] = modD.calcB(i-(s0+zOff), h0)
    b_dip1[cnt] = modD.calcB(i-(s1+zOff), h0)
    b_dip2[cnt] = modD.calcB(i-(s2+zOff), h0)
    b_dip3[cnt] = modD.calcB(i-(s3+zOff), h0)
    
    b_cyl0[cnt] = modC.calcB_cyl(i-(s0+zOff), 0.)
    b_cyl1[cnt] = modC.calcB_cyl(i-(s1+zOff), 0.)
    b_cyl2[cnt] = modC.calcB_cyl(i-(s2+zOff), 0.)
    b_cyl3[cnt] = modC.calcB_cyl(i-(s3+zOff), 0.)
    
    cnt += 1
    
plo.plotter2d((b_dip0, b_dip1, b_dip2, b_dip3), ("DIP 0", "1", "2", "3"))    
plo.plotter2d((b_cyl0, b_cyl1, b_cyl2, b_cyl3), ("CYL 0", "1", "2", "3"))
    
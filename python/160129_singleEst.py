import dataAcquisitionMulti as datAc
import EKF as k
import handDim as h
import modelDip as modD
import numpy as np
import plotting as plo
import matplotlib.pyplot as plt

''' estimating single finger and sensor '''

''' simulation of perfect data for fitting '''
fingList = [h.phalMid]
sensList = [h.sMid_car]
jointList = [h.jointMid_car]
t = np.arange(0,np.pi/2,0.01)       # describing the angles
angles = np.zeros((len(t),2*len(fingList)))
cnt = 0
for i in t:
#    TODO adjust it on the number of fingers you want to measure
    angles[cnt] = np.array([i, 0])#,    # angle index
#                                0, i,    # angle mid
#                                i, 0.4,    # angle rin
#                                i, i*0.3])   # angle pin
        
    cnt += 1
    
b = np.zeros((len(t), 3*len(sensList)))    

cnt = 0
for i in range(len(t)):    
    b[i] = modD.cy.angToBm_cy(angles[i],fingList,sensList,jointList)              # simulating dipole model



''' fitting '''
d = datAc.textAcquisition("160129_mid3")[1]
d *= 0.01

(scale, off) = datAc.getScaleOff(b,d)

d_fit = d*scale+off

plo.plotter2d((b,d_fit,d),("sim","fitted","raw"),shareAxis=False)


''' estimation '''

P = np.eye(2)
# process noise covariance matrix (2x2)
Q = np.diag([1e+2, 1e-2])                
# measurement noise covariance matrix (3x3)                
R = np.diag([1e+1, 1e+1, 1e+1])    

estAngK = np.zeros((len(d_fit)+1,2))

cnt = 1
for i in d_fit:    
    (x_p, P_p) = k.EKF_predict_fing(estAngK[cnt-1], P, Q)    
    (estAngK[cnt], P) = k.EKF_update_fing(k.jacoAngToB, i, x_p, P_p, R)
    
    cnt += 1    
    
cnt = 0    
x_est = np.zeros((len(d_fit)+1,2))    
for i in d_fit:
#    print "---------normal estimation step ",cnt,"--------"
    tmp = modD.estimate_BtoAng(x_est[cnt], fingList, jointList, sensList, i)
    x_est[cnt+1] = tmp.x
    
    cnt += 1
    
    
plt.figure()    
plo.plotter2d((estAngK,x_est),("estimatedK","normal"))    


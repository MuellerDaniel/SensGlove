import numpy as np
import EKF as k
import handDim as h
import jacB as j
import modelDip as modD
import plotting as plo
import dataAcquisitionMulti as datAc
import matplotlib.pyplot as plt
import time, random

''' simulating the data '''

sensList = [h.sInd_car,h.sMid_car,h.sRin_car,h.sPin_car]
fingList = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
jointList = [h.jointInd_car,h.jointMid_car, h.jointRin_car, h.jointPin_car]

t = np.arange(0,np.pi/2,0.01)       # describing the angles
angles = np.zeros((len(t),2*len(fingList)))
cnt = 0
for i in t:
#    TODO adjust it on the number of fingers you want to measure
#    angles[cnt] = np.array([0.3, i,    # angle index
#                            i, i*0.4,    # angle mid
#                            i, 0.8,    # angle rin
#                            0, i])   # angle pin
    angles[cnt] = np.array([i, 0.,    # angle index
                            i, 0.,    # angle mid
                            i, 0.,    # angle rin
                            i, 0.])   # angle pin
        
    cnt += 1
    
b = np.zeros((len(t), 3*len(sensList)))
offset = 3*np.random.rand(12,1).reshape(12,)
scale = np.random.rand(1,12).reshape(12,)+0.3
b_noise = np.zeros((len(t), 3*len(sensList)))


for i in range(len(t)): 
    b[i] = modD.cy.angToBm_cy(angles[i],fingList,sensList,jointList)           # simulating dipole model
    b_noise[i] = modD.cy.angToBm_cy(angles[i],fingList,sensList,jointList)  #*scale + offset

    
#plt.close('all')    
#plo.plotter2d((b_cyl,b_dip),("cyl","dip"),shareAxis=False)
#plo.plotter2d((b[:,:3], b[:,3:6], b[:,6:9], b[:,9:]),
#              ("dipole index","dipole middle","dipole ring","dipole pinky"))
plo.plotter2d((b_noise[:,:3], b_noise[:,3:6], b_noise[:,6:9], b_noise[:,9:]),
              ("dipole index","dipole middle","dipole ring","dipole pinky"))              
              
  
''' fitting measured data '''
#d = datAc.textAcquisition("160129_all1")
#
#(sInd, oInd) = datAc.getScaleOff(b[0][0:3],d[0])
#d_fit = d[0]*sInd+oInd

            
''' normal estimation '''
#x_est = np.zeros((len(t)+1, 2*len(fingList)))
#x_est[0] = angles[0]
#
#cnt = 0
#estStart = time.time()
#for i in b_noise:
##for i in b:
#    print "---------normal estimation step ",cnt,"--------"
#    tmp = modD.estimate_BtoAng(x_est[cnt], fingList, jointList, sensList, i)
#    x_est[cnt+1] = tmp.x
#    
#    cnt += 1
#estTime = time.time()-estStart 
#
#plo.plotter2d((x_est[:,0:2], x_est[:,2:4], x_est[:,4:6], x_est[:,6:]),
#              ("norm est index", "norm est middle","norm est ring","norm est pinky"))


''' EKF estimation '''              
# error covariance matrix (8x8), gets updated each step, so the initial one is not so important...
P = np.eye(8)

# process noise covariance matrix (8x8)
#Q = np.diag([1e+2, 1e-2, 1e-2, 1e+2, 1e+2, 1e-2, 1e+2, 1e-2,])
Q = np.eye(8) * 1e+2
                
# measurement noise covariance matrix (12x12)                
#R = np.diag([1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1])       
R = np.eye(12) * 1e-1                


x_EKF = np.zeros((len(t)+1, 2*4))
x_EKF[0] = angles[0]

cnt = 1
kalStart = time.time()
for i in b_noise:
#for i in b:
    print "---------step ",cnt,"--------"

    (x_p, P_p) = k.EKF_predict_hand(x_EKF[cnt-1], P, Q)
    
    (x_EKF[cnt], P) = k.EKF_update_hand(j.jacMulti, i, x_p, P_p, R)

    cnt += 1    
kalTime = time.time()-kalStart

print "time needed kalman: ", kalTime
#print "time needed minimization: ", estTime
plo.plotter2d((x_EKF[:,0:2], x_EKF[:,2:4], x_EKF[:,4:6], x_EKF[:,6:]),
              ("EKF est index", "EKF est middle","EKF est ring","EKF est pinky"))
              
print "scale:\n",scale              
print "offset:\n",offset
              
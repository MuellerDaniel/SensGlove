import dataAcquisitionMulti as datAc
import modelDip as modD
import modelDip_A as modDA
import modelCyl as modC
import modelCyl_A as modCA
import handDim as h
import numpy as np
import plotting as plo
import EKF as k
import time

''' simulating data for fitting '''
sensList = [h.sInd,h.sMid,h.sRin,h.sPin]
#sensList = [h.sInd]
fingList = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
#fingList = [h.phalInd]
jointList = [h.jointInd,h.jointMid,h.jointRin,h.jointRin]
#jointList = [h.jointInd]

t = np.arange(0,np.pi/2,0.1)       # describing the angles
#a = np.arange(0,np.pi*(110./180),(np.pi*(110./180))/16)
angles = np.zeros((len(t),3*len(fingList)))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0., 0.,     # moving only MCP
                            i, 0. ,0.,
                            i, 0. ,0.,
                            i, 0. ,0.])
        
    cnt += 1
    
b = np.zeros((len(t), 3*len(sensList)))
b_A = np.zeros((len(t), 3*len(sensList)))    

cnt = 0
for i in range(len(t)):
#    b[i] = modD.angToBm(angles[i][:2],fingList,sensList,jointList)    # simulating model without ad-ab
#    b_A[i] = modDA.angToBm(angles[i],fingList,sensList,jointList)              # simulating model with ad-ab
#    b[i] = modC.angToB_cyl(angles[i][:2],fingList,sensList,jointList)    # simulating model without ad-ab
    b_A[i] = modCA.angToB_cyl(angles[i],fingList,sensList,jointList)              # simulating model with ad-ab
    
#plo.plotter2d((b[:,:3], b[:,3:6], b[:,6:9], b[:,9:]),
#              ("without ad-ab index","middle","ring","pinky"))
#plo.plotter2d((b_A[:,:3], b_A[:,3:6], b_A[:,6:9], b_A[:,9:]),
#              ("with ad-ab index","middle","ring","pinky"))      
    
''' fitting measurements '''    
sString = 'set6'
(tim, s1, s2, s3, s4) = datAc.readMag("../datasets/160210/160210_"+sString+"_mag")

tim = tim[:300]
s1 = s1[:300]
s2 = s2[:300]
s3 = s3[:300]
s4 = s4[:300]

#print "fitting for fist"
#(scale, off) = datAc.getScaleOff(b_A[:,:3],s1[157:315]) 
#s1_fit = s1*scale+off
##plo.plotter2d((b_A[:,:3], s1_fit[157:315], s1[157:315]),("sim", "fitted", "meas"))

print "fitting for 90"
start = 42
end = 85
(scale, off) = datAc.getScaleOff(b_A[:,:3],s1[start:end]) 
s1_fit = s1*scale+off
plo.plotter2d((b_A[:,:3], s1_fit[start:end], s1[start:end]),("sim1", "fitted", "meas"))

(scale, off) = datAc.getScaleOff(b_A[:,3:6],s2[start:end]) 
s2_fit = s2*scale+off
#plo.plotter2d((b_A[:,3:6], s2_fit[start:end], s2[start:end]),("sim2", "fitted", "meas"))

(scale, off) = datAc.getScaleOff(b_A[:,6:9],s3[start:end]) 
s3_fit = s3*scale+off
plo.plotter2d((b_A[:,6:9], s3_fit[start:end], s3[start:end]),("sim3", "fitted", "meas"))

(scale, off) = datAc.getScaleOff(b_A[:,9:],s4[start:end]) 
s4_fit = s4*scale+off
#plo.plotter2d((b_A[:,9:], s4_fit[start:end], s4[start:end]),("sim4", "fitted", "meas"))

# combining everything again...
s1_fit = np.append(s1_fit,np.append(s2_fit,np.append(s3_fit,s4_fit,1),1),1)

''' estimating measurements '''
P = np.eye(12)

#Q = np.eye(12) * 1e+1
Q = np.diag([1e+3, 1e+3, 1e+1, 1e+3, 1e+3, 1e+1, 1e+3, 1e+3, 1e+1, 1e+3, 1e+3, 1e+1])
                
R = np.eye(12) * 1e+2     

estAng = np.zeros((len(s1_fit)+1, 3*len(fingList)))

b = ((0.0,np.pi/2.),
    (0.0,np.pi/2.),
    (-(30./180)*np.pi,(30./180)*np.pi),
    (0.0,np.pi/2.),
    (0.0,np.pi/2.),
    (-(30./180)*np.pi,(30./180)*np.pi),
    (0.0,np.pi/2.),
    (0.0,np.pi/2.),
    (-(30./180)*np.pi,(30./180)*np.pi),
    (0.0,np.pi/2.),
    (0.0,np.pi/2.),
    (-(30./180)*np.pi,(30./180)*np.pi))

cnt = 1
for i in range(0,len(s1_fit)):
#    print "estimation step: ", i-1
    
#   four sensors, four fingers
    (x_p, P_p) = k.EKF_predict_hand_A(estAng[cnt-1], P, Q)
    
    (estAng[cnt], P) = k.EKF_update_hand_A(s1_fit[i], x_p, P_p, R)    
    
    cnt += 1
    
    
    
# add the DIP states
estAng_I = estAng[:,:3]
dip_I = estAng_I[:,1]*(2./3.)
estAng_I = np.insert(estAng_I,2,dip_I,1)

estAng_M = estAng[:,3:6]
dip_M = estAng_M[:,1]*(2./3)
estAng_M = np.insert(estAng_M,2,dip_M,1)

estAng_R = estAng[:,6:9]
dip_R = estAng_R[:,1]*(2./3)
estAng_R = np.insert(estAng_R,2,dip_R,1)

estAng_P = estAng[:,9:]
dip_P = estAng_P[:,1]*(2./3)
estAng_P = np.insert(estAng_P,2,dip_P,1)


    
plo.plotLeapVsMag((tim,estAng_I[1:]),(tim,s1,s1_fit[:,:3]),head="estAng vs B-field "+sString)

(timLeap, angInd, angMid, angRin, angPin) = datAc.readLeap("../datasets/160210/160210_"+sString+"_leap")
plo.plotLeapVsMag((timLeap,angInd,angMid,angRin,angPin),
                  (tim,estAng_I[1:],estAng_M[1:],estAng_R[1:],estAng_P[1:]),head="leap state vs est "+sString,dif=False)


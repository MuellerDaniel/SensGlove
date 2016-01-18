import modelCyl as modC
import modelEqMultiCython as modE
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np
import time,random

''' verifying the cyl model with the finger '''

#           prox-,   int-,     dist-    phalanges
phalInd = [0.03080, 0.02581, 0.01678]
phalMid = [0.03593, 0.03137, 0.01684]
phalRin = [0.03404, 0.02589, 0.01820]
phalPin = [0.02892, 0.02493, 0.01601]

# sensor positions [lateral(z), radial(rho)]
sInd = [-0.03, 0.024]     # rack1
sMid = [-0.0, 0.024]
#sMid = [0.,0.]
sRin = [-0.03, 0.024]
sPin = [-0.03, 0.024]

# joint position 
jointInd = [0.0, 0.0]
jointMid = [0.0, 0.00]
jointRin = [0.0, 0.00]
jointPin = [0.0, 0.0]

t = np.arange(0,np.pi/2,0.01)
#t = np.arange(0.6,1.0,0.001)
angles = np.zeros((len(t),2))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0])
    cnt += 1
    
b_cyl = np.zeros((len(angles),2))  
b_dip = np.zeros((len(angles),3))  
fingerPos = np.zeros((len(angles),2))
ang = np.zeros((len(angles),))

cnt = 0
startT = time.time()
for i in angles:
    b_cyl[cnt] = modC.angToB_cyl(i,phalMid,sMid,jointMid)    
    cnt += 1
print "time needed: ", time.time()-startT    

''' estimation '''
#startT = time.time()
#a = modC.estimateAng_cyl([0,0], phalMid, sMid, jointMid, b_cyl[-1])
#print "time needed: ", time.time()-startT
#print a.x
#print angles[-1]
   
estAng = np.zeros((len(angles),2))   
stat = np.zeros((len(angles),2))
tolerance = 1.e-06
cnt = 0
startT = time.time()
for i in b_cyl[1:]:
    startEst = time.time()
    temp = modC.estimateAng_cyl(estAng[cnt], phalMid, sMid, jointMid, i)
    stat[cnt] = [time.time()-startEst, temp.fun]
    estAng[cnt+1] = temp.x    
    cnt += 1    
print "time needed: ", time.time()-startT   
   
d = datAc.textAcquisition('150814_pinkyOff')

plt.close('all')
plo.plotter2d((b_cyl,estAng,angles),("model","estimated Angles","perfectAngles"),shareAxis=False)
#plo.plotter2d((b_cyl,angles),("model","angles"),shareAxis=False)

#plt.figure()
#plo.plotter2d((d,),("meas",))

plt.show()

import modelEqMultiCython as modE
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import *
import time, random
import fcnCyPy as fcn

## absolute positions of wooden-joints
#jointInd = [0.09138, 0.02957, -0.01087]         # to wooden-joint(index)
#jointMid = [0.09138, 0.00920, -0.01087]          # to wooden-joint(middle)
#jointRin = [0.09138, -0.01117, -0.01087]         # to wooden-joint(ring)
#jointPin = [0.09138, -0.03154, -0.01087]         # to wooden-joint(pinky)
#
#
## position of sensor
#s1 = [0.06755, 0.02957, 0.]     # sensor beneath index   
#s2 = [0.04755, 0.00920, 0.]     # sensor beneath middle
#s3 = [0.06755, -0.01117, 0.]    # sensor beneath ring
#s4 = [0.04755, -0.03012, 0.]    # sensor beneath pinky

''' taking s0 as initial position... '''
# position of sensor
zSensor = 0.0
#s1 = [0., 0.0, zSensor]
#s2 = [s1[0]-0.02, -0.02063, zSensor]     # sensor beneath middle
#s3 = [s1[0], -0.02063*2, zSensor]    # sensor beneath ring
#s4 = [s1[0]-0.02, -0.02063*3, zSensor]    # sensor beneath pinky
s1 = [0.0, 0.0, zSensor]
s2 = [s1[0], -0.02063, zSensor]     # sensor beneath middle
s3 = [s1[0], -0.02063*2, zSensor]    # sensor beneath ring
s4 = [s1[0], -0.02063*3, zSensor]    # sensor beneath pinky

# position of wooden joints
# TODO adjust them, when you have your rack!
xJoint = 0.03       # distance between sensor rack and joints
#zJoint = -0.02
zJoint = -0.001
jointInd = [xJoint, 0., -0.03006+zJoint]                                 # to wooden-joint(index)
jointMid = [xJoint, jointInd[1]-0.01930, -0.02000+zJoint]          # to wooden-joint(middle)
jointRin = [xJoint, jointMid[1]-0.01930, -0.02000+zJoint]         # to wooden-joint(ring)
jointPin = [xJoint, jointRin[1]-0.01896, -0.02802+zJoint]         # to wooden-joint(pinky)

# lengths of phalanges
phalInd = [0.03080, 0.02581, 0.01678]
phalMid = [0.03593, 0.03137, 0.01684]
phalRin = [0.03404, 0.02589, 0.01820]
phalPin = [0.02892, 0.02493, 0.01601]

t = np.arange(0,1/2.*np.pi,0.01)
angles = np.array([[0.,0.,0.]])
#orienN = np.array([[0.,0.,0.]])
cnt = 0
for i in t:
    angles = np.append(angles,[[i,0,0]],axis=0)
#    angles = np.append(angles,[[i, 
#                                random.uniform(1,np.pi/2), 
#                                random.uniform(0,0.5)]], axis=0)
    cnt += 1
angles = angles[1:]    
                

''' calculating the B-field '''
calcBInd = np.array([[0.,0.,0.]])
calcBMid = np.array([[0.,0.,0.]])
calcBRin = np.array([[0.,0.,0.]])
calcBPin = np.array([[0.,0.,0.]])

# for moving all 4 fingers the same way...
for i in angles:
#    calcBInd = np.append(calcBInd,modE.angToB(i,phalInd,jointInd,s1)+
#                                  modE.angToB(i,phalMid,jointMid,s1)+
#                                  modE.angToB(i,phalRin,jointRin,s1)+
#                                  modE.angToB(i,phalPin,jointPin,s1),axis=0)    
#    calcBMid = np.append(calcBMid,modE.angToB(i,phalInd,jointInd,s2)+
#                                  modE.angToB(i,phalMid,jointMid,s2)+
#                                  modE.angToB(i,phalRin,jointRin,s2)+
#                                  modE.angToB(i,phalPin,jointPin,s2),axis=0)
#    calcBRin = np.append(calcBRin,modE.angToB(i,phalInd,jointInd,s3)+
#                                  modE.angToB(i,phalMid,jointMid,s3)+
#                                  modE.angToB(i,phalRin,jointRin,s3)+
#                                  modE.angToB(i,phalPin,jointPin,s3),axis=0)
#    calcBPin = np.append(calcBPin,modE.angToB(i,phalInd,jointInd,s4)+
#                                  modE.angToB(i,phalMid,jointMid,s4)+
#                                  modE.angToB(i,phalRin,jointRin,s4)+
#                                  modE.angToB(i,phalPin,jointPin,s4),axis=0)                                  
    calcBInd = np.append(calcBInd,modE.angToB(i,phalInd,jointInd,s1),axis=0)
    calcBMid = np.append(calcBMid,[modE.angToP(i,phalInd,jointInd)],axis=0)
calcBInd = calcBInd[1:]    
calcBMid = calcBMid[1:]    
#calcBRin = calcBRin[1:]    
#calcBPin = calcBPin[1:]  


''' save it to a file in the desired format '''
#fi = open("151103_perfectB_straight",'w')
#for i in range(len(calcBInd)):
#    fi.write(str(0) + "\t" + str(calcBInd[i][0]) + "\t" + 
#                            str(calcBInd[i][1]) + "\t" + 
#                            str(calcBInd[i][2]) + "\n")
#    fi.write(str(1) + "\t" + str(calcBMid[i][0]) + "\t" + 
#                            str(calcBMid[i][1]) + "\t" + 
#                            str(calcBMid[i][2]) + "\n")
#    fi.write(str(2) + "\t" + str(calcBRin[i][0]) + "\t" + 
#                            str(calcBRin[i][1]) + "\t" + 
#                            str(calcBRin[i][2]) + "\n")
#    fi.write(str(3) + "\t" + str(calcBPin[i][0]) + "\t" + 
#                            str(calcBPin[i][1]) + "\t" + 
#                            str(calcBPin[i][2]) + "\n")
#fi.close()                            

plo.plotter2d((calcBInd, calcBMid, calcBRin, calcBPin),("ind","mid","rin","pin"),shareAxis=False)
#plt.show()
# the angles...
#plt.figure()
#plt.plot(angles[:,0],linestyle='-')
#plt.plot(angles[:,1],linestyle='-.')
#plt.plot(angles[:,2],linestyle=':')
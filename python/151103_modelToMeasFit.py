''' trying to find the right values for the joint positions,
    in order to match the model to the measurement data '''

import modelEqMultiCython as modE
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import *
import time, random
import fcnCyPy as fcn
''' the measurement data '''
measDat = datAc.textAcquisition("151102_rawMeas_move")
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
s1 = [0., 0.0, zSensor]
s2 = [s1[0]-0.02, -0.02063, zSensor]     # sensor beneath middle
s3 = [s1[0], -0.02063*2, zSensor]    # sensor beneath ring
s4 = [s1[0]-0.02, -0.02063*3, zSensor]    # sensor beneath pinky

# position of wooden joints
# TODO adjust them, when you have your rack!
xJoint = 0.03-0.0045       # distance between sensor-rack and joints
zJoint = -0.001
#jointInd = [xJoint, 0., -0.03006+zJoint]                                 # to wooden-joint(index)
#jointMid = [xJoint, jointInd[1]-0.01930, -0.02000+zJoint]          # to wooden-joint(middle)
#jointRin = [xJoint, jointMid[1]-0.01930, -0.02000+zJoint]         # to wooden-joint(ring)
#jointPin = [xJoint, jointRin[1]-0.01896, -0.02802+zJoint]         # to wooden-joint(pinky)

a = np.arange(-0.04,0.04,0.005)
jointInd = np.zeros((len(a),3))
jointMid = np.zeros((len(a),3))
jointRin = np.zeros((len(a),3))
jointPin = np.zeros((len(a),3))
cnt = 0
for i in a:         # virtually moving the rack from right to left on the hand (in y-direction)
    jointInd[cnt] = [xJoint, i, -0.03006+0.025]
    jointMid[cnt] = [xJoint, jointInd[cnt][1]-0.02007, -0.02000+0.025]
    jointRin[cnt] = [xJoint, jointMid[cnt][1]-0.01970, -0.02000+0.025]
    jointPin[cnt] = [xJoint, jointRin[cnt][1]-0.01896, -0.02802+0.025]
    cnt += 1

# lengths of phalanges
phalInd = [0.03080, 0.02581, 0.01678]
phalMid = [0.03593, 0.03137, 0.01684]
phalRin = [0.03404, 0.02589, 0.01820]
phalPin = [0.02892, 0.02493, 0.01601]

t = np.arange(0,1/2.*np.pi,0.01)
angles = np.array([[0.,0.,0.]])

for i in t:
    angles = np.append(angles,[[i,0,0]],axis=0)

angles = angles[1:]


''' calculating the B-field '''
calcBInd = np.zeros((len(a),len(angles),3))
calcBMid = np.zeros((len(a),len(angles),3))
calcBRin = np.zeros((len(a),len(angles),3))
calcBPin = np.zeros((len(a),len(angles),3))

# for moving all 4 fingers the same way...

for j in range(len(a)):
    cnt = 0
    for i in angles:
        calcBInd[j][cnt] = (modE.angToB(i,phalInd,jointInd[j],s1)+
                            modE.angToB(i,phalMid,jointMid[j],s1)+
                            modE.angToB(i,phalRin,jointRin[j],s1)+
                            modE.angToB(i,phalPin,jointPin[j],s1))
        calcBMid[j][cnt] = (modE.angToB(i,phalInd,jointInd[j],s2)+
                          modE.angToB(i,phalMid,jointMid[j],s2)+
                          modE.angToB(i,phalRin,jointRin[j],s2)+
                          modE.angToB(i,phalPin,jointPin[j],s2))
        calcBRin[j][cnt] = (modE.angToB(i,phalInd,jointInd[j],s3)+
                          modE.angToB(i,phalMid,jointMid[j],s3)+
                          modE.angToB(i,phalRin,jointRin[j],s3)+
                          modE.angToB(i,phalPin,jointPin[j],s3))
        calcBPin[j][cnt] = (modE.angToB(i,phalInd,jointInd[j],s4)+
                          modE.angToB(i,phalMid,jointMid[j],s4)+
                          modE.angToB(i,phalRin,jointRin[j],s4)+
                          modE.angToB(i,phalPin,jointPin[j],s4))
        cnt += 1


''' plotting '''
plo.plotter2d((measDat[0],measDat[1],measDat[2],measDat[3]),("measInd","measMid","measRin","measPin"))

ax = 1
plt.figure()
cnt = 0
for i in calcBInd:
    plt.plot(i[:,ax],label=str(cnt))
    cnt += 1
plt.title('index')
plt.legend()

plt.figure()
cnt = 0
for i in calcBMid:
    plt.plot(i[:,ax],label=str(cnt))
    cnt += 1
plt.title('middle')
plt.legend()

plt.figure()
cnt = 0
for i in calcBRin:
    plt.plot(i[:,ax],label=str(cnt))
    cnt += 1
plt.title('ring')
plt.legend()

plt.figure()
cnt = 0
for i in calcBPin:
    plt.plot(i[:,ax],label=str(cnt))
    cnt += 1
plt.title('pinky')
plt.legend()

plt.show()

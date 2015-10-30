import modelEqMultiCython as modE
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import *
import time
import fcnCyPy as fcn

# absolute positions of wooden-joints
jointInd = [0.09138, 0.02957, -0.01087]         # to wooden-joint(index)
jointMid = [0.09138, 0.00920, -0.01087]          # to wooden-joint(middle)
jointRin = [0.09138, -0.01117, -0.01087]         # to wooden-joint(ring)
jointPin = [0.09138, -0.03154, -0.01087]         # to wooden-joint(pinky)

# position of sensor
s1 = [0.06755, 0.02957, 0.]     # sensor beneath index
#s1 = [0.08755, 0.02957, 0.]
#s2 = [0.06755, 0.00920, 0.]    
s2 = [0.04755, 0.00920, 0.]     # sensor beneath middle
s3 = [0.06755, -0.01117, 0.]    # sensor beneath ring
#s3 = [0.08755, -0.01117, 0.]
#s4 = [0.06755, -0.03012, 0.]     
s4 = [0.04755, -0.03012, 0.]    # sensor beneath pinky

# lengths of phalanges
phalInd = [0.03038, 0.02728, 0.02234]
phalMid = [0.03640, 0.03075, 0.02114]
phalRin = [0.03344, 0.02782, 0.01853]
phalPin = [0.02896, 0.02541, 0.01778]

t = np.arange(0,1/2.*np.pi,0.01)
angles = np.array([[0.,0.,0.]])
#orienN = np.array([[0.,0.,0.]])

for i in t:
    angles = np.append(angles,[[i,0,0]],axis=0)
#    orienN = np.append(orienN, [[-1*np.cos(i),        # verifying the orientation
#                               0,
#                               1*np.sin(i)]],axis=0)    
angles = angles[1:]        
#orienN = orienN[1:]
#calcOrien = np.array([[0.,0.,0.]])      # verifying the orientation
#for i in angles:
#    calcOrien = np.append(calcOrien,[[np.sin(-np.pi/2+abs(-i[0]-i[1]-i[2])),
#                  0,
#                  np.cos(-np.pi/2+abs(-i[0]-i[1]-i[2]))]], axis=0)                  
#calcOrien = calcOrien[1:]

#calcPos = np.array([[0.,0.,0.]])        # verifying the position...
#for i in angles:
#    calcPos=np.append(calcPos,
#                 [[xPos(i,phalInd,jointInd[0]),
#                  yPos(i,phalInd,jointInd[1]),
#                  zPos(i,phalInd,jointInd[2])]],axis=0)
#calcPos = calcPos[1:]                  

''' calculating the B-field '''
#calcBInd = np.array([[0.,0.,0.]])
#calcBMid = np.array([[0.,0.,0.]])
#calcBRin = np.array([[0.,0.,0.]])
#calcBPin = np.array([[0.,0.,0.]])
#calcB_old = np.array([[0.,0.,0.]])
#cnt = 0
#for i in angles:
#    calcBInd = np.append(calcBInd,evalfuncMagAngle(i,phalInd,jointInd,s1)+
#                                  evalfuncMagAngle(i,phalMid,jointMid,s1)+
#                                  evalfuncMagAngle(i,phalRin,jointRin,s1)+
#                                  evalfuncMagAngle(i,phalPin,jointPin,s1),axis=0)
#    
#    calcBMid = np.append(calcBMid,evalfuncMagAngle(i,phalInd,jointInd,s2)+
#                                  evalfuncMagAngle(i,phalMid,jointMid,s2)+
#                                  evalfuncMagAngle(i,phalRin,jointRin,s2)+
#                                  evalfuncMagAngle(i,phalPin,jointPin,s2),axis=0)
#                                  
#    calcBRin = np.append(calcBRin,evalfuncMagAngle(i,phalInd,jointInd,s3)+
#                                  evalfuncMagAngle(i,phalMid,jointMid,s3)+
#                                  evalfuncMagAngle(i,phalRin,jointRin,s3)+
#                                  evalfuncMagAngle(i,phalPin,jointPin,s3),axis=0)
#
#    calcBPin = np.append(calcBPin,evalfuncMagAngle(i,phalInd,jointInd,s4)+
#                                  evalfuncMagAngle(i,phalMid,jointMid,s4)+
#                                  evalfuncMagAngle(i,phalRin,jointRin,s4)+
#                                  evalfuncMagAngle(i,phalPin,jointPin,s4),axis=0)                                  
##    calcB_old = np.append(calcB_old,modE.evalfuncMagDotH(calcPos[cnt],calcOrien[cnt],s1),axis=0)
#    cnt += 1    
#calcBInd = calcBInd[1:]    
#calcBMid = calcBMid[1:]    
#calcBRin = calcBRin[1:]    
#calcBPin = calcBPin[1:]    
#calcB_old = calcB_old[1:]

# simply get the data from the textfile...
calcBdata = datAc.textAcquisition("151030_perfectB_H")

''' estimating the angles '''
#estAngIndPy = np.zeros((len(t),3))
#estAngMidPy = np.zeros((len(t),3))
#estAngRinPy = np.zeros((len(t),3))
#estAngPinPy = np.zeros((len(t),3))
#estAngIndCy = np.zeros((len(t),3))
#estAngMidCy = np.zeros((len(t),3))
#estAngRinCy = np.zeros((len(t),3))
#estAngPinCy = np.zeros((len(t),3))
estAngInd = np.zeros((len(t),3))
estAngMid = np.zeros((len(t),3))
estAngRin = np.zeros((len(t),3))
estAngPin = np.zeros((len(t),3))

bnds = ((0.0,np.pi/2),    # index
        (0.0,np.pi/2),
        (0.0,np.pi/2),
        (0.0,np.pi/2),    # middle
        (0.0,np.pi/2),
        (0.0,np.pi/2),
        (0.0,np.pi/2),    # ring
        (0.0,np.pi/2),
        (0.0,np.pi/2),
        (0.0,np.pi/2),    # pinky
        (0.0,np.pi/2),
        (0.0,np.pi/2))
cnt = 0
hurray = 0

startTime = time.time()                      
for i in range(len(calcBdata[0][1:])):
    
       
    res = modE.estimate_BtoAng(np.concatenate((estAngInd[i], estAngMid[i], estAngRin[i], estAngPin[i])),
                                [phalInd,phalMid,phalRin,phalPin],
                                [jointInd,jointMid,jointRin,jointPin],
                                [s1,s2,s3,s4],
                                np.concatenate((calcBdata[0][i+1],calcBdata[1][i+1],calcBdata[2][i+1],calcBdata[3][i+1])),
                                bnds)
    # python way
#    resPy = modE.estimate_BtoAngPy(np.concatenate((estAngIndPy[i], estAngMidPy[i], estAngRinPy[i], estAngPinPy[i])),
#                                [phalInd,phalMid,phalRin,phalPin],
#                                [jointInd,jointMid,jointRin,jointPin],
#                                [s1,s2,s3,s4],
#                                np.concatenate((calcBdata[0][i+1],calcBdata[1][i+1],calcBdata[2][i+1],calcBdata[3][i+1])),
#                                bnds)
    
    # cython way                                
#    resCy = modE.estimate_BtoAngCy(np.concatenate((estAngIndCy[i], estAngMidCy[i], estAngRinCy[i], estAngPinCy[i])),
#                                np.reshape([phalInd,phalMid,phalRin,phalPin],((12,))),
#                                np.reshape([jointInd,jointMid,jointRin,jointPin],((12,))),
#                                np.reshape([s1,s2,s3,s4],((12,))),
#                                np.concatenate((calcBdata[0][i+1],calcBdata[1][i+1],calcBdata[2][i+1],calcBdata[3][i+1])),
#                                bnds)
        
#    if res.success:
#        hurray += 1
#    else:
#        print "error, iteration: ",cnt
    
    estAngInd[i+1] = res.x[0:3]    
    estAngMid[i+1] = res.x[3:6]    
    estAngRin[i+1] = res.x[6:9]    
    estAngPin[i+1] = res.x[9:12]    
#    estAngIndPy[i+1] = resPy.x[0:3]
#    estAngMidPy[i+1] = resPy.x[3:6]
#    estAngRinPy[i+1] = resPy.x[6:9]
#    estAngPinPy[i+1] = resPy.x[9:12]
#    
#    estAngIndCy[i+1] = resCy.x[0:3]
#    estAngMidCy[i+1] = resCy.x[3:6]
#    estAngRinCy[i+1] = resCy.x[6:9]
#    estAngPinCy[i+1] = resCy.x[9:12]    
    
print "time needed: ",time.time()-startTime    



'''----------PLOTTING----------'''

#plt.close('all')

#plo.plotter2d((calcBdata[0],calcBdata[1],calcBdata[2],calcBdata[3]),("oldind","oldmid","oldrin","oldpin"))
#plo.plotter2d((calcBInd,calcBMid,calcBRin,calcBPin),("ind","mid","rin","pin"))
plo.plotter2d((estAngInd,estAngMid,estAngRin,estAngPin),("angleInd","angleMid","angleRin","anglePin"))
''' code for comparing python and cython results with the perfect angles '''
#pyDev0 = estAngIndPy-angles
#pyDev1 = estAngMidPy-angles
#pyDev2 = estAngRinPy-angles
#pyDev3 = estAngPinPy-angles
#
#cyDev0 = estAngIndCy-angles
#cyDev1 = estAngMidCy-angles
#cyDev2 = estAngRinCy-angles
#cyDev3 = estAngPinCy-angles
#plo.plotter2d((estAngIndPy,estAngMidPy,estAngRinPy,estAngPinPy),("angleInd","angleMid","angleRin","anglePin"))
#plo.plotter2d((estAngIndCy,estAngMidCy,estAngRinCy,estAngPinCy),("angleIndCy","angleMidCy","angleRinCy","anglePinCy"))

#f = plt.figure()
#a=f.add_subplot(3,4,1,title='X-deviation index')
#a.scatter(np.arange(len(angles[:,0])),pyDev0[:,0],color='r')
#a.scatter(np.arange(len(angles[:,0])),cyDev0[:,0],color='b')
#a=f.add_subplot(3,4,2,title='X-deviation middle')
#a.scatter(np.arange(len(angles[:,0])),pyDev1[:,0],color='r')
#a.scatter(np.arange(len(angles[:,0])),cyDev1[:,0],color='b')
#a=f.add_subplot(3,4,3,title='X-deviation ring')
#a.scatter(np.arange(len(angles[:,0])),pyDev2[:,0],color='r')
#a.scatter(np.arange(len(angles[:,0])),cyDev2[:,0],color='b')
#a=f.add_subplot(3,4,4,title='X-deviation pinky')
#a.scatter(np.arange(len(angles[:,0])),pyDev3[:,0],color='r')
#a.scatter(np.arange(len(angles[:,0])),cyDev3[:,0],color='b')
#
#a=f.add_subplot(3,4,5,title='Y-deviation index')
#a.scatter(np.arange(len(angles[:,1])),pyDev0[:,1],color='r')
#a.scatter(np.arange(len(angles[:,1])),cyDev0[:,1],color='b')
#a=f.add_subplot(3,4,6,title='Y-deviation middle')
#a.scatter(np.arange(len(angles[:,1])),pyDev1[:,1],color='r')
#a.scatter(np.arange(len(angles[:,1])),cyDev1[:,1],color='b')
#a=f.add_subplot(3,4,7,title='Y-deviation ring')
#a.scatter(np.arange(len(angles[:,1])),pyDev2[:,1],color='r')
#a.scatter(np.arange(len(angles[:,1])),cyDev2[:,1],color='b')
#a=f.add_subplot(3,4,8,title='Y-deviation pinky')
#a.scatter(np.arange(len(angles[:,1])),pyDev3[:,1],color='r')
#a.scatter(np.arange(len(angles[:,1])),cyDev3[:,1],color='b')
#
#a=f.add_subplot(3,4,9,title='Z-deviation index')
#a.scatter(np.arange(len(angles[:,2])),pyDev0[:,2],color='r')
#a.scatter(np.arange(len(angles[:,2])),cyDev0[:,2],color='b')
#a=f.add_subplot(3,4,10,title='Z-deviation middle')
#a.scatter(np.arange(len(angles[:,2])),pyDev1[:,2],color='r')
#a.scatter(np.arange(len(angles[:,2])),cyDev1[:,2],color='b')
#a=f.add_subplot(3,4,11,title='Z-deviation ring')
#a.scatter(np.arange(len(angles[:,2])),pyDev2[:,2],color='r')
#a.scatter(np.arange(len(angles[:,2])),cyDev2[:,2],color='b')
#a=f.add_subplot(3,4,12,title='Z-deviation pinky')
#a.scatter(np.arange(len(angles[:,2])),pyDev3[:,2],color='r',label='python version')
#a.scatter(np.arange(len(angles[:,2])),cyDev3[:,2],color='b', label='cython version')
#a.legend(loc='lower left')


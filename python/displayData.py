# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 14:57:20 2015

@author: daniel
"""

import string
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import *

"""
reading the data from a textfile and saving it in a matrix
"""
def scanData(fileName):
    try:
        f = open(fileName, 'r')
    except IOError:
        print "File not found!"
    
   # offset=np.array([7.3829999999999938, -7.0713000000000186, 31.645324999999961])
    offsetX = 14.741774999999986
    offsetY = 8.5498749999999806
    offsetZ = 33.112424999999973
    line = f.readline()    
    dataMat = np.empty(shape=[0,4])     
    while(line != ""):    
        if (line.startswith("#")):
            print line
        else:  
            dataString = string.split(line, "\t")
            dataMat = np.append(dataMat, 
                                [[float(dataString[0]), 
                                  float(float(dataString[1]) - offsetX), 
                                  float(float(dataString[2]) - offsetY), 
                                  float(float(dataString[3]) - offsetZ)]],axis=0)        
        line = f.readline() 
        
    return dataMat
    
"""
 functions for estimating the position and orientation
"""
def getH(P,S):
    return np.cross(P,(S-P))

# magnetic function
#P position of magnet
#S position of sensor
def evalfuncMag(P,S):
    H=getH(P,S)
    R = (S-P)
    return np.array([((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) - 
                                        (H/(np.linalg.norm(R)**3)))])
                                        

# magnetic function subtracting the measured B-field                                     
def funcMagY(P,S,B):    
    val = evalfuncMag(P,S)    
    #print "P",P
    #print "S",S
    #print "B", B
    res = np.linalg.norm(B - val)       
    #print "funcMag res: ",res 
    return res    

def estimate(P,S,B):
    res = minimize(funcMagY,P,args=(S,B),method='bfgs',tol=1e-2)
    return res.x        # as result you will get the P vector!
    

#noMotionMagnet = scanData("150630_dataNoMotionMagnet")
#noMotion = scanData("150630_dataMotion")

# motion positions for "*_dataMotion":
#motion = scanData("150630_dataMotion")
# 1)    MCP 0     PIP 0    DIP 0 (straight)
# 2)    MCP 0     PIP 0    DIP 
# 3)    MCP 0     PIP 90   DIP ~90
# 4)    MCP ~90   PIP 90   DIP ~90
# 5)    MCP 90    PIP 90   DIP 0
# 6)    MCP 90    PIP 0    DIP 0
# 7     MCP 90    PIP 0    DIP 90 
# 8)    MCP 0     PIP 90   DIP 0
# 9)    MCP 0     PIP 0    DIP 0

# motion positions for "*_dataMotionsmall":
#motionsmall = scanData("150630_dataMotionSmall2")
# 1)    MCP 0     PIP 0    DIP 0 (straight)
# 2)    MCP 90    PIP 0    DIP 0
# 3)    MCP 0     PIP 0    DIP 0

dataStraight = scanData("150707_dataFlatY0")
dataBend = scanData("150707_dataFlatX0")
datay2 = scanData("150707_dataFlatY2")
#dataMove = scanData("150707_dataMoveVert2")
#dataMoveHo = scanData("150707_dataMoveHo2")

py0 = np.array([-0.04,0.05,0])
px0 = np.array([-0.1,-0.01,0])
py2 = np.array([-0.04,-0.07,0])
s0 = np.array([-0.04,-0.01,0])
# 6.7.15



estimatedData = []
estimatedOr = []

#for i in range(motionsmall.shape[0]):       # evaluating the whole dataset
##for i in range(500):
#    #print "evaluating row ", i
#    p0 = estimate(p0,s0,motion[i][1:])
#    estimatedData.append(p0)
#    orien = getH(p0, s0)    
#    estimatedOr.append(orien)
 
#estimatedData = np.reshape(estimatedData, (size(estimatedData)/3,3))
#estimatedOr = np.reshape(estimatedOr, (size(estimatedOr)/3, 3))
   
#fig2 = plt.figure()
#b = motion[:,0]
#b = b[0:500]

#mob = motion[0:500]

"""
Plotting one value
"""
#plt.plot(dataMoveHo[:,1], color='r', label='x')
#plt.plot(dataMoveHo[:,2], color='g', label='y')
#plt.plot(dataMoveHo[:,3], color='b', label='z')

"""
Plotting two valules
"""
#f,(ho, vert) = plt.subplots(1,2, sharey=True)
#vert.plot(dataMove[:,1], color='r', label='x')
#vert.plot(dataMove[:,2], color='g', label='y')
#vert.plot(dataMove[:,3], color='b', label='z')
#vert.set_title("vertical orientation")
#vert.legend()
#
#ho.plot(dataMoveHo[:,1], color='r', label='x')
#ho.plot(dataMoveHo[:,2], color='g', label='y')
#ho.plot(dataMoveHo[:,3], color='b', label='z')
#ho.set_title("horizontal orientation")

"""
Plotting three values 
"""
f, (y2, bend, straight) = plt.subplots(1,3, sharey = True)
#straight.subplot(121)
straight.plot(dataStraight[:,1], color='r', label='x') 
straight.plot(dataStraight[:,2], color='g', label='y') 
straight.plot(dataStraight[:,3], color='b', label='z')
straight.set_ylabel('Magnetic field strength [ugauss]')
straight.legend()
#plt.legend(('x','y','z'), loc='best')
straight.set_title('Y0')
# get min, max and avg value of magMat
resVect1 = np.array([min(dataStraight[:,1]), max(dataStraight[:,1]), mean(dataStraight[:,1])])
resVect1 = np.append(resVect1, np.array([min(dataStraight[:,2]), max(dataStraight[:,2]), mean(dataStraight[:,2])]))
resVect1 = np.append(resVect1, np.array([min(dataStraight[:,3]), max(dataStraight[:,3]), mean(dataStraight[:,3])]))
resVect1 = np.reshape(resVect1, (resVect1.size/3, 3))
print "resVect1 MCP 0 DIP 0 PIP 0\n", resVect1
straight.text(5,50,"meas: " + str(resVect1[:,2]))
straight.axhline(resVect1[0][2], color='y')
straight.axhline(resVect1[1][2], color='y')
straight.axhline(resVect1[2][2], color='y')
estY0 = evalfuncMag(py0,s0)
straight.text(5, 60, "estimated: " + str(estY0))


bend.plot(dataBend[:,1], color='r', label='x') 
bend.plot(dataBend[:,2], color='g', label='y') 
bend.plot(dataBend[:,3], color='b', label='z')
bend.set_ylabel('Magnetic field strength [ugauss]')
#plt.legend(('x','y','z'), loc='best')
bend.set_title('X0')
# get min, max and avg value of magMat
resVect2 = np.array([min(dataBend[:,1]), max(dataBend[:,1]), mean(dataBend[:,1])])
resVect2 = np.append(resVect2, np.array([min(dataBend[:,2]), max(dataBend[:,2]), mean(dataBend[:,2])]))
resVect2 = np.append(resVect2, np.array([min(dataBend[:,3]), max(dataBend[:,3]), mean(dataBend[:,3])]))
resVect2 = np.reshape(resVect2, (resVect2.size/3, 3))
print "resVect2 MCP 0 DIP 0 PIP 0\n", resVect2
bend.text(5,50,"meas: " + str(resVect2[:,2]))
bend.axhline(resVect2[0][2], color='y')
bend.axhline(resVect2[1][2], color='y')
bend.axhline(resVect2[2][2], color='y')
estX0 = evalfuncMag(px0,s0)
bend.text(5, 60, "estimated: " + str(estX0))


y2.plot(datay2[:,1], color='r', label='x') 
y2.plot(datay2[:,2], color='g', label='y') 
y2.plot(datay2[:,3], color='b', label='z')
y2.set_ylabel('Magnetic field strength [ugauss]')
#plt.legend(('x','y','z'), loc='best')
y2.set_title('Y2')
# get min, max and avg value of magMat
resVect3 = np.array([min(datay2[:,1]), max(datay2[:,1]), mean(datay2[:,1])])
resVect3 = np.append(resVect3, np.array([min(datay2[:,2]), max(datay2[:,2]), mean(datay2[:,2])]))
resVect3 = np.append(resVect3, np.array([min(datay2[:,3]), max(datay2[:,3]), mean(datay2[:,3])]))
resVect3 = np.reshape(resVect3, (resVect3.size/3, 3))
print "resVect3 MCP 0 DIP 0 PIP 0\n", resVect3
y2.text(5,50,"meas: " + str(resVect3[:,2]))
y2.axhline(resVect3[0][2], color='y')
y2.axhline(resVect3[1][2], color='y')
y2.axhline(resVect3[2][2], color='y')
estY2 = evalfuncMag(py2,s0)
y2.text(5, 60, "estimated: " + str(estY2))


"""
Plotting the motion things...
"""
#motionPlt = plt.subplot(311)
#motionPlt.plot(motionsmall[:,0], motionsmall[:,1], 'r') 
#motionPlt.plot(motionsmall[:,0], motionsmall[:,2], 'g') 
#motionPlt.plot(motionsmall[:,0], motionsmall[:,3], 'b')
#
#motionPlt.axvline(x=5, color='y')
#motionPlt.axvline(x=15, color='y')
##plt.plot(b, mob[:,1], 'r') 
##plt.plot(b, mob[:,2], 'g') 
##plt.plot(b, mob[:,3], 'b')
#motionPlt.set_ylabel('Magnetic field\nstrength [ugauss]')
#motionPlt.set_xlabel('time [s]')
#motionPlt.legend(('x','y','z'), loc='upper right')
#motionPlt.set_title('Motion')
#motionPlt.grid(True)
##plt.show()
#
##figP = plt.figure()
#estimatedPosPlt = plt.subplot(312)
#estimatedPosPlt.plot(motionsmall[:,0], estimatedData[:,0], 'r') 
#estimatedPosPlt.plot(motionsmall[:,0], estimatedData[:,1], 'g') 
#estimatedPosPlt.plot(motionsmall[:,0], estimatedData[:,2], 'b')
#
#estimatedPosPlt.axvline(x=5, color='y')
#estimatedPosPlt.axvline(x=15, color='y')
##plt.plot( estimatedData[:,0], 'r') 
##plt.plot( estimatedData[:,1], 'g') 
##plt.plot( estimatedData[:,2], 'b')
##plt.ylabel('Magnetic field\nstrength [ugauss]')
#estimatedPosPlt.set_xlabel('time [s]')
#estimatedPosPlt.legend(('x','y','z'), loc='upper right')
#estimatedPosPlt.set_title('estimated Pos')
#estimatedPosPlt.grid(True)
##plt.show()
#
#estimatedOrPlt = plt.subplot(313)
#estimatedOrPlt.plot(motionsmall[:,0], estimatedOr[:,0], 'r') 
#estimatedOrPlt.plot(motionsmall[:,0], estimatedOr[:,1], 'g') 
#estimatedOrPlt.plot(motionsmall[:,0], estimatedOr[:,2], 'b')
#
#estimatedOrPlt.axvline(x=5, color='y')
#estimatedOrPlt.axvline(x=15, color='y')
##plt.plot( estimatedData[:,0], 'r') 
##plt.plot( estimatedData[:,1], 'g') 
##plt.plot( estimatedData[:,2], 'b')
##plt.ylabel('Magnetic field\nstrength [ugauss]')
#estimatedOrPlt.set_xlabel('time [s]')
#estimatedOrPlt.legend(('x','y','z'), loc='upper right')
#estimatedOrPlt.set_title('estimated Or')
#estimatedOrPlt.grid(True)
plt.show()
    
#print "finished!"
    
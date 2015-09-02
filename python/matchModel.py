# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 13:16:02 2015

@author: daniel
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import string
from scipy.optimize import *

def evalfuncMag(P,S):
    #H=getH(P,S)
    H = 1*(P-S)
    #H = np.array([0,0,0])
    R = (S-P)
    factor = np.array([-1, 1, 1])
    return np.array([((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) - 
                                        (H/(np.linalg.norm(R)**3)))] * factor)
                                    
def funcMagY(P,S,B):    
    val = evalfuncMag(P,S)    
    res = np.linalg.norm(B - val)       
    #print "funcMag res: ",res 
    return res
  
def estimate(P,S,B):
    res = minimize(funcMagY,P,args=(S,B),method='bfgs',tol=1e-5)
    return res.x        # as result you will get the P vector! 
    

def scanData(fileName):
    #try:
    f = open(fileName, 'r')
    #except IOError:
    #    print "File not found!"
    
   # offset=np.array([7.3829999999999938, -7.0713000000000186, 31.645324999999961])
#    offsetX = 14.741774999999986
#    offsetY = 8.5498749999999806
#    offsetZ = 33.112424999999973
    offsetX = 0
    offsetY = 0
    offsetZ = 0
    # measurements that I neglect
    dataOffset = 10
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
        
    return dataMat[dataOffset:-1]

 
def getStatDynOffset(estValues, measValues):
    staticOff = np.array([0.,0.,0.])
    scale = np.array([0.,0.,0.])
    dynOffEst = np.array([0.,0.,0.])
    dynOffMeas = np.array([0.,0.,0.])
    # static offset
    # choose here your initial values
    startMat = measValues[10:40]
    meanMeas = np.array([np.mean(startMat[:,0]),
                         np.mean(startMat[:,1]),
                         np.mean(startMat[:,2])])
    staticOff = estValues[0] - meanMeas
    print "staticOff:\n" + str(staticOff)
    
    # scale factor
    i=0
    for i in range(3):
        #dynOffEst[i] = np.mean([np.max(estValues[:,i]), np.min(estValues[:,i])])
        #dynOffMeas[i] = np.mean([np.max(measValues[:,i]), np.min(measValues[:,i])])
        print "dynOffEst[i]/dynOffMeas[i] " + str(dynOffEst[i]) + " " + str(dynOffMeas[i])  
        scale[i] = dynOffEst[i]/dynOffMeas[i]        
        i+=1
    
    print "scale:\n" + str(scale)
    return (staticOff, scale)
    
    
def scaleMeasurements(real, meas):
    i=0
    raReal=0
    raMeas=0
    scale = np.array([0.,0.,0.])
    resMat = meas.copy()
    
    for i in range(3):
        raReal = max(real[:,i]) - min(real[:,i])
        raMeas = max(meas[:,i]) - min(meas[:,i])
        scale[i] = raReal/raMeas
        i+=1    
    print "scale " + str(scale)
    
    i=0
    for i in range(resMat.shape[0]):
        resMat[i][0] *= scale[0]
        resMat[i][1] *= scale[1]
        resMat[i][2] *= scale[2]
        i+=1
        
    return resMat
    
    
def shiftMeasurements(real, meas):
    offset = real[0] - meas[0]
    resMat = meas.copy()   
    
    startMat = meas[10:40]
    meanMeas = np.array([np.mean(startMat[:,0]),
                         np.mean(startMat[:,1]),
                         np.mean(startMat[:,2])])
    offset = real[0] - meanMeas
    
    i=0
    for i in range (resMat.shape[0]):
        resMat[i][0] += offset[0]
        resMat[i][1] += offset[1]
        resMat[i][2] += offset[2]
    #    yShiftArr[i][0] += offset[0]*scale[0]
    #    yShiftArr[i][1] += offset[1]*scale[1]
    #    yShiftArr[i][2] += offset[2]*scale[2]
        i+=1
    print "offset: " + str(offset)
    return resMat

def fitMeasurements(ref, meas):
    scaled = scaleMeasurements(ref, meas)
    fitted = shiftMeasurements(ref, scaled)
    return fitted



"""""""""""""""""""""
main program flow
"""""""""""""""""""""

values = np.empty(shape=[0,3]) 
r = 0.06
# also the position of the sensor
center = [-0.04, -0.01]
s0=np.array([-0.04, -0.01, 0])
# values for the half circle
t = np.arange(((-1/2.)*np.pi), ((1/2.)*np.pi), 0.01)
resMat = np.empty(shape=[0,3])
#measMat = np.empty(shape=[0,3])
res = np.array([0.,0.,0.])
estPosReal = np.empty(shape=[0,3]) 
estPosMeas = np.empty(shape=[0,3]) 
mu = 1.05
n = 310

"""
Calculating the magnetic field with the model
"""
# calculate the position values
i=0
while i < t.size:
    res[0] = (center[0] + r*np.cos(t[i]))
    res[1] = (center[1] + r*np.sin(t[i]))
    res[2] = 0
    values = np.append(values, [res])    
    i+=1
    
values = np.reshape(values, (values.size/3, 3))    

# calculate the magnetic field with the model
i=0
while i < values.shape[0]:
    resMat = np.append(resMat, evalfuncMag(values[i], s0))
    #resMat = np.append(resMat, evalfuncMagH(values[i], s0, valuesH[i]))
    i+=1
    
resMat = np.reshape(resMat, (resMat.size/3, 3))

"""
Read the measured points
"""
dataMat = scanData("150707_dataMoveHo")
# eliminate first column
measMat = dataMat[:,1:,]
#measMat[:,0] = measMat[:,1]
#measMat[:,1] = measMat[:,2]
#measMat[:,2] = measMat[:,3]
#measMat = np.reshape(measMat, (measMat.size/3, 3))   

"""
calculate the offsets
"""
measMat = fitMeasurements(resMat, measMat)

"""
estimate the position
"""
p0 = np.array([-0.07, -0.1, 0])
# for the calculated magnetic data
#i=0
#for i in range (resMat.shape[0]):
#    print "estimating the perfect positions..." + str(i)
#    if (i == 0):     
#        estPosReal = np.append(estPosReal, estimate(p0, s0, resMat[i]))
#        estPosReal = np.reshape(estPosReal, (estPosReal.size/3, 3))
#        #print "calc position nr: " + str(i) + " " + str(estPos[i])
#        #print "real position: " + str(values[i])
#    else:
#        estPosReal = np.append(estPosReal, estimate(estPosReal[i-1], s0, resMat[i]))        
#        estPosReal = np.reshape(estPosReal, (estPosReal.size/3, 3))
#        #print "calc position nr: " + str(i) + " " + str(estPos[i])
#        #print "real position: " + str(values[i])
#    i+=1
#    
# for the measured magnetic data    
#i=0
#for i in range (measMat.shape[0]):
#    print "estimating the measured positions..." + str(i)
#    if (i == 0):     
#        estPosMeas = np.append(estPosMeas, estimate(p0, s0, measMat[i]))
#        estPosMeas = np.reshape(estPosMeas, (estPosMeas.size/3, 3))
#        #print "calc position nr: " + str(i) + " " + str(estPos[i])
#        #print "real position: " + str(values[i])
#    else:
#        estPosMeas = np.append(estPosMeas, estimate(estPosMeas[i-1], s0, measMat[i]))        
#        estPosMeas = np.reshape(estPosMeas, (estPosMeas.size/3, 3))
#        #print "calc position nr: " + str(i) + " " + str(estPos[i])
#        #print "real position: " + str(values[i])
#    i+=1  

"""
plot your results
"""
#plt.cla()
#f, (bfield) =  plt.subplots(1,1)
f, (bfield, pos) =  plt.subplots(1,2)
#plt.plot(values[:,0], values[:,1], color='y', label='values')
#plt.plot(values, color = 'y', label='values')
bfield.plot(resMat[:,0], linestyle='dashed', color='r', label='estX')
bfield.plot(resMat[:,1], linestyle='dashed', color='g', label='estY')
bfield.plot(resMat[:,2], linestyle='dashed', color='b', label='estZ')
#plt.axhline(max(resMat[:,0]), color='y')
#plt.axhline(max(resMat[:,1]), color='y')
#plt.axhline(max(resMat[:,2]), color='y')

bfield.plot(measMat[:,0], linestyle='solid', color='r', label='measX')
bfield.plot(measMat[:,1], linestyle='solid', color='g', label='measY')
bfield.plot(measMat[:,2], linestyle='solid', color='b', label='measZ')

pos.plot(estPosReal[:,0], estPosReal[:,1], color='r')
#pos.plot(estPosMeas[:,0], estPosMeas[:,1], color='g')

#plt.plot(estPosReal[:,0], estPosReal[:,1], color='r')
#plt.plot(estPosMeas[:,0], estPosMeas[:,1], color='g')
#plt.xlim((t[0], t[-1]))
#plt.legend()
plt.show()
                
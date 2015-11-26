''' script for estimating multiple fingers '''

import modelEqMultiCython as modE
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import *


''' collecting the data '''
cmd = "gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen"
#(meas_index,meas_middle,meas_ring,meas_pinky) = datAc.collectForTime(cmd, 10, 0.001, avgFil=False, avgN=10, 
#                                                fileName="151116_sMidRin2")
#data = datAc.pipeAcquisition(cmd, 1,measNr=201, fileName="151125_mid1")
#data = datAc.textAcquisition("151125_mid1")
#dataAvgMid = datAc.moving_average3d(data[0],10)

''' taking s0 as initial position... '''
# position of sensor
zSensor = 0.0
sInd = [-0.03, 0.0, 0.024]
sMid = [-0.03, -0.022, 0.024]
sRin = [-0.03, -0.044, 0.024]
sPin = [-0.03, -0.066, 0.024]

yInd = 0.
yMid = -0.022
yRin = -0.044
yPin = -0.066
    
    # lengths of phalanges
phalInd = [0.03080, 0.02581, 0.01678]
phalMid = [0.03593, 0.03137, 0.01684]
phalRin = [0.03404, 0.02589, 0.01820]
phalPin = [0.02892, 0.02493, 0.01601]

t = np.arange(0,1/2.*np.pi,0.01)
angles = np.zeros((len(t)*1,3))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0., 0.])
    cnt += 1

#for i in t[::-1]:
#    angles[cnt] = np.array([i, 0, 0.])
#    cnt += 1

''' calculating the B-field '''
calcBInd = np.zeros((len(angles),3))
calcBMid = np.zeros((len(angles),3))
calcBRin = np.zeros((len(angles),3))
calcBPin = np.zeros((len(angles),3))
# for moving all 4 fingers the same way...
cnt = 0
for i in angles:      
    calcBInd[cnt] = (modE.angToB(i,phalMid,sInd,yMid)+
                    modE.angToB(i,phalRin,sInd,yRin)+
                    modE.angToB(i,phalPin,sInd,yPin)+
                    modE.angToB(i,phalInd,sInd,yInd)) 
    calcBMid[cnt] = (modE.angToB(i,phalMid,sMid,yMid)+
                    modE.angToB(i,phalRin,sMid,yRin)+
                    modE.angToB(i,phalPin,sMid,yPin)+
                    modE.angToB(i,phalInd,sMid,yInd))
    calcBRin[cnt] = (modE.angToB(i,phalMid,sRin,yMid)+
                    modE.angToB(i,phalRin,sRin,yRin)+
                    modE.angToB(i,phalPin,sRin,yPin)+
                    modE.angToB(i,phalInd,sRin,yInd))
    calcBPin[cnt] = (modE.angToB(i,phalMid,sPin,yMid)+
                    modE.angToB(i,phalRin,sPin,yRin)+
                    modE.angToB(i,phalPin,sPin,yPin)+
                    modE.angToB(i,phalInd,sPin,yInd))                        
    cnt += 1

''' estimating the angles '''
bnds = ((0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP  
        (0.0,np.pi/2),
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP  
        (0.0,np.pi/2),
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP  
        (0.0,np.pi/2),
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP  
        (0.0,np.pi/2))      # DIP)      # DIP
#        
estAngCalcInd = np.zeros((len(calcBMid),3))        
estAngCalcMid = np.zeros((len(calcBMid),3))
estAngCalcRin = np.zeros((len(calcBRin),3))
estAngCalcPin = np.zeros((len(calcBRin),3))
errCnt = 0

#f = plt.figure()
#graphMid = f.add_subplot(131)
#graphMid.set_title('angle Mid')
#graphRin = f.add_subplot(132,sharey=graphMid)
#graphRin.set_title('angle Rin')
#graphPin = f.add_subplot(133,sharey=graphMid)
#graphPin.set_title('angle Pin')
#cnt = 0
print "estimating calculated"
for i in range(len(calcBMid[1:])):    
    # for one magnet and one sensor...
    res = modE.estimate_BtoAng(np.concatenate((estAngCalcInd[i],estAngCalcMid[i],estAngCalcRin[i],estAngCalcPin[i])),
                               [phalInd,phalMid,phalRin,phalPin],
                               [yInd,yMid,yRin,yPin],
                               [sInd,sMid,sRin,sPin],
                               np.concatenate((calcBInd[i+1],calcBMid[i+1],calcBRin[i+1],calcBPin[i+1])),
                                bnds)                                
    if not res.success:
        errCnt += 1
        print "error!", cnt   
    estAngCalcInd[i+1] = res.x[:3]               
    estAngCalcMid[i+1] = res.x[3:6]        
    estAngCalcRin[i+1] = res.x[6:9]
    estAngCalcPin[i+1] = res.x[9:]
    print "estimated nr: ",cnt
#    xValues = np.arange(0,i,1)
#    graphMid.clear()
#    graphRin.clear()
#    graphPin.clear()
#    graphMid.plot(xValues,estAngCalcMid[:,0][:i],'r',xValues,estAngCalcMid[:,1][:i],'g',xValues,estAngCalcMid[:,2][:i],'b',)
#    graphRin.plot(xValues,estAngCalcRin[:,0][:i],'r',xValues,estAngCalcRin[:,1][:i],'g',xValues,estAngCalcRin[:,2][:i],'b',)
#    graphPin.plot(xValues,estAngCalcPin[:,0][:i],'r',xValues,estAngCalcPin[:,1][:i],'g',xValues,estAngCalcPin[:,2][:i],'b',)
#    plt.pause(0.0001)
    cnt += 1
    
   

''' estimating angles with the fitted values '''
#print "estimating fitted"
##startTime = time.time()
#estAngMeasMid = np.zeros((len(fitMid),3))
##estAngMeasRin = np.zeros((len(fitRin),3))
#for i in range(len(fitMid[1:])):
#    res = modE.estimate_BtoAng(estAngMeasMid[i],
#                               [phalMid],
#                                [yMid],
#                                [sMid],
#                                fitMid[i+1],
#                                bnds)
#         
#    if not res.success:
#        errCnt += 1
#        print "error!", i                                  
#    estAngMeasMid[i+1] = res.x[:3]                  
##    estAngMeasRin[i+1] = res.x[3:]                  
    



#plt.close('all')
plo.plotter2d((calcBInd,calcBMid,calcBRin,calcBPin),("B-ind","B-mid","B-rin","B-pin"))
plo.plotter2d((estAngCalcInd,estAngCalcMid,estAngCalcRin,estAngCalcPin),("angles Ind","angles Mid","angles Rin","angles Pin"))
plt.show()
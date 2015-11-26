''' script for measuring and estimating the data of one single finger (index) '''

import modelEqMultiCython as modE
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import *
import time, random, subprocess

''' collecting the data '''
cmd = "gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen"
#(meas_index,meas_middle,meas_ring,meas_pinky) = datAc.collectForTime(cmd, 10, 0.001, avgFil=False, avgN=10, 
#                                                fileName="151116_sMidRin2")
#data = datAc.pipeAcquisition(cmd, 1,measNr=201, fileName="151125_mid1")
#data = datAc.textAcquisition("151125_mid1")
#dataAvgMid = datAc.moving_average3d(data[0],10)
#dataAvgMid[:,1] = 0
#dataAvgRin = datAc.moving_average3d(data[1],10)
# old scale factors...
#scaleMid = [ 5.14527643,  5.45983932,  6.35944692]
#offMid = [ 1525.65625143,   351.73604384,   811.68620046]
#scaleRin = [ 5.14240214,  4.482095,    6.18252224]
#offRin = [ 1846.48688658,   163.33697638,   -19.94990909]

#data[0] = data[0]*scaleMid+offMid
#data[1] = data[1]*scaleRin+offRin


''' taking s0 as initial position... '''
# position of sensor
zSensor = 0.0
sInd = [-0.07, 0.0, 0.0]
sMid = [-0.071, -0.022, 0.024]
sRin = [-0.071, -0.044, 0.024]
sPin = [-0.07, -0.066, 0.0]

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
#angles = np.zeros((len(t)*2,3))
angles = np.zeros((len(t),3))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0., 0.])
    cnt += 1

#for i in t[::-1]:
#    angles[cnt] = np.array([i, 0., 0.])
#    cnt += 1

''' calculating the B-field '''
#calcBInd = np.array([[0.,0.,0.]])
calcBMid = np.zeros((len(angles),3))

# for moving all 4 fingers the same way...
cnt = 0
for i in angles:           
    calcBMid[cnt] = (modE.angToB(i,phalMid,sMid,yMid))
    cnt += 1

# adding some noise...
calcBMid += np.random.normal(0,1,calcBMid.shape)


''' trimming the data '''
#filteredMid = dataAvgMid[60:150]
#fitMid = modE.fitMeasurements(calcBMid,filteredMid,(0,10))
# Middle("151116_sMid"): scale[3.85835944  0.          4.52661198]
#                       offset[1500.65699743     0.          -494.3204662 ]
# Ring("151116_sRin"): scale[ 6.47457634  10.24397007   8.14008439]
#                      offset[ 2467.8549009   1757.50418865 -1159.17110187]

#filMid = dataAvgMid[30:160]
#filRin = dataAvgRin[30:160]
#fitMid = modE.fitMeasurements(calcBMid,filMid,(0,10))
#fitRin = modE.fitMeasurements(calcBRin,filRin,(0,10))


''' estimating the angles '''
bnds = ((0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP  
        (0.0,np.pi/2))
#        (0.0,np.pi/2),      # MCP
#        (0.0,np.pi/(180/110)),      # PIP  
#        (0.0,np.pi/2))      # DIP
#        
estAngCalcMid = np.zeros((len(calcBMid),3))
#estAngCalcRin = np.zeros((len(calcBRin),3))
errCnt = 0
#cnt = 0
print "estimating calculated"
#
##fileName = "tst.txt"
##f = open(fileName,'w')
##cmd = "./../visualization/riggedAni/HandGame.blend " + fileName
##subPro = subprocess.Popen(cmd.split())
func = np.zeros((len(angles),))
startTime = time.time()
for i in range(len(calcBMid[1:])):    
    # for one magnet and one sensor...
    res = modE.estimate_BtoAng(estAngCalcMid[i],
                               [phalMid],
                               [yMid],
                               [sMid],
                               calcBMid[i+1],bnds[:3])                                
    if not res.success:
        errCnt += 1
        print "error!", cnt                  
    estAngCalcMid[i+1] = res.x[:3]
    func[i] = res.fun        
    cnt += 1
print "time needed for estimation: ",time.time()-startTime    
    
    #     sending the estimated values to the visualization
#    toSend = ("0.0000 0.0000 0.0000 " +
#                "0.0000 0.0000 0.0000 "+
#                "{0:.4f} ".format(res.x[0])+"{0:.4f} ".format(res.x[1])+"{0:.4f} ".format(res.x[2])+
#                "{0:.4f} ".format(res.x[3])+"{0:.4f} ".format(res.x[4])+"{0:.4f} ".format(res.x[5])+
#                "0.0000 0.0000 0.0000")
#                
#    f = open(fileName,'w')  
#    f.write(toSend+'\n')     
#    f.close()   
#subPro.kill()    

## initiating the subprocess
#fileName = "tst.txt"
#f = open(fileName,'w')
#cmd = "./../visualization/riggedAni/HandGame.blend " + fileName
#subPro = subprocess.Popen(cmd.split())

''' estimating angles with the fitted values '''
#print "estimating fitted"
#estAngMeasMid = np.zeros((len(fitMid),3))
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
#    estAngMeasMid[i+1] = res.x
#    
#    if not res.success:
#        print "error!", cnt
#        errCnt += 1
#    cnt += 1        

#print "estimating fitted"
#startTime = time.time()
#estAngMeasMid = np.zeros((len(data[0]),3))
#estAngMeasRin = np.zeros((len(data[1]),3))
#for i in range(len(data[0][1:])):
#    res = modE.estimate_BtoAng(np.concatenate((estAngMeasMid[i],estAngMeasRin[i])),
#                               [phalMid,phalRin],
#                                [jointMid,jointRin],
#                                [s2,s3],
#                                np.concatenate((data[0][i+1],data[1][i+1])),
#                                bnds)
#                                
#    estAngMeasMid[i+1] = res.x[:3]                  
#    estAngMeasRin[i+1] = res.x[3:]                  
#    
#    if not res.success:
#        print "error!", cnt
#        errCnt += 1
#    cnt += 1        
    
##     sending the estimated values to the visualization
#    toSend = ("0.0000 0.0000 0.0000 " +
#                "0.0000 0.0000 0.0000 "+
#                "{0:.4f} ".format(res.x[0])+"{0:.4f} ".format(res.x[1])+"{0:.4f} ".format(res.x[2])+
#                "{0:.4f} ".format(res.x[3])+"{0:.4f} ".format(res.x[4])+"{0:.4f} ".format(res.x[5])+
#                "0.0000 0.0000 0.0000")
#                
#    f = open(fileName,'w')  
#    f.write(toSend+'\n')     
#    f.close()   
#subPro.kill()    
#print "time needed: ", time.time()-startTime    

plt.close('all')
#plo.plotter2d((data[0],calcBMid,estAngCalcMid),("data","B(all in one)","angles"),shareAxis=False)
#plo.plotter2d((calcBMid,estAngCalcMid,estAngMeasMid),("B","anglesMid","anglesMeas"),shareAxis=False)
plo.plotter2d((calcBMid,estAngCalcMid),("calcB","angles"),shareAxis=False)
plt.figure()
plt.plot(func)
#plo.plotter2d((pos,orien),("Pos","orien"),shareAxis=False)
#plo.plotter2d((meas_index,calcBMid),("avg meas Mid","calc Index"),shareAxis=False)
#plo.plotter2d((estAngMeasMid,estAngCalcMid,estAngMeasRin,estAngCalcRin),("measMid","estAngCalcMid","measRin","estAngCalcRin"),shareAxis=True)
#plo.plotter2d((meas_index,),("index",))
plt.show()
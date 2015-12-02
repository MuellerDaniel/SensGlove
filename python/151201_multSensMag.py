''' script for estimation with multiple sensors per magnet '''

import dataAcquisitionMulti as datAc
import matplotlib.pyplot as plt
import modelEqMultiCython as modE
import numpy as np
from scipy.optimize import *
import plotting as plo
import time

''' acquiring the data '''
cmd = "gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen"
#d = datAc.pipeAcquisition(cmd,4,measNr=199,fileName="151202_midringpin")
d = datAc.textAcquisition("151202_midringpin")

#d_ind = datAc.moving_average3d(d[0],10)
#d_mid = datAc.moving_average3d(d[1],10)
#d_rin = datAc.moving_average3d(d[2],10)
#d_pin = datAc.moving_average3d(d[3],10)
index = datAc.moving_average3d(d[0],10)
middle = datAc.moving_average3d(d[1],10)
ring = datAc.moving_average3d(d[2],10)
pinky = datAc.moving_average3d(d[3],10)

sInd = [-0.03, -0.0, 0.024]
sMid = [-0.03, -0.022, 0.024]
sRin = [-0.03, -0.044, 0.024]
sPin = [-0.03, -0.066, 0.024]

#sInd_2 = [-0.03, 0.024]
#sMid_2 = [-0.03, 0.024]
#sRin_2 = [-0.03, 0.024]
#sPin_2 = [-0.03, 0.024]

yInd = [0.0, 0.0, -0.0]
yMid = [0.0, -0.022, -0.0]
yRin = [0.0, -0.044, -0.0]
yPin = [0.0, -0.066, -0.0]

# lengths of phalanges
phalInd = [0.03080, 0.02581, 0.01678]
phalMid = [0.03593, 0.03137, 0.01684]
phalRin = [0.03404, 0.02589, 0.01820]
phalPin = [0.02892, 0.02493, 0.01601]

t = np.arange(0,1/2.*np.pi,0.01)
#angles = np.zeros((len(t)*2,2))
angles = np.zeros((len(t),2))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0])
    cnt += 1

#for i in t[::-1]:
#    angles[cnt] = np.array([i, 0])
#    cnt += 1

''' calculating the B-field '''
sensList = [sInd,sMid,sRin,sPin]
fingerList = [phalMid,phalRin,phalPin]
yOffList = [yMid,yRin,yPin]

calcBInd_m = np.zeros((len(angles),len(sensList)*3))
#calcBInd =  np.zeros((len(angles),3))
cnt = 0
for i in angles:
#     multiple magnets and multiple sensors (just add the b-fields)
    calcBInd_m[cnt] = (modE.angToB_m2(i,phalMid,sensList,yMid)+
                         modE.angToB_m2(i,phalRin,sensList,yRin)+
                         modE.angToB_m2(i,phalPin,sensList,yPin))#+
#                         modE.angToB_m2(np.array([0.,0.,0.]),phalPin,sensList,yPin))
    cnt += 1

# adding some noise...
#calcBInd_m += np.random.normal(0,1,calcBInd_m.shape)

''' fitting the measurements '''
#index = d_ind[10:100]
#middle = d_mid[10:100]
#ring = d_rin[10:100]
#pinky = d_pin[10:100]
#
#index = modE.fitMeasurements(calcBInd_m[:,:3],index,(0,10))[10:]
#middle = modE.fitMeasurements(calcBInd_m[:,3:6],middle,(0,10))[10:]
#ring = modE.fitMeasurements(calcBInd_m[:,6:9],ring,(0,10))[10:]
#pinky = modE.fitMeasurements(calcBInd_m[:,9:],pinky,(0,10))[10:]
#
#measB = np.zeros((len(index),3*len(sensList)))
#measB[:,0:3] = index
#measB[:,3:6] = middle
#measB[:,6:9] = ring
#measB[:,9:] = pinky

#index = d_ind[10:40]
#middle = d_mid[10:100]
#ring = d_rin[10:100]
#pinky = d_pin[10:100]

#index = modE.fitMeasurements(calcBInd_m[:,:3],index,(0,10))[10:]
#middle = modE.fitMeasurements(calcBInd_m[:,3:6],middle,(0,10))[10:]
#ring = modE.fitMeasurements(calcBInd_m[:,6:9],ring,(0,10))[10:]
#pinky = modE.fitMeasurements(calcBInd_m[:,9:],pinky,(0,10))[10:]

scaleInd = [0.36462151,  0.,          0.35546784]
offInd = [101.9832471 ,    0. ,          -6.69879091]
scaleMid = [0.35913999,  0.   ,       0.39066646]
offMid = [80.23952749,   0.  ,        12.18912481]
scaleRin = [0.35825034 , 0.    ,      0.37539817]
offRin = [111.94372244  ,  0.    ,      -32.14775172]
scalePin = [0.37584881 , 0.    ,      0.32751091]
offPin = [ 145.20063789  ,  0.    ,      -75.24422619]
index = index*scaleInd+offInd
middle = middle*scaleMid+offMid
ring = ring*scaleRin+offRin
pinky = pinky*scalePin+offPin

measB = np.zeros((len(index),3*len(sensList)))
measB[:,0:3] = index
measB[:,3:6] = middle
measB[:,6:9] = ring
measB[:,9:] = pinky

''' estimation '''
bnds = ((0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP
        #(0.0,np.pi/2),
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP
        #(0.0,np.pi/2),
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP
        #(0.0,np.pi/2),
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),)      # PIP
        #(0.0,np.pi/2))

### perfect values
#func = np.zeros((len(angles),))
#estAng = np.zeros((len(angles),len(fingerList)*2))
#cnt = 0
#errCnt = 0
#startTime = time.time()
#for i in range(len(calcBInd_m[1:])):
#    res = modE.estimate_BtoAng(estAng[cnt],fingerList,yOffList,sensList,calcBInd_m[cnt+1],bnds[:2])
#
#    if not res.success:
#        print "error, iter: ",cnt
#        errCnt += 1
#    estAng[cnt+1] = res.x
#    func[cnt] = res.fun
#    print "estimating ",cnt
#    cnt += 1
#print "time  needed for estimation: ", time.time()-startTime

## fitted values
errCnt2 = 0
estAngMeas = np.zeros((len(measB),2*len(fingerList)))
#estAngMeas = np.zeros((len(measB),3))
startTime = time.time()
for i in range(len(measB[1:])):
    print "estimating fitted",i
#    res = modE.estimate_BtoAng(estAngMeas[i],fingerList,yOffList,sensList,measB[i+1][3:6],bnds[:3])
    res = modE.estimate_BtoAng(estAngMeas[i],fingerList,yOffList,sensList,measB[i+1],bnds[:6])
    
    if not res.success:
        print "error, iter: ",i
        print res
        errCnt2 += 1
    estAngMeas[i+1] = res.x
print "time needed for estimation: ", time.time()-startTime    

#plt.close('all')
#plo.plotter2d((calcBInd_m[:,:3],calcBInd_m[:,3:6],calcBInd_m[:,6:9],calcBInd_m[:,9:]),("sInd","sMid","sRin","sPin"))
#plo.plotter2d((d_ind,d_mid,d_rin,d_pin),("measInd","measMid","measRin","measPin"))
plo.plotter2d((calcBInd_m[:,:3],index),("ind","measInd"),shareAxis=True)
plo.plotter2d((calcBInd_m[:,3:6],middle),("mid","measMid"),shareAxis=True)
plo.plotter2d((calcBInd_m[:,6:9],ring),("rin","measRin"),shareAxis=True)
plo.plotter2d((calcBInd_m[:,9:],pinky),("pin","measPin"),shareAxis=True)
#plt.figure()
#plt.plot(estAng[:,0],'r')
#plt.plot(estAng[:,1],'g')
#plt.plot(estAng[:,1]*2/3,'b')


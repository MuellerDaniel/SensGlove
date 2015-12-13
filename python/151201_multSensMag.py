''' script for estimation with multiple sensors per magnet '''

import dataAcquisitionMulti as datAc
import matplotlib.pyplot as plt
import modelEqMultiCython as modE
import numpy as np
from scipy.optimize import *
import plotting as plo
import time,random

''' acquiring the data '''
cmd = "gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen"
#d = datAc.pipeAcquisition(cmd,4,measNr=199,fileName="151209_four")
d = datAc.textAcquisition("151209_index2")
#d = datAc.collectForTime(cmd,5,wait=0)

#d_ind = datAc.moving_average3d(d[0],10)
#d_mid = datAc.moving_average3d(d[1],10)
#d_rin = datAc.moving_average3d(d[2],10)
#d_pin = datAc.moving_average3d(d[3],10)
index = datAc.moving_average3d(d[0],10)
middle = datAc.moving_average3d(d[1],10)
ring = datAc.moving_average3d(d[2],10)
pinky = datAc.moving_average3d(d[3],10)

#index = np.delete(index,np.s_[1],1)
#middle = np.delete(middle,np.s_[1],1)
#ring = np.delete(ring,np.s_[1],1)
#pinky = np.delete(pinky,np.s_[1],1)

sInd = [-0.03, -0.0, 0.024]     # rack1
sMid = [-0.03, -0.022, 0.024]
sRin = [-0.03, -0.044, 0.024]
sPin = [-0.03, -0.066, 0.024]
#sInd = [-0.03, -0.0, 0.024]     # rack2
#sMid = [-0.05, -0.022, 0.024]
#sRin = [-0.03, -0.044, 0.024]
#sPin = [-0.05, -0.066, 0.024]

yInd = [0.0, 0.0, -0.0]
yMid = [0.0, -0.022, 0.002]
yRin = [0.0, -0.044, 0.002]
yPin = [0.0, -0.066, -0.0]

# lengths of phalanges
phalInd = [0.03080, 0.02581, 0.01678]
phalMid = [0.03593, 0.03137, 0.01684]
phalRin = [0.03404, 0.02589, 0.01820]
phalPin = [0.02892, 0.02493, 0.01601]

t = np.arange(0,1/2.*np.pi,0.01)
#t = np.arange(0,np.pi*(110./180.),0.01)
#angles = np.zeros((len(t)*2,3))
angles = np.zeros((len(t),3))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0, 0])
    cnt += 1

#for i in t[::-1]:
#    angles[cnt] = np.array([i, 0, 0])
#    cnt += 1

''' calculating the B-field '''
sensList = [sInd,sMid,sRin,sPin]
#sensList = [sInd_2]
fingerList = [phalInd]
yOffList = [yInd]

calcBInd_m = np.zeros((len(angles),len(sensList)*3))
#calcBInd =  np.zeros((len(angles),3))
cnt = 0
for i in angles:
#     multiple magnets and multiple sensors (just add the b-fields)
    calcBInd_m[cnt] = (modE.angToB_m2(i,phalInd,sensList,yInd))#+
#                         modE.angToB_m2(i,phalMid,sensList,yMid)+
#                         modE.angToB_m2(i,phalRin,sensList,yRin)+
#                         modE.angToB_m2(i,phalPin,sensList,yPin))
    cnt += 1

# adding some noise...
#calcBInd_m += np.random.normal(0,1,calcBInd_m.shape)

''' fitting the measurements '''
#index = d_ind[10:100]
#middle = d_mid[10:100]
#ring = d_rin[10:100]
#pinky = d_pin[10:100]

#index = modE.fitMeasurements(calcBInd_m[:,:3],index,(0,10))[10:]
#middle = modE.fitMeasurements(calcBInd_m[:,3:6],middle,(0,10))[10:]
#ring = modE.fitMeasurements(calcBInd_m[:,6:9],ring,(0,10))[10:]
#pinky = modE.fitMeasurements(calcBInd_m[:,9:],pinky,(0,10))[10:]

(scaleInd,offInd) = modE.getScaleOff(calcBInd_m[:,:3],index)
(scaleMid,offMid) = modE.getScaleOff(calcBInd_m[:,3:6],middle)
(scaleRin,offRin) = modE.getScaleOff(calcBInd_m[:,6:9],ring)
(scalePin,offPin) = modE.getScaleOff(calcBInd_m[:,9:],pinky)

#(scaleInd,offInd) = ([ 0.30282884 , 0.    ,      0.34976132], [ 88.57037195   ,0.,           9.87133819])
#(scaleMid,offMid) = ([ 0.29291524 , 0.   ,       0.38527667] ,[ 79.1614863    ,0. ,         20.70100158])
#(scaleRin,offRin) = ([ 0.27814136 , 0.  ,        0.38388733] ,[ 107.77864367  ,  0.,           14.60548782])
#(scalePin,offPin) = ([ 0.27829422 , 0. ,         0.37379545] ,[ 124.56965979 ,   0. ,         -42.52921605])

#(scaleInd,offInd) = ([1,0,1], [ 0,0,0])
#(scaleMid,offMid) = ([1,0,1], [ 0,0,0])
#(scaleRin,offRin) = ([1,0,1], [ 0,0,0])
#(scalePin,offPin) = ([1,0,1], [ 0,0,0])

measB = np.zeros((len(index[10:]),3*len(sensList)))
measB[:,0:3] = index[10:]*scaleInd+offInd
measB[:,3:6] = middle[10:]*scaleMid+offMid
measB[:,6:9] = ring[10:]*scaleRin+offRin
measB[:,9:] = pinky[10:]*scalePin+offPin

#index = d_ind[10:40]
#middle = d_mid[10:100]
#ring = d_rin[10:100]
#pinky = d_pin[10:100]

#index = modE.fitMeasurements(calcBInd_m[:,:3],index,(0,10))[10:]
#middle = modE.fitMeasurements(calcBInd_m[:,3:6],middle,(0,10))[10:]
#ring = modE.fitMeasurements(calcBInd_m[:,6:9],ring,(0,10))[10:]
#pinky = modE.fitMeasurements(calcBInd_m[:,9:],pinky,(0,10))[10:]

''' estimation '''
bnds = ((0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180./110.)),      # PIP
#        (0.0,np.pi/2),
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180./110.)),      # PIP
#        (0.0,np.pi/2),
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180./110.)),      # PIP
        #(0.0,np.pi/2),
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180./110.)),)      # PIP
        #(0.0,np.pi/2))

### perfect values
#func = np.zeros((len(angles),))
#estAng = np.zeros((len(angles),len(fingerList)*2))
#cnt = 0
#errCnt = 0
#startTime = time.time()
#for i in range(len(calcBInd_m[1:])):
#    res = modE.estimate_BtoAng(estAng[cnt],fingerList,yOffList,sensList,calcBInd_m[cnt+1],bnds[:len(fingerList)*2],method='cy')
##    res = modE.estimate_BtoAng(estAng[cnt],fingerList,yOffList,sensList,calcBInd_m[cnt+1],method='py')
#
#    if res[2]['warnflag']:
#        print "error, iter: ",cnt
#        errCnt += 1
#        print res[2]['warnflag']
#        # estAng[cnt+1] = np.zeros((len(fingerList)*2,))
#    # else:
#    # estAng[cnt+1] = res[0]
#    # func[cnt] = res[1]
#    # if res[-1]:
#    #     print "error, iter: ",cnt
#    #     print res[-1]
#    #     errCnt += 1
#    estAng[cnt+1] = res[0]
#    func[cnt] = res[1]
#    print "estimating ",cnt
#    cnt += 1
#print "time  needed for estimation: ", time.time()-startTime
#print "errCnt: ", errCnt
#print "max func: ", max(func)

## fitted values
errCnt2 = 0
estAngMeas = np.zeros((len(measB),2*len(fingerList)))
funcMeas = np.zeros((len(measB),))
startTime = time.time()
for i in range(len(measB[1:])):
   print "estimating fitted",i
#    res = modE.estimate_BtoAng(estAngMeas[i],fingerList,yOffList,sensList,measB[i+1][3:6],bnds[:3])
   res = modE.estimate_BtoAng(estAngMeas[i],fingerList,yOffList,sensList,measB[i+1],bnds[:len(fingerList)*2],method='cy')
#   if not res.success:
   if res[2]['warnflag']:
       print "error, iter: ",i
       print res
       errCnt2 += 1
#        estAngMeas[i+1] = estAngMeas[i]

#   estAngMeas[i+1] = res.x
   estAngMeas[i+1] = res[0]
   funcMeas[i] = res[1]

print "time needed for estimation: ", time.time()-startTime
print "nr of errors: ", errCnt2
print "maxFunc: ", max(funcMeas)

''' recalculate the B-field with the estimated angles '''
estCalcB = np.zeros((len(estAngMeas),len(sensList)*3))
cnt = 0
for i in estAngMeas:
    for j in range(len(fingerList)):
        estCalcB[cnt] += modE.angToB_m2(np.array([i[j*2],i[j*2+1]]),fingerList[j],sensList,yOffList[j])
    cnt += 1
dif = measB-estCalcB


plt.close('all')
#plo.plotter2d((calcBInd_m[:,:3],calcBInd_m[:,3:6],calcBInd_m[:,6:9],calcBInd_m[:,9:]),("sInd","sMid","sRin","sPin"))
#plo.plotter2d((d_ind,d_mid,d_rin,d_pin),("measInd","measMid","measRin","measPin"))
plo.plotter2d((calcBInd_m[:,:3],measB[:,:3],estCalcB[:,:3]),("ind","measInd","estInd"),shareAxis=True)
plo.plotter2d((calcBInd_m[:,3:6],measB[:,3:6],estCalcB[:,3:6]),("mid","measMid","estMid"),shareAxis=True)
plo.plotter2d((calcBInd_m[:,6:9],measB[:,6:9],estCalcB[:,6:9]),("rin","measRin","estRin"),shareAxis=True)
plo.plotter2d((calcBInd_m[:,9:],measB[:,9:],estCalcB[:,9:]),("pin","measPin","estPin"),shareAxis=True)

plo.plotter2d((dif[:,:3],dif[:,3:6],dif[:,6:9],dif[:,9:]),("difInd","difMid","difRin","difPin"))
#plt.figure()
#plt.plot(estAng[:,0],'r')
#plt.plot(estAng[:,1],'g')
#plt.plot(estAng[:,2],'b')
# plt.title('perfectB')
plt.figure()
plt.plot(estAngMeas[:,0],'r')
plt.plot(estAngMeas[:,1],'g')
plt.plot(estAngMeas[:,1]*(2./3.),'b')
plt.title('index')
#plt.figure()
#plt.plot(estAngMeas[:,2],'r')
#plt.plot(estAngMeas[:,3],'g')
#plt.plot(estAngMeas[:,3]*(2./3.),'b')
#plt.title('middle')
#plt.figure()
#plt.plot(estAngMeas[:,4],'r')
#plt.plot(estAngMeas[:,5],'g')
#plt.plot(estAngMeas[:,5]*(2./3.),'b')
#plt.title('ring')
#plt.figure()
#plt.plot(estAngMeas[:,6],'r')
#plt.plot(estAngMeas[:,7],'g')
#plt.plot(estAngMeas[:,7]*(2./3.),'b')
#plt.title('pinky')
print scaleInd,offInd
print scaleMid,offMid
print scaleRin,offRin
print scalePin,offPin
#plt.plot(estAng[:,2],'b')
#plt.plot(estAng[:,3],'y')
plt.show()

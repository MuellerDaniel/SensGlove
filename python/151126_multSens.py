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
#d = datAc.pipeAcquisition(cmd,4,measNr=199,fileName="151201_onefour1")
d = datAc.textAcquisition("151201_onefour1")

d_ind = datAc.moving_average3d(d[0],10)
d_mid = datAc.moving_average3d(d[1],10)
d_rin = datAc.moving_average3d(d[2],10)
d_pin = datAc.moving_average3d(d[3],10)


sInd = [-0.03, -0.0, 0.024]
sMid = [-0.03, -0.022, 0.024]
sRin = [-0.03, -0.044, 0.024]
sPin = [-0.03, -0.066, 0.024]

sInd2 = [-0.07, 0.0, 0.024]
sMid2 = [-0.07, -0.022, 0.024]
sRin2 = [-0.07, -0.044, 0.024]
sPin2 = [-0.07, -0.066, 0.024]

yInd = [0.0, 0.0, -0.01]
yMid = [0.0, -0.022, -0.01]
yRin = [0.0, -0.044, -0.01]
yPin = [0.0, -0.066, -0.01]

# lengths of phalanges
phalInd = [0.03080, 0.02581, 0.01678]
phalMid = [0.03593, 0.03137, 0.01684]
phalRin = [0.03404, 0.02589, 0.01820]
phalPin = [0.02892, 0.02493, 0.01601]

t = np.arange(0,1/2.*np.pi,0.01)
angles = np.zeros((len(t)*2,3))
#angles = np.zeros((len(t),3))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0., 0.])
    cnt += 1

for i in t:
    angles[cnt] = np.array([t[-1], i, 0.])
    cnt += 1

''' calculating the B-field '''
sensList = [sInd,sMid,sRin,sPin]
fingerList = [phalMid]
yOffList = [yMid]

calcBInd_m = np.zeros((len(angles),len(sensList)*3))
#calcBInd =  np.zeros((len(angles),3))
cnt = 0
for i in angles:
#    calcBInd[cnt] = modE.angToB(i,phalMid,sMid,yMid)
#     multiple magnets and multiple sensors (just add the b-fields)
    calcBInd_m[cnt] = (modE.angToB_m(i,phalMid,sensList,yMid))#+
#                         modE.angToB_m(i,phalRin,sensList,yRin)+
#                         modE.angToB_m(i,phalPin,sensList,yPin)+
#                         modE.angToB_m(i,phalInd,sensList,yInd))
    cnt += 1

# adding some noise...
#calcBInd_m += np.random.normal(0,1,calcBInd_m.shape)

''' fitting the measurements '''
# for 151130_onefour
#d_ind = d_ind[15:140]
#d_mid = d_mid[15:140]
#d_rin = d_rin[15:140]
#d_pin = d_pin[15:140]
#
#index = modE.fitMeasurements(calcBInd_m[:,:3],d_ind,(0,10))[10:]
#middle = modE.fitMeasurements(calcBInd_m[:,3:6],d_mid,(0,10))[10:]
#ring = modE.fitMeasurements(calcBInd_m[:,6:9],d_rin,(0,10))[10:]
#pinky = modE.fitMeasurements(calcBInd_m[:,9:],d_pin,(0,10))[10:]
#
#measB = np.zeros((len(index),3*len(sensList)))
#measB[:,0:3] = index
#measB[:,3:6] = middle
#measB[:,6:9] = ring
#measB[:,9:] = pinky


# for 151130_onefour1
#d_ind = d_ind[10:110]
#d_mid = d_mid[10:110]
#d_rin = d_rin[10:110]
#d_pin = d_pin[10:110]
#
#d_indF = modE.fitMeasurements(calcBInd_m[:,:3],d_ind,(0,10))[10:]
#d_midF = modE.fitMeasurements(calcBInd_m[:,3:6],d_mid,(0,10))[10:]
#d_rinF = modE.fitMeasurements(calcBInd_m[:,6:9],d_rin,(0,10))[10:]
#d_pinF = modE.fitMeasurements(calcBInd_m[:,9:],d_pin,(0,10))[10:]

# delete the resting phase
#index = d_indF[:25]
#index = np.append(index,d_indF[65:],axis=0)
#middle = d_midF[:25]
#middle = np.append(middle,d_midF[65:],axis=0)
#ring = d_rinF[:25]
#ring = np.append(ring,d_rinF[65:],axis=0)
#pinky = d_pinF[:25]
#pinky = np.append(pinky,d_pinF[65:],axis=0)


# for 151130_onefour2
#d_ind = d_ind[10:120]
#d_mid = d_mid[10:120]
#d_rin = d_rin[10:120]
#d_pin = d_pin[10:120]
#
#index = modE.fitMeasurements(calcBInd_m[:,:3],d_ind,(0,10))[10:]
#middle = modE.fitMeasurements(calcBInd_m[:,3:6],d_mid,(0,10))[10:]
#ring = modE.fitMeasurements(calcBInd_m[:,6:9],d_rin,(0,10))[10:]
#pinky = modE.fitMeasurements(calcBInd_m[:,9:],d_pin,(0,10))[10:]

# delete the resting phase
#index = d_indF[:40]
#index = np.append(index,d_indF[60:],axis=0)
#middle = d_midF[:40]
#middle = np.append(middle,d_midF[60:],axis=0)
#ring = d_rinF[:40]
#ring = np.append(ring,d_rinF[60:],axis=0)
#pinky = d_pinF[:40]
#pinky = np.append(pinky,d_pinF[60:],axis=0)




#measB = np.zeros((len(index),3*len(sensList)))
#measB[:,0:3] = index
#measB[:,3:6] = middle
#measB[:,6:9] = ring
#measB[:,9:] = pinky


''' estimation '''
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
        (0.0,np.pi/2))

### perfect values
func = np.zeros((len(angles),))
estAng = np.zeros((len(angles),len(fingerList)*2))
cnt = 0
errCnt = 0
startTime = time.time()
for i in range(len(calcBInd_m[1:])):
    res = modE.estimate_BtoAng(estAng[cnt],fingerList,yOffList,sensList,calcBInd_m[cnt+1],bnds[:2])

    if not res.success:
        print "error, iter: ",cnt
        errCnt += 1
    estAng[cnt+1] = res.x
    func[cnt] = res.fun
    print "estimating ",cnt
    cnt += 1
print "time  needed for estimation: ", time.time()-startTime

## fitted values
#errCnt2 = 0
#estAngMeas = np.zeros((len(measB),2*len(fingerList)))
##estAngMeas = np.zeros((len(measB),3))
#startTime = time.time()
#for i in range(len(measB[1:])):
##    print "estimating ",i
##    res = modE.estimate_BtoAng(estAngMeas[i],fingerList,yOffList,sensList,measB[i+1][3:6],bnds[:3])
#    res = modE.estimate_BtoAng(estAngMeas[i],fingerList,yOffList,sensList,measB[i+1],bnds[:2])
#    
#    if not res.success:
#        print "error, iter: ",i
#        print res
#        errCnt2 += 1
#    estAngMeas[i+1] = np.array([res.x[0], res.x[1]])
#print "time needed for estimation: ", time.time()-startTime    


#sens_I = calcBInd[:,0:3]
plt.close('all')
#plt.figure()
#plo.plotter2d((calcBInd_m,),("sMid_m",))
plo.plotter2d((calcBInd_m[:,:3],calcBInd_m[:,3:6],calcBInd_m[:,6:9],calcBInd_m[:,9:]),("sInd","sMid","sRin","sPin"))
#plo.plotter2d((d_ind,d_mid,d_rin,d_pin),("measInd","measMid","measRin","measPin"))
#plo.plotter2d((calcBInd_m[:,:3],index),("ind","measInd"),shareAxis=True)
#plo.plotter2d((calcBInd_m[:,3:6],middle),("mid","measMid"),shareAxis=True)
#plo.plotter2d((calcBInd_m[:,6:9],ring),("rin","measRin"),shareAxis=True)
#plo.plotter2d((calcBInd_m[:,9:],pinky),("pin","measPin"),shareAxis=True)
plt.figure()
plt.plot(estAng[:,0])
plt.plot(estAng[:,1])
plt.plot(estAng[:,1]*(2/3))
#plo.plotter2d((estAngMeas,angles),("meas estAngles","perfect estAng"))
#plo.plotter2d((estAngMeas[:,:3],estAngMeas[:,3:6],estAngMeas[:,6:9],estAngMeas[:,9:]),("estInd","estMid","estRin","estPin"))
#plo.plotter2d((estAng[:,:3],estAng[:,3:]),("mid","rin"))
#plt.figure()
#plo.plotter2d((estAngMeas[:,:3],),("estAnglesMid",))
#plt.plot(np.arange(0,np.pi/2,np.pi/2/len(estAngMeas)))
#plt.plot(angles[:,0])
#plt.figure()
#dif = angles[:,0]-estAngMeas[:,0]
#print "max abs difference: ", max(abs(dif))
#print "mean dif: ", np.mean(abs(dif))
#plt.plot(dif)
#plt.show()

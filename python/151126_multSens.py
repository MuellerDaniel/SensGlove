''' script for estimation with multiple sensors per magnet '''

import dataAcquisitionMulti as datAc
import matplotlib.pyplot as plt
import modelEqMultiCython as modE
import numpy as np
from scipy.optimize import *
import plotting as plo
import time

sInd = [-0.03, 0.0, 0.024]
sMid = [-0.03, -0.022, 0.024]
sRin = [-0.03, -0.044, 0.024]
sPin = [-0.03, -0.066, 0.024]
sInd2 = [-0.07, 0.0, 0.024]
sMid2 = [-0.07, -0.022, 0.024]
sRin2 = [-0.07, -0.044, 0.024]
sPin2 = [-0.07, -0.066, 0.024]

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
#    angles[cnt] = np.array([i, 0, 0.])
#    cnt += 1

''' calculating the B-field '''
sensList = [sInd,sMid,sRin,sPin,sInd2,sMid2,sRin2,sPin2]
fingerList = [phalInd,phalPin]
yOffList = [yInd,yPin]

calcBInd_m = np.zeros((len(angles),len(sensList)*3))
cnt = 0
for i in angles:
    # ONE magnet and multiple sensors
#    calcBInd_m[cnt] = modE.angToB_m(i,phalInd,sensList,yInd)
#     multiple magnets and multiple sensors (just add the b-fields)
    calcBInd_m[cnt] = (modE.angToB_m(i,phalInd,sensList,yInd)+
                         modE.angToB_m(i,phalPin,sensList,yPin))#+
                        # modE.angToB_m(i,phalRin,sensList,yRin)+
                        # modE.angToB_m(i,phalPin,sensList,yPin))
    cnt += 1

# adding some noise...
calcBInd_m += np.random.normal(0,1,calcBInd_m.shape)

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


func = np.zeros((len(angles),))
estAng = np.zeros((len(angles),len(fingerList)*3))
cnt = 0
errCnt = 0
startTime = time.time()
for i in range(len(calcBInd_m[1:])):
    # playing around with the estimation for ONE magnet and several sensors...
#    res = modE.estimate_BtoAng(estAng[cnt],[phalInd],[yInd],sensList,calcBInd_m[cnt+1],bnds[:3])
#    res = modE.estimate_BtoAng(estAng[cnt],[phalInd],[yInd],sensList[:1],calcBInd[cnt+1][:3],bnds)
    # playing around with the estimation for several magnets and several sensors...
    res = modE.estimate_BtoAng(estAng[cnt],fingerList,yOffList,sensList,calcBInd_m[cnt+1],bnds[:6])

    if not res.success:
        print "error, iter: ",cnt
        errCnt += 1
#    func[cnt] = res.fun
    estAng[cnt+1] = res.x
    print "estimating ",cnt
    cnt += 1
print "time  needed for estimation: ", time.time()-startTime
#a = modE.funcMagY_angle_m(estAng[0],fingerList,sensList,yOffList,calcBInd_m[0])
#print a


#sens_I = calcBInd[:,0:3]
#plt.close('all')
#plo.plotter2d((calcBInd_m[:,0:3],),("sInd",))
plo.plotter2d((calcBInd_m[:,:3],calcBInd_m[:,3:6],calcBInd_m[:,6:9],calcBInd_m[:,9:]),("sInd","sMid","sRin","sPin"))
plt.figure()
plo.plotter2d((estAng[:,:3],estAng[:,3:6]),("estAnglesInd","estAngles2"))
#plt.plot(angles[:,0])
#plt.figure()
#dif = angles[:,0]-estAng[:,0]
#print "max abs difference: ", max(abs(dif))
#print "mean dif: ", mean(abs(dif))
#plt.plot(dif)
plt.show()

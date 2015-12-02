import dataAcquisitionMulti as datAc
import matplotlib.pyplot as plt
import modelEqMultiCython as modE
import numpy as np
from scipy.optimize import *
import plotting as plo
import time,subprocess

cmd = "gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen"


sInd = [-0.04, 0.0, 0.024]
sMid = [-0.04, -0.022, 0.024]
sRin = [-0.04, -0.044, 0.024]
sPin = [-0.04, -0.066, 0.024]

yInd = [0.0, 0.0, -0.0]
yMid = [0.0, -0.022, -0.0]
yRin = [0.0, -0.044, -0.0]
yPin = [0.0, -0.066, -0.0]

# lengths of phalanges
phalInd = [0.03080, 0.02581, 0.01678]
phalMid = [0.03593, 0.03137, 0.01684]
phalRin = [0.03404, 0.02589, 0.01820]
phalPin = [0.02892, 0.02493, 0.01601]
                           
data = np.array([[0,0.,0.,0.],
                 [1,0.,0.,0.],
                 [2,0.,0.,0.],
                 [3,0.,0.,0.]])
                 
                 
t = np.zeros((4,4))  

''' calibration process '''
calDat = datAc.pipeAcquisition(cmd,4)

t = np.arange(0,1/2.*np.pi,0.01)
angles = np.zeros((len(t),2))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0])
    cnt += 1

# calculating the B-field
sensList = [sInd,sMid,sRin,sPin]

calcBInd_m = np.zeros((len(angles),len(sensList)*3))
cnt = 0
for i in angles:
    calcBInd_m[cnt] = (modE.angToB_m2(i,phalMid,sensList,yMid))#+
#                         modE.angToB_m2(i,phalRin,sensList,yRin)+
#                         modE.angToB_m2(i,phalPin,sensList,yPin))#+
#                         modE.angToB_m2(np.array([0.,0.,0.]),phalPin,sensList,yPin))
    cnt += 1

filInd = datAc.moving_average3d(calDat[0],1)
filMid = datAc.moving_average3d(calDat[1],1)
filRin = datAc.moving_average3d(calDat[2],1)
filPin = datAc.moving_average3d(calDat[3],1)

#(scaleInd,offInd) = modE.getScaleOff(calcBInd_m[:,0:3],calDat[0][10:])
#(scaleMid,offMid) = modE.getScaleOff(calcBInd_m[:,3:6],calDat[1][10:])
#(scaleRin,offRin) = modE.getScaleOff(calcBInd_m[:,6:9],calDat[2][10:])
#(scalePin,offPin) = modE.getScaleOff(calcBInd_m[:,9:12],calDat[3][10:])

(scaleInd,offInd) = modE.getScaleOff(calcBInd_m[:,0:3],filInd[10:])
(scaleMid,offMid) = modE.getScaleOff(calcBInd_m[:,3:6],filMid[10:])
(scaleRin,offRin) = modE.getScaleOff(calcBInd_m[:,6:9],filRin[10:])
(scalePin,offPin) = modE.getScaleOff(calcBInd_m[:,9:12],filPin[10:])

#index = calDat[0]*scaleInd+offInd
#middle = calDat[1]*scaleMid+offMid
#ring = calDat[2]*scaleRin+offRin
#pinky = calDat[3]*scalePin+offPin

#plo.plotter2d((calcBInd_m[:,:3],index,calDat[0]),("index","index","measInd"))
#plo.plotter2d((calcBInd_m[:,3:6],middle,calDat[1]),("index","middle","measMid"))
#plo.plotter2d((calcBInd_m[:,6:9],ring,calDat[2]),("index","ring","measRin"))
#plo.plotter2d((calcBInd_m[:,9:],pinky,calDat[3]),("index","Pinky","measPin"))


''' RT estimation '''
procBle = subprocess.Popen("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen".split(), 
                           stdout=subprocess.PIPE, close_fds=True)
                           
bnds = ((0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP  
        #(0.0,np.pi/2),
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP  
        #(0.0,np.pi/2))      # DIP
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),)      # PIP  
        #(0.0,np.pi/2))      # DIP
        
estAngMeas = np.array([[0.,0.]])  
fval = np.array([0.])        
cnt = 0
errCnt = 0
     
index = np.array([[0.,0.,0.]])
middle = np.array([[0.,0.,0.]])
ring = np.array([[0.,0.,0.]])
pinky = np.array([[0.,0.,0.]])
     
fileName = "tst.txt"
f = open(fileName,'w')
toSend = ("0.0000 0.0000 0.0000 " +
        "0.0000 0.0000 0.0000 " +
        "0.0000 0.0000 0.0000 " +
        "0.0000 0.0000 0.0000 " +
        "0.0000 0.0000 0.0000")
f.write(toSend+'\n')                    
f.close()

blendCmd = "./../visualization/riggedAni/HandGame.blend " + fileName
subProBlend = subprocess.Popen(blendCmd.split())
                 
try:
    while True:
        print "cnt: ",cnt
        data = datAc.RTdata(data,procBle)              

        index = np.append(index,[data[0][1:]*scaleInd+offInd],axis=0)
        middle = np.append(middle,[data[1][1:]*scaleMid+offMid],axis=0)        
        ring = np.append(ring,[data[2][1:]*scaleRin+offRin],axis=0)
        pinky = np.append(pinky,[data[3][1:]*scalePin+offPin],axis=0)
        
        if len(index) > 10:
            print "here"
            res = modE.estimate_BtoAng(estAngMeas[-1],
                                       [phalMid],
                                        [yMid],
                                        [sInd,sMid,sRin,sPin],
                                        np.concatenate((index[-1],middle[-1],ring[-1],pinky[-1])),
                                        bnds[:2])        
#        
##        time.sleep(0.05) 
            if not res.success:
                print "no solution..."  
                errCnt += 1
#            estAngMeas = np.append(estAngMeas,[[0.,0.,0.]],axis=0)
#        else:
            estAngMeas = np.append(estAngMeas,[res.x],axis=0)
            fval = np.append(fval,res.fun)
#        time.sleep(0.1)
            cnt += 1
            #     sending the estimated values to the visualization
            toSend = ("0.0000 0.0000 0.0000 " +
                        "0.0000 0.0000 0.0000 " +
                        "{0:.4f} ".format(res.x[0])+"{0:.4f} ".format(res.x[1])+"{0:.4f} ".format(res.x[1]*(2/3))+
                        "0.0000 0.0000 0.0000 " +
                        "0.0000 0.0000 0.0000")
                        
            f = open(fileName,'a')  
            f.write(toSend+'\n')     
            print toSend
            f.close()   
    
        
        
except KeyboardInterrupt:
    print "ended, cnt: ", cnt
    subProBlend.kill()    
    procBle.kill()          
    plo.plotter2d((index[10:],middle[10:],ring[10:],pinky[10:]),("ind","mid","rin","pinky"))
    plt.figure()
    plt.plot(estAngMeas[:,0],'r')
    plt.plot(estAngMeas[:,1],'g')
    
    
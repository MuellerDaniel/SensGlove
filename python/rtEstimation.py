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
                 
collected = np.array([[0.,0.,0.],
                     [0.,0.,0.],
                     [0.,0.,0.],
                     [0.,0.,0.]])                 
                 
                 
t = np.zeros((4,4))  

''' calibration process '''
calDat = datAc.pipeAcquisition(cmd,4)

t = np.arange(0,1/2.*np.pi,0.01)
angles = np.zeros((len(t),3))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0, 0])
    cnt += 1

# calculating the B-field
sensList = [sInd,sMid,sRin,sPin]

calcBInd_m = np.zeros((len(angles),len(sensList)*3))
cnt = 0
for i in angles:
    calcBInd_m[cnt] = (modE.angToB_m2(i,phalMid,sensList,yMid)+
                        modE.angToB_m2(i,phalRin,sensList,yRin)+
                         modE.angToB_m2(i,phalPin,sensList,yPin))#+
#                         modE.angToB_m2(np.array([0.,0.,0.]),phalPin,sensList,yPin))
    cnt += 1

filInd = datAc.moving_average3d(calDat[0],1)
filMid = datAc.moving_average3d(calDat[1],1)
filRin = datAc.moving_average3d(calDat[2],1)
filPin = datAc.moving_average3d(calDat[3],1)

(scaleInd,offInd) = modE.getScaleOff(calcBInd_m[:,0:3],filInd[20:])
(scaleMid,offMid) = modE.getScaleOff(calcBInd_m[:,3:6],filMid[20:])
(scaleRin,offRin) = modE.getScaleOff(calcBInd_m[:,6:9],filRin[20:])
(scalePin,offPin) = modE.getScaleOff(calcBInd_m[:,9:12],filPin[20:])

#scaleInd = [ 0.27411365 , 0.        ,  0.3475002 ]
#offInd = [ 102.08140103  ,  0.        ,   -4.4541138 ]
#scaleMid = [ 0.27202594  ,0.         , 0.37690844]
#offMid = [ 100.09260316  ,  0.      ,     -2.63168125]
#scaleRin = [ 0.28069745 , 0.       ,   0.35377253]
#offRin = [ 127.56886782 ,   0.    ,      -16.67340924]
#scalePin = [ 0.31165901 , 0.     ,     0.32485459]
#offPin = [ 142.79841089 ,   0.  ,        -61.90143651]

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
        
estAngMeas = np.array([[0.,0.,0.,0.,0.,0.]])  
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
        
#        collected = np.append(collected,[index,middle,ring,pinky],axis=0)
        
        if len(index) > 10:
            print "here"
            res = modE.estimate_BtoAng(estAngMeas[-1],
                                       [phalMid,phalRin,phalPin],
                                        [yMid,yRin,yPin],
                                        [sInd,sMid,sRin,sPin],
                                        np.concatenate((index[-1],middle[-1],ring[-1],pinky[-1])),
                                        bnds[:6],method='cy')        
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
                        "{0:.4f} ".format(res.x[2])+"{0:.4f} ".format(res.x[3])+"{0:.4f} ".format(res.x[3]*(2/3))+ 
                        "{0:.4f} ".format(res.x[4])+"{0:.4f} ".format(res.x[5])+"{0:.4f} ".format(res.x[5]*(2/3)))
                        
            f = open(fileName,'a')  
            f.write(toSend+'\n')     
            print toSend
            f.close()   
    
        
        
except KeyboardInterrupt:
    print "ended, cnt: ", cnt
    print "errorCnt: ", errCnt
    subProBlend.kill()    
    procBle.kill()          
#    plo.plotter2d((index[10:],middle[10:],ring[10:],pinky[10:]),("ind","mid","rin","pinky"))
    plo.plotter2d((calcBInd_m[:,:3],index[10:]),("INDEX perfect","meas"))
    plo.plotter2d((calcBInd_m[:,3:6],middle[10:]),("MIDDLEperfect","meas"))
    plo.plotter2d((calcBInd_m[:,6:9],ring[10:]),("RINGperfect","meas"))
    plo.plotter2d((calcBInd_m[:,9:],pinky[10:]),("PINKYperfect","meas"))
#    plt.figure()
#    plt.plot(estAngMeas[:,0],'r')
#    plt.plot(estAngMeas[:,1],'g')
    plt.show()
    
    
import dataAcquisitionMulti as datAc
import matplotlib.pyplot as plt
import modelEqMultiCython as modE
import numpy as np
from scipy.optimize import *
import plotting as plo
import time,subprocess


def inStretchPos(ref,meas):
       # number of measurements to take into account
    mMeas = np.zeros((len(meas[0],)))
    for i in range(len(meas[0])):
        mMeas[i] = np.mean(meas[:,i])
    print "summed dif: ",sum((mMeas-ref))    
    if abs(sum((mMeas-ref))) < 80:
        return True
    else:
        return False


cmd = "gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen"


sInd = [-0.03, -0.0, 0.024]
sMid = [-0.03, -0.022, 0.024]
sRin = [-0.03, -0.044, 0.024]
sPin = [-0.03, -0.066, 0.024]

yInd = [0.0, 0.0, -0.0]
yMid = [0.0, -0.022, 0.002]
yRin = [0.0, -0.044, 0.002]
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
calDat = datAc.pipeAcquisition(cmd,4,measNr=100)
#calDat = datAc.collectForTime(cmd,5)

t = np.arange(0,1/2.*np.pi,0.01)
angles = np.zeros((len(t),3))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0, 0])
    cnt += 1

# calculating the B-field
fingerList = [phalInd,phalMid,phalRin,phalPin]
yOffList = [yInd,yMid,yRin,yPin]
sensList = [sInd,sMid,sRin,sPin]

calcBInd_m = np.zeros((len(angles),len(sensList)*3))
cnt = 0
for i in angles:
    calcBInd_m[cnt] = (modE.angToB_m2(i,phalMid,sensList,yMid)+
                        modE.angToB_m2(i,phalRin,sensList,yRin)+
                         modE.angToB_m2(i,phalPin,sensList,yPin)+
                         modE.angToB_m2(i,phalInd,sensList,yInd))
    cnt += 1

caliPos = calcBInd_m[0]

filInd = datAc.moving_average3d(calDat[0],10)
filMid = datAc.moving_average3d(calDat[1],10)
filRin = datAc.moving_average3d(calDat[2],10)
filPin = datAc.moving_average3d(calDat[3],10)

(scaleInd,offInd) = modE.getScaleOff(calcBInd_m[:,0:3],filInd)
(scaleMid,offMid) = modE.getScaleOff(calcBInd_m[:,3:6],filMid)
(scaleRin,offRin) = modE.getScaleOff(calcBInd_m[:,6:9],filRin)
(scalePin,offPin) = modE.getScaleOff(calcBInd_m[:,9:12],filPin)

#(scaleInd,offInd) = ([1.,1.,1.] ,
#                    [calcBInd_m[0][0]-np.mean(filInd[:,0]), calcBInd_m[0][1]-np.mean(filInd[:,1]),calcBInd_m[0][2]-np.mean(filInd[:,2])])
#(scaleMid,offMid) = ([1.,1.,1.],
#                    [ calcBInd_m[0][3]-np.mean(filMid[:,0]), calcBInd_m[0][4]-np.mean(filMid[:,1]),calcBInd_m[0][5]-np.mean(filMid[:,2])])
#(scaleRin,offRin) = ([1.,1.,1.],
#                    [ calcBInd_m[0][6]-np.mean(filRin[:,0]), calcBInd_m[0][7]-np.mean(filRin[:,1]),calcBInd_m[0][8]-np.mean(filRin[:,2])])
#(scalePin,offPin) = ([1.,1.,1.],
#                    [ calcBInd_m[0][9]-np.mean(filPin[:,0]), calcBInd_m[0][10]-np.mean(filPin[:,1]),calcBInd_m[0][11]-np.mean(filPin[:,2])])

#(scaleInd,offInd) = ([ 0.32109206  ,0.,          0.38416407] ,[ 91.2577668,    0.       ,    7.53530872])
#(scaleMid,offMid) = ([ 0.33155661  ,0. ,         0.41174773] ,[ 79.19175527,   0.      ,    14.85343632])
#(scaleRin,offRin) = ([ 0.33834944  ,0.  ,        0.40100347] ,[ 97.30206833   ,0.  ,         1.31727868])
#(scalePin,offPin) = ([ 0.35126895  ,0. ,         0.39166963] ,[ 118.12913948  ,  0. ,         -60.0863787 ])

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
        (0.0,np.pi/(180/110)),      # PIP  
        #(0.0,np.pi/2))      # DIP
        (0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)))      # PIP  
        #(0.0,np.pi/2))      # DIP
        
estAngMeas = np.zeros((1,2*len(fingerList)))
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
    time.sleep(0.5)
    while True:
        print "cnt: ",cnt
        cnt += 1                   
        
        data = datAc.RTdata_blocking(procBle)  
        zero = False
        for i in range(4):
            if not data[i][1:].any():       # you have a whole line of zeros...
                zero = True
                        
        if not zero:            
            index = np.append(index,[data[0][1:]*scaleInd+offInd],axis=0)
            middle = np.append(middle,[data[1][1:]*scaleMid+offMid],axis=0)        
            ring = np.append(ring,[data[2][1:]*scaleRin+offRin],axis=0)
            pinky = np.append(pinky,[data[3][1:]*scalePin+offPin],axis=0)
        
            index[-1] = datAc.movAvgRT(index,5)
            middle[-1] = datAc.movAvgRT(middle,5)
            ring[-1] = datAc.movAvgRT(ring,5)
            pinky[-1] = datAc.movAvgRT(pinky,5)
        
        if cnt > 20:
#            a = inStretchPos(caliPos,np.concatenate((index[-10:],middle[-10:],ring[-10:],pinky[-10:]),1)) 
            a = False
            if a:
                print "!!!!!!!!ZERO!!!!!!!!!!!"
                estAngMeas = np.append(estAngMeas,[estAngMeas[0]],axis=0)
                
            else:
                res = modE.estimate_BtoAng(estAngMeas[-1],
                                           fingerList,
                                            yOffList,
                                            sensList,
                                            np.concatenate((index[-1],middle[-1],ring[-1],pinky[-1])),
                                            bnds[:2*len(fingerList)],method='cy')        
    
#                if not res.success:
#                    print "no solution..."  
#                    errCnt += 1
#                estAngMeas = np.append(estAngMeas,[res.x],axis=0)
#                fval = np.append(fval,res.fun)
                if res[2]['warnflag']:
                    print "no solution..."  
                    errCnt += 1
                    print res
                estAngMeas = np.append(estAngMeas,[res[0]],axis=0)
                fval = np.append(fval,res[1])
    ###                 sending the estimated values to the visualization
#            toSend = ("0.0000 0.0000 0.0000 " +                        
#                        "{0:.4f} ".format(estAngMeas[-1][0])+"{0:.4f} ".format(estAngMeas[-1][1])+"{0:.4f} ".format(estAngMeas[-1][1]*(2/3))+
#                        "{0:.4f} ".format(estAngMeas[-1][2])+"{0:.4f} ".format(estAngMeas[-1][3])+"{0:.4f} ".format(estAngMeas[-1][3]*(2/3))+ 
#                        "{0:.4f} ".format(estAngMeas[-1][4])+"{0:.4f} ".format(estAngMeas[-1][5])+"{0:.4f} ".format(estAngMeas[-1][5]*(2/3))+
#                         "{0:.4f} ".format(estAngMeas[-1][6])+"{0:.4f} ".format(estAngMeas[-1][7])+"{0:.4f} ".format(estAngMeas[-1][7]*(2/3)))
            toSend = ("0.0000 0.0000 0.0000 " +     # thumb                     
                        "{0:.4f} ".format(estAngMeas[-1][0])+"{0:.4f} ".format(estAngMeas[-1][1])+"{0:.4f} ".format(estAngMeas[-1][1]*(2/3))+                        
                        "{0:.4f} ".format(estAngMeas[-1][2])+"{0:.4f} ".format(estAngMeas[-1][3])+"{0:.4f} ".format(estAngMeas[-1][3]*(2/3))+                        
#                        "0.0000 0.0000 0.0000 " + 
                        "{0:.4f} ".format(estAngMeas[-1][4])+"{0:.4f} ".format(estAngMeas[-1][5])+"{0:.4f} ".format(estAngMeas[-1][5]*(2/3))+                        
                        "{0:.4f} ".format(estAngMeas[-1][6])+"{0:.4f} ".format(estAngMeas[-1][7])+"{0:.4f} ".format(estAngMeas[-1][7]*(2/3)))                       
#                        "0.0000 0.0000 0.0000 " +                         
#                         "0.0000 0.0000 0.0000 " )                        
            f = open(fileName,'a')  
            f.write(toSend+'\n')     
            print toSend
            f.close()   
        else:
            print "not enough!"
            
            
    
        
        
except KeyboardInterrupt:
    print "ended, cnt: ", cnt
    print "errorCnt: ", errCnt
subProBlend.kill()    
procBle.kill()          
#plo.plotter2d((calcBInd_m[0:3],index[1:],middle[1:],ring[1:],pinky[1:]),("perfectInd","ind","mid","rin","pinky"))
#plo.plotter2d((calcBInd_m[0:3],indexEst[1:],middleEst[1:],ringEst[1:],pinkyEst[1:]),("ind","ESTind","mid","rin","pinky"))
plo.plotter2d((calcBInd_m[:,:3],index[10:]),("INDEX perfect","meas"))
plo.plotter2d((calcBInd_m[:,3:6],middle[10:]),("MIDDLEperfect","meas"))
plo.plotter2d((calcBInd_m[:,6:9],ring[10:]),("RINGperfect","meas"))
plo.plotter2d((calcBInd_m[:,9:],pinky[10:]),("PINKYperfect","meas"))
plt.figure()
plt.plot(estAngMeas[:,0],'r')
plt.plot(estAngMeas[:,1],'g')
plt.plot(estAngMeas[:,1]*(2./3.),'b')
plt.title("RT")
plt.show()

print scaleInd,offInd
print scaleMid,offMid
print scaleRin,offRin
print scalePin,offPin
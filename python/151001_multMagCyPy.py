
"""
Created on Wed Aug 12 09:40:01 2015

@author: daniel
"""

import dataAcquisitionMulti as datAcM
import plotting as plo
import numpy as np
import modelEqMultiCython as modE
import modelEq as modEsing
import matplotlib.pyplot as plt
import time, os, subprocess
from sympy import *
import fcnCyPy as fcn
import signal



"""
the sensor is below the middle finger and the magnet is on the middle finger
"""

""" acquiring data... """
#print "t:"
#fingDat=datAcM.pipeAcquisition("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen",
#                               "150901_testAll", measNr=500, offset=100)
#fingDat=datAcM.textAcquistion("150825_middleLSM")

# position of wooden-joints
jointInd = [0.09138, 0.02957, -0.01087]         # to wooden-joint(index)
jointMid = [0.09138, 0.00920, -0.01087]          # to wooden-joint(middle)
jointRin = [0.09138, -0.01117, -0.01087]         # to wooden-joint(ring)
jointPin = [0.09138, -0.03154, -0.01087]         # to wooden-joint(pinky)

# position of sensor
s1 = [0.06755, 0.02957, 0.]     # sensor beneath index
#s1 = [0.02886, 0.04755, 0.]
#s2 = [0.00920 , 0.06755, 0.]    # sensor beneath middle
s2 = [0.04755, 0.00920, 0.]
s3 = [0.06755, -0.01117, 0.]     # sensor beneath ring
#s3 = [-0.01046, 0.04755, 0.]
#s4 = [-0.03154, 0.06755, 0.]     # sensor beneath pinky
s4 = [0.04755, -0.03012, 0.]

# length of fingers
rInd = 0.08                     # length of index finger (from jointle)
rMid = 0.08829                  # length of middle finger (from jointle)
rRin = 0.07979                  # length of ring finger (from jointle)
rPin = 0.07215                  # length of pinky finger (from jointle)

# lengths of phalanges
phalInd = [0.03038, 0.02728, 0.02234]
phalMid = [0.03640, 0.03075, 0.02114]
phalRin = [0.03344, 0.02782, 0.01853]
phalPin = [0.02896, 0.02541, 0.01778]

b = datAcM.textAcquistion("perfectB")

""" fitting the data to the model """

""" estimating the position from the measurments """
estPos = np.zeros((4,len(b[0]),3))
# initial positions
estPos[0][0] = [jointInd[0]+rInd, jointInd[1], jointInd[2]]
estPos[1][0] = [jointMid[0]+rMid, jointMid[1], jointMid[2]]
estPos[2][0] = [jointRin[0]+rRin, jointRin[1], jointRin[2]]
estPos[3][0] = [jointPin[0]+rPin, jointPin[1], jointPin[2]]
# fixed bnds for position
bndsPos = ((jointInd[0],jointInd[0]+rInd),    # index finger
    #      (jointInd[1]-0.003,jointInd[1]+0.003),
          (jointInd[1]-0.0001,jointInd[1]+0.0001),
          (jointInd[2]-rInd,jointInd[2]),

          (jointMid[0],jointMid[0]+rMid),    # middle finger
    #      (jointMid[1]-0.003,jointMid[1]+0.003),
          (jointMid[1]-0.0001,jointMid[1]+0.0001),
          (jointMid[2]-rMid,jointMid[2]),

          (jointRin[0],jointRin[0]+rRin),    # ring finger
    #      (jointRin[1]-0.003,jointRin[1]+0.003),
          (jointRin[1]-0.0001,jointRin[1]+0.0001),
          (jointRin[2]-rRin,jointRin[2]),

          (jointPin[0],jointPin[0]+rPin),    # pinky finger
#          (jointPin[1]-0.003,jointPin[1]+0.003),
          (jointPin[1]-0.0001,jointPin[1]+0.0001),
          (jointPin[2]-rPin,jointPin[2]))

estAng = np.zeros((4,len(b[0]),3))
estAng[0][0] = [0,0,0]
estAng[1][0] = [0,0,0]
estAng[2][0] = [0,0,0]
estAng[3][0] = [0,0,0]
# fixed bnds for angles
bndsAng = ((0,np.pi/2),         # index finger
        (0,(110/180*np.pi)),
        (0,np.pi/2),
        (0,np.pi/2),            # middle finger
        (0,(110/180*np.pi)),
        (0,np.pi/2),
        (0,np.pi/2),            # ring finger
        (0,(110/180*np.pi)),
        (0,np.pi/2),
        (0,np.pi/2),            # pinky finger
        (0,(110/180*np.pi)),
        (0,np.pi/2))


startAlg = time.time()
lapPos = np.zeros((len(estPos[0])-1,2))
lapAng = np.zeros((len(estPos[0])-1,2))

# piping action...
#mPath = 'estimatedAngles'
#if not os.path.exists(mPath):
#    os.mkfifo(mPath)
#procId = os.getpid()   
#print "starting visualization..."
#vis = subprocess.Popen(('./../visualization/finger_angles/application.linux64/finger_angles '+mPath).split(),shell=False)
#pipeout = file(mPath,"w")

print "begin of estimation..."
for i in range(len(b[0])-1):
    ''' position estimation
        for four magnets(index, middle, pinky) and four sensors (middle, pinky, index)'''
    startPos = time.time()
#    cython way...
#    tmp = modE.estimatePos(np.concatenate((estPos[0][i],estPos[1][i],estPos[2][i],estPos[3][i])),
#                         np.reshape([s1,s2,s3,s4],((12,))),     # for calling the cython function
#                         np.concatenate((b[0][i+1],b[1][i+1],b[2][i+1],b[3][i+1])),
#                         i,bndsPos)
#   python way...                         
    tmp = modE.estimatePosPy(np.concatenate((estPos[0][i],estPos[1][i],estPos[2][i],estPos[3][i])),
                         [s1,s2,s3,s4],
                         np.concatenate((b[0][i+1],b[1][i+1],b[2][i+1],b[3][i+1])),
                         i,bndsPos)

    resPos = np.reshape(tmp.x,(4,1,3))
    lapPos[i] = ((time.time()-startPos),tmp.nit)
    estPos[0][i+1] = resPos[0]
    estPos[1][i+1] = resPos[1]
    estPos[2][i+1] = resPos[2]
    estPos[3][i+1] = resPos[3]

    ''' angle estimation '''
#    startAngle = time.time()
#    eAng = modE.estimateAngle_m(tmp.x,
#                                np.concatenate((estAng[0][i],estAng[1][i],estAng[2][i],estAng[3][i])),
#                                np.reshape([jointInd,jointMid,jointRin,jointPin],((12,))),
#                                np.reshape([phalInd,phalMid,phalRin,phalPin],((12,))),
#                                bndsAng)
#
#    resAng = np.reshape(eAng.x,(4,1,3))
##    resAng = np.reshape(eAng,(4,1,3))
#    lapAng[i] = ((time.time()-startAngle), eAng.nit)
#    estAng[0][i+1] = resAng[0]
#    estAng[1][i+1] = resAng[1]
#    estAng[2][i+1] = resAng[2]
#    estAng[3][i+1] = resAng[3]
    # convert angles to proper format
#    pipeStr = ''
#    for i in eAng.x:
#        pipeStr = pipeStr + " {0:.4f}".format(abs(i))
#    # put the angles on the pipe...
#    try:                   #thumb      #index       #middle      #ring        #pinky
#        pipeout.write("0.0000 0.0000 0.0000" + pipeStr)
#        pipeout.flush()
#    except OSError,e:
#        print "error! listener disconnected"
#        os.unlink(mPath)
#        break

    #time.sleep(1)   #wait a second, to have a better visualization

#print "child ID: ", vis.pid
#os.remove(mPath)
#vis.kill()
#os.unlink(mPath)
#print "procID: ", procId
#os.kill(vis.pid+3, signal.SIGKILL)  # why +3 ???

print "time duration: ", (time.time()-startAlg)

print "delta y estPos[0]-Index", max(estPos[0][:,1])-min(estPos[0][:,1])
print "delta y estPos[1]-Middle", max(estPos[1][:,1])-min(estPos[1][:,1])
print "delta y estPos[2]-Ring", max(estPos[2][:,1])-min(estPos[2][:,1])
print "delta y estPos[3]-Pinky", max(estPos[3][:,1])-min(estPos[3][:,1])

# remove the y-axis motion...
#estPos[0][:,1] = jointInd[1]
#estPos[1][:,1] = jointMid[1]
#estPos[2][:,1] = jointRin[1]
#estPos[3][:,1] = jointPin[1]

""" plotting stuff """
#plo.plotter3d((pos[0],pos[1],pos[2], pos[3]),("Ind real","mid Real", "ring Real", "pin Real"))
#plo.plotter2d((summedInd,summedMid,summedRin,summedPin),("index","Mid","Rin","Pin"))
plo.multiPlotter(estPos[0],"Index")
plo.multiPlotter(estPos[1],"Middle")
plo.multiPlotter(estPos[2],"Ring")
plo.multiPlotter(estPos[3],"Pinky")

#plt.figure("callTime Position")
#plt.hist(lapPos[:,0],100)
#plt.figure("callHist Position")
#plt.hist(lapPos[:,1],100)
#plt.figure("callTime Angle")
#plt.hist(lapAng[:,0],100)
#plt.figure("callHist Angle")
#plt.hist(lapAng[:,1],100)
#plt.figure("angles")
#plt.plot(estAng[0][:,0])
#plt.plot(estAng[1][:,0])
#plt.plot(estAng[2][:,0])
#plt.plot(estAng[3][:,0])


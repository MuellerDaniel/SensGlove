
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
import time
from sympy import *
import fcnCyPy as fcn



"""
the sensor is below the middle finger and the magnet is on the middle finger
"""

""" acquiring data... """
#print "t:"
#fingDat=datAcM.pipeAcquisition("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen",
#                               "150901_testAll", measNr=500, offset=100)
#fingDat=datAcM.textAcquistion("150825_middleLSM")

#""" the artificial data... """
angInd = [0.09138, 0.02957, -0.01087]         # to wooden-angle(index)
angMid = [0.09138, 0.00920, -0.01087]          # to wooden-angle(middle)
angRin = [0.09138, -0.01117, -0.01087]         # to wooden-angle(ring)
angPin = [0.09138, -0.03154, -0.01087]         # to wooden-angle(pinky)

# position of sensor
s1 = [0.06755, 0.02957, 0.]     # sensor beneath index
#s1 = [0.02886, 0.04755, 0.]
#s2 = [0.00920 , 0.06755, 0.]    # sensor beneath middle
s2 = [0.04755, 0.00920, 0.]
s3 = [0.06755, -0.01117, 0.]     # sensor beneath ring
#s3 = [-0.01046, 0.04755, 0.]
#s4 = [-0.03154, 0.06755, 0.]     # sensor beneath pinky
s4 = [0.04755, -0.03012, 0.]

rInd = 0.08                     # length of index finger (from angle)
rMid = 0.08829                  # length of middle finger (from angle)
rRin = 0.07979                  # length of ring finger (from angle)
rPin = 0.07215                  # length of pinky finger (from angle)

b = datAcM.textAcquistion("perfectB")

""" fitting the data to the model """

""" estimating the position from the measurments """
estPos = np.zeros(shape=(4,len(b[0]),3))
# initial positions
estPos[0][0] = [angInd[0]+rInd, angInd[1], angInd[2]]
estPos[1][0] = [angMid[0]+rMid, angMid[1], angMid[2]]
estPos[2][0] = [angRin[0]+rRin, angRin[1], angRin[2]]
estPos[3][0] = [angPin[0]+rPin, angPin[1], angPin[2]]

# fixed bnds
bnds=((angInd[0],angInd[0]+rInd),    # index finger
      (angInd[1]-0.003,angInd[1]+0.003),
      (angInd[2]-rInd,angInd[2]),

      (angMid[0],angMid[0]+rMid),    # middle finger
      (angMid[1]-0.003,angMid[1]+0.003),
      (angMid[2]-rMid,angMid[2]),

      (angRin[0],angRin[0]+rRin),    # ring finger
      (angRin[1]-0.003,angRin[1]+0.003),
      (angRin[2]-rRin,angRin[2]),

      (angPin[0],angPin[0]+rPin),    # pinky finger
      (angPin[1]-0.003,angPin[1]+0.003),
      (angPin[2]-rPin,angPin[2]))

startAlg = time.time()
lapinfo = np.zeros((len(estPos[0])-1,2))
print "begin of estimation..."
for i in range(len(b[0])-1):
# for four magnets(index, middle, pinky) and four sensors (middle, pinky, index)
    startTime = time.time()
    ''' normal version '''
    tmp = modE.estimatePos(np.concatenate((estPos[0][i],estPos[1][i],estPos[2][i],estPos[3][i])),
                         np.reshape([s1,s2,s3,s4],((12,))),     # for calling the cython function
                         np.concatenate((b[0][i+1],b[1][i+1],b[2][i+1],b[3][i+1])),   
                         i,bnds)
    ''' cython version '''
#    tmp = fcn.estimatePos(np.concatenate((estPos[0][i],estPos[1][i],estPos[2][i],estPos[3][i])),
#                        np.reshape([s1,s2,s3,s4],((12,))),     # for calling the cython function
#                        np.concatenate((b[0][i+1],b[1][i+1],b[2][i+1],b[3][i+1])),
#                        i,bnds)

    res = np.reshape(tmp.x,(4,1,3))   
    lapinfo[i] = ((time.time()-startTime),tmp.nit)
    estPos[0][i+1] = res[0]
    estPos[1][i+1] = res[1]
    estPos[2][i+1] = res[2]
    estPos[3][i+1] = res[3]


print "time duration: ", (time.time()-startAlg)

print "delta y estPos[0]-Index", max(estPos[0][:,1])-min(estPos[0][:,1])
print "delta y estPos[1]-Middle", max(estPos[1][:,1])-min(estPos[1][:,1])
print "delta y estPos[2]-Ring", max(estPos[2][:,1])-min(estPos[2][:,1])
print "delta y estPos[3]-Pinky", max(estPos[3][:,1])-min(estPos[3][:,1])

""" plotting stuff """
#plo.plotter3d((pos[0],pos[1],pos[2], pos[3]),("Ind real","mid Real", "ring Real", "pin Real"))
#plo.plotter2d((summedInd,summedMid,summedRin,summedPin),("index","Mid","Rin","Pin"))
plo.multiPlotter(estPos[0],"Index")
plo.multiPlotter(estPos[1],"Middle")
plo.multiPlotter(estPos[2],"Ring")
plo.multiPlotter(estPos[3],"Pinky")

plt.figure("callTime")
plt.hist(lapinfo[:,0],100)
plt.figure("callHist")
plt.hist(lapinfo[:,1],100)
plt.show()

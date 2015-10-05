
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


def jaco(P,S):
    s0,s1,s2,x,y,z=symbols('s0 s1 s2 x y z')
    funSubst = np.array(symJac.subs({s0:S[0],s1:S[1],s2:S[2],
                                  x:P[0],y:P[1],z:P[2]}))
#    print funSubst
    return funSubst


"""
the sensor is below the middle finger and the magnet is on the middle finger
"""

""" acquiring data... """
#print "t:"
#fingDat=datAcM.pipeAcquisition("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen",
#                               "150901_testAll", measNr=500, offset=100)
fingDat=datAcM.textAcquistion("150825_middleLSM")
#fingDat2=datAcM.textAcquistion("150828_MidPin3")
# applying average filter
#avg=modE.moving_average(fingDat[0], 10)
#t=np.zeros(shape=[len(avg),1])
#t=np.append(t,avg,axis=1)
#t=datAcM.sortData(t)
#fingDat=None
#fingDat=t

#avg2=modE.moving_average(fingDat2[0], 10)
#t2=np.zeros(shape=[len(avg2),1])
#t2=np.append(t2,avg2,axis=1)
#t2=datAcM.sortData(t2)
#fingDat2=None
#fingDat2=t2

""" the artificial data... """
angInd = [0.02957, 0.09138, 0.01087]         # to wooden-angle(index)
angMid = [0.00920, 0.09138, 0.01087]          # to wooden-angle(middle)
angRin = [-0.01117, 0.09138, 0.01087]         # to wooden-angle(ring)
angPin = [-0.03154, 0.09138, 0.01087]         # to wooden-angle(pinky)

# position of sensor
s1 = [0.02957, 0.06755, 0.]     # sensor beneath index
#s1 = [0.02886, 0.06755, 0.]
s2 = [0.00920 , 0.06755, 0.]    # sensor beneath middle
#s2 = [0.00920 , 0.02755, 0.]
s3 = [-0.01117, 0.06755, 0.]     # sensor beneath ring
#s3 = [-0.01046, 0.06755, 0.]
s4 = [-0.03154, 0.06755, 0.]     # sensor beneath pinky
#s4 = [-0.03012, 0.02755, 0.]

rInd = 0.08                     # length of index finger (from angle)
rMid = 0.08829                  # length of middle finger (from angle)
rRin = 0.07979                  # length of ring finger (from angle)
rPin = 0.07215                  # length of pinky finger (from angle)
# values for the half circle
t = np.arange(0, 1/2.*np.pi, 0.01)
pos1 = [[0.,0.,0.]]
pos2 = [[0.,0.,0.]]
pos3 = [[0.,0.,0.]]
pos4 = [[0.,0.,0.]]
cnt=1
for i in t:
    # position of the index finger
    pos1 = np.append(pos1, [[angInd[0],
                            angInd[1]+rInd*np.cos(i),
                            angInd[2]+rInd*np.sin(i)]],
                            axis=0)

    # positions of the middle finger
    pos2 = np.append(pos2, [[angMid[0],
                            angMid[1]+rMid*np.cos(i),
                            angMid[2]+rMid*np.sin(i)]],
                            axis=0)
#    pos2 = np.append(pos2, [[angMid[0],
#                            angMid[1]+rMid*np.cos(i/2),
#                            angMid[2]+rMid*np.sin(i/2)]],
#                            axis=0)

      # position of the ring finger
    pos3 = np.append(pos3, [[angRin[0],
                            angRin[1]+rRin*np.cos(i),
                            angRin[2]+rRin*np.sin(i)]],
                            axis=0)

    # positions of the pinky finger
    pos4 = np.append(pos4, [[angPin[0],
                            angPin[1]+rPin*np.cos(i),
                            angPin[2]+rPin*np.sin(i)]],
                            axis=0)
#    pos4 = np.append(pos4, [[angPin[0],
#                            angPin[1],
#                            angPin[2]]],
#                            axis=0)

    cnt+=1

pos = np.zeros(shape=(4,len(pos1)-1,3))
pos[0] = pos1[1:]
pos[1] = pos2[1:]
pos[2] = pos3[1:]
pos[3] = pos4[1:]

calcBInd = [[[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]]]
calcBMid = [[[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]]]      # The cumulative field measured with sensor at s0
calcBMid_dot = [[[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]]]
calcBRin = [[[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]]]
calcBPin = [[[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]]]

cnt=0
# calculate the magnetic fields for each sensor and each magnet
for i in range(pos.shape[1]):
    calcBInd[0] = np.append(calcBInd[0],
                      modE.evalfuncMagDot(pos[0][i],s1), axis=0)
    calcBInd[1] = np.append(calcBInd[1],
                      modE.evalfuncMagDot(pos[1][i],s1), axis=0)
    calcBInd[2] = np.append(calcBInd[2],
                      modE.evalfuncMagDot(pos[2][i],s1), axis=0)
    calcBInd[3] = np.append(calcBInd[3],
                      modE.evalfuncMagDot(pos[3][i],s1), axis=0)

    calcBMid[0] = np.append(calcBMid[0],
                      modE.evalfuncMagDot(pos[0][i],s2), axis=0)
    calcBMid[1] = np.append(calcBMid[1],
                      modE.evalfuncMagDot(pos[1][i],s2), axis=0)
    calcBMid[2] = np.append(calcBMid[2],
                      modE.evalfuncMagDot(pos[2][i],s2), axis=0)
    calcBMid[3] = np.append(calcBMid[3],
                      modE.evalfuncMagDot(pos[3][i],s2), axis=0)

#    calcBMid_dot[0] = np.append(calcBMid_dot[0],
#                      modE.evalfuncMagDot(pos[0][i],s2), axis=0)
#    calcBMid_dot[1] = np.append(calcBMid_dot[1],
#                      modE.evalfuncMagDot(pos[1][i],s2), axis=0)
#    calcBMid_dot[2] = np.append(calcBMid_dot[2],
#                      modE.evalfuncMagDot(pos[2][i],s2), axis=0)
#    calcBMid_dot[3] = np.append(calcBMid_dot[3],
#                      modE.evalfuncMagDot(pos[3][i],s2), axis=0)

    calcBRin[0] = np.append(calcBRin[0],
                      modE.evalfuncMagDot(pos[0][i],s3), axis=0)
    calcBRin[1] = np.append(calcBRin[1],
                      modE.evalfuncMagDot(pos[1][i],s3), axis=0)
    calcBRin[2] = np.append(calcBRin[2],
                      modE.evalfuncMagDot(pos[2][i],s3), axis=0)
    calcBRin[3] = np.append(calcBRin[3],
                      modE.evalfuncMagDot(pos[3][i],s3), axis=0)

    calcBPin[0] = np.append(calcBPin[0],
                      modE.evalfuncMagDot(pos[0][i],s4), axis=0)
    calcBPin[1] = np.append(calcBPin[1],
                      modE.evalfuncMagDot(pos[1][i],s4), axis=0)
    calcBPin[2] = np.append(calcBPin[2],
                      modE.evalfuncMagDot(pos[2][i],s4), axis=0)
    calcBPin[3] = np.append(calcBPin[3],
                      modE.evalfuncMagDot(pos[3][i],s4), axis=0)

calcBInd = np.delete(calcBInd,0,1)
calcBMid = np.delete(calcBMid,0,1)
calcBMid_dot = np.delete(calcBMid_dot,0,1)
calcBRin = np.delete(calcBRin,0,1)
calcBPin = np.delete(calcBPin,0,1)

# REMEMBER: only add the fields, that you realy need!
summedInd=np.zeros(shape=(1,len(calcBInd[0]),3))
summedInd+=(calcBInd[0]+calcBInd[1]+calcBInd[2]+calcBInd[3])
summedMid=np.zeros(shape=(1,len(calcBMid[0]),3))
summedMid+=(calcBMid[0]+calcBMid[1]+calcBMid[2]+calcBMid[3])
summedRin=np.zeros(shape=(1,len(calcBRin[0]),3))
summedRin+=(calcBRin[0]+calcBRin[1]+calcBRin[2]+calcBRin[3])
summedPin=np.zeros(shape=(1,len(calcBPin[0]),3))
summedPin+=(calcBPin[0]+calcBPin[1]+calcBPin[2]+calcBPin[3])

""" fitting the data to the model """
#data=modE.fitMeasurements(calc[0], fingDat[0], (0,5))
### 150825 EarthMagField = [-154.94878, -394.42383, -63.25812]
#dataS=np.zeros(shape=[len(data),1])
#dataS=np.append(dataS,data,axis=1)
#dataS=datAcM.sortData(dataS)

""" estimating the position from the measurments """
estPos = np.zeros(shape=(4,len(summedMid[0]),3))
#estPos2 = np.zeros(shape=(2,len(summedMid[0]),3))
#estPos[0][0] = [angMid[0]+s0[0], angMid[1]+s0[1]+rMid, s0[2]+angMid[2]]
#estPos[1][0] = [angPin[0]+s0[0], angPin[1]+s0[1]+rPin, s0[2]+angPin[2]]
estPos[0][0] = pos[0][0]
estPos[1][0] = pos[1][0]
estPos[2][0] = pos[2][0]
estPos[3][0] = pos[3][0]

# fixed bnds
bnds=((angInd[0]-0.003,angInd[0]+0.003),    # index finger
      (angInd[1],angInd[1]+rInd),
      (angInd[2],angInd[2]+rInd),

      (angMid[0]-0.003,angMid[0]+0.003),    # middle finger
      (angMid[1],angMid[1]+rMid),
      (angMid[2],angMid[2]+rMid),

      (angRin[0]-0.003,angRin[0]+0.003),    # ring finger
      (angRin[1],angRin[1]+rRin),
      (angRin[2],angRin[2]+rRin),

      (angPin[0]-0.003,angPin[0]+0.003),    # pinky finger
      (angPin[1],angPin[1]+rPin),
      (angPin[2],angPin[2]+rPin))


#global symJac
#symJac = modE.calcJacobi()
#modE.calcJacobi()

S=np.append(s1,s2,axis=0)
S=np.append(S,s3,axis=0)
S=np.append(S,s4,axis=0)
B=np.zeros((4,3))
startAlg = time.time()
lapinfo = np.zeros((len(summedMid[0])-1,2))
# fi = open("Errors.txt",'w')
print "begin of estimation..."
for i in range(len(summedMid[0])-1):
#    # for three magnets(index, middle, pinky) and two sensors (middle, pinky)
#    tmp = modE.estimatePos(np.concatenate((estPos[0][i],estPos[1][i],estPos[2][i])),
#                         [s0,s1],
#                          np.concatenate((summedMid[0][i+1],summedPin[0][i+1])),i,bnds)
#    estPos[0][i+1] = tmp[0]
#    estPos[1][i+1] = tmp[1]
#    estPos[2][i+1] = tmp[2]

 # for three magnets(index, middle, pinky) and three sensors (middle, pinky, index)
#    tmp = modE.estimatePos(np.concatenate((estPos[0][i],estPos[1][i],estPos[2][i])),
#                         [s0,s1,s2],
#                          np.concatenate((summedMid[0][i+1],summedPin[0][i+1],summedInd[0][i+1])),i,bnds)
#    estPos[0][i+1] = tmp[0]
#    estPos[1][i+1] = tmp[1]
#    estPos[2][i+1] = tmp[2]

# for two magnets(middle, pinky) and two sensors(middle, pinky)   -   works good!
#    tmp = modE.estimatePos(np.concatenate((estPos[0][i],estPos[1][i])),
#                         [s0,s1],
#                          np.concatenate((summedMid[0][i+1],summedPin[0][i+1])),i,bnds[:6])
#    estPos[0][i+1] = tmp[0]
#    estPos[1][i+1] = tmp[1]

#    print "finished first"

    # for two magnets and one sensor
#    tmp2 = modE.estimatePos(np.append(estPos2[0][i],estPos2[1][i]),
#                         [s0],
#                          summedMid[0][i+1],i,bnds)
#    estPos2[0][i+1] = tmp2[0]
#    estPos2[1][i+1] = tmp2[1]

    B[0] = summedInd[0][i+1]
    B[1] = summedMid[0][i+1]
    B[2] = summedRin[0][i+1]
    B[3] = summedPin[0][i+1]
# for four magnets(index, middle, pinky) and four sensors (middle, pinky, index)
#    print "solution ", i
    startTime = time.time()
    ''' normal version '''
    #tmp = modE.estimatePos(np.concatenate((estPos[0][i],estPos[1][i],estPos[2][i],estPos[3][i])),
    #                     np.reshape([s1,s2,s3,s4],((12,))),     # for calling the cython function
    #                     np.concatenate((summedInd[0][i+1],summedMid[0][i+1],summedRin[0][i+1],summedPin[0][i+1])),
#   #                      B,     # for advanced approach version 2
    #                     i,bnds)
    ''' cython version '''
    tmp = fcn.estimatePos(np.concatenate((estPos[0][i],estPos[1][i],estPos[2][i],estPos[3][i])),
                        np.reshape([s1,s2,s3,s4],((12,))),     # for calling the cython function
                        np.concatenate((summedInd[0][i+1],summedMid[0][i+1],summedRin[0][i+1],summedPin[0][i+1])),
                        i,bnds)

    res = np.reshape(tmp.x,(4,1,3))
    #tst = np.reshape(tmp.x,(12,))



    # for k in range(len(bnds)):
    #     if (tst[k] < bnds[k][0]) or (tst[k] > bnds[k][1]):
    #         fi.write("ERROR in iteration " + str(i) + " value " +
    #                     str(k) + "\t" + str(tst[k]) + "\n")

    lapinfo[i] = ((time.time()-startTime),tmp.nit)
#    print "step ",i," iterations: ",lapinfo[i][1]," time: ",lapinfo[i][0]

    estPos[0][i+1] = res[0]
    estPos[1][i+1] = res[1]
    estPos[2][i+1] = res[2]
    estPos[3][i+1] = res[3]


#    print "time for ", i, " in sec: ", lapTime
#   Debugging...
#    print "Mat ", i
#    print modE.evalfuncMagMulti(np.concatenate((pos[0][i],pos[1][i],pos[2][i],pos[3][i])),
#                             [s1,s2,s3,s4])
#                             np.concatenate((summedInd[0][i+1],summedMid[0][i+1],summedRin[0][i+1],summedPin[0][i+1])))


#fi.close()
print "time duration: ", (time.time()-startAlg)
#estPos[0]=np.round(estPos[0],6)
#estPos[1]=np.round(estPos[1],6)
#estPos[2]=np.round(estPos[2],6)
#estPos[3]=np.round(estPos[3],6)
print "delta x estPos[0]-Index", max(estPos[0][:,0])-min(estPos[0][:,0])
print "delta x estPos[1]-Middle", max(estPos[1][:,0])-min(estPos[1][:,0])
print "delta x estPos[2]-Ring", max(estPos[2][:,0])-min(estPos[2][:,0])
print "delta x estPos[3]-Pinky", max(estPos[3][:,0])-min(estPos[3][:,0])

""" plotting stuff """
#plo.plotter3d((pos[0],pos[1],pos[2], pos[3]),("Ind real","mid Real", "ring Real", "pin Real"))
#plo.plotter2d((summedInd,summedMid,summedRin,summedPin),("index","Mid","Rin","Pin"))
plo.multiPlotter(estPos[0],"Index",pos[0])
plo.multiPlotter(estPos[1],"Middle",pos[1])
plo.multiPlotter(estPos[2],"Ring",pos[2])
plo.multiPlotter(estPos[3],"Pinky",pos[3])
plt.show()
#plo.plotter3d((pos[1],estPos[1]),("Pinky real","estOne"))
#print "delta x estPos2[1]", max(estPos2[1][:,0])-min(estPos2[1][:,0])
#print "delta x estPos2[0]", max(estPos2[0][:,0])-min(estPos2[0][:,0])
#print "delta y from pos[0] and estPos[0]", max(pos[0][:,1]-estPos[0][:,1])
#print "delta z from pos[0] and estPos[0]", max(pos[0][:,2]-estPos[0][:,2])
#print "delta y from pos[1] and estPos[1]", max(pos[1][:,1]-estPos[1][:,1])
#print "delta z from pos[1] and estPos[1]", max(pos[1][:,2]-estPos[1][:,2])
#print "delta y from pos[0] and estPos2[0]", max(pos[0][:,1]-estPos2[0][:,1])
#print "delta z from pos[0] and estPos2[0]", max(pos[0][:,2]-estPos2[0][:,2])
#print "delta y from pos[1] and estPos2[1]", max(pos[1][:,1]-estPos2[1][:,1])
#print "delta z from pos[1] and estPos2[1]", max(pos[1][:,2]-estPos2[1][:,2])

#plo.plotter3d((pos[0], estPos[0]), ("realMid", "new"))
#plo.plotter3d((pos[1], estPos[1]),("realPin","estimatedPin"))

#plt.scatter(np.arange(0,10,10/len(pos[0])),pos[0][:,0],color='r')
#plt.scatter(np.arange(0,10,10/len(pos[0])),pos[0][:,1],color='r')
#plt.scatter(np.arange(0,10,10/len(pos[0])),pos[0][:,2],color='r')
#plt.scatter(np.arange(0,10,10/len(estPos[0])),estPos[0][:,0],color='g')
#plt.scatter(np.arange(0,10,10/len(estPos[0])),estPos[0][:,1],color='g')
#plt.scatter(np.arange(0,10,10/len(estPos[0])),estPos[0][:,2],color='g')
#plt.show()

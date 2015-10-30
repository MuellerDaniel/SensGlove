
"""
Created on Wed Aug 12 09:40:01 2015

@author: daniel
"""

import dataAcquisitionMulti as datAcM
import plotting as plo
import numpy as np
import modelEqMulti as modE
import matplotlib.pyplot as plt

"""
the sensor is below the middle finger and the magnet is on the middle finger
"""

"""
    acquiring data...
"""
#print "t:"
#fingDat=datAcM.pipeAcquisition("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen", 
#                               "150825_MidPin", measNr=500, offset=100)
fingDat=datAcM.textAcquistion("150825_MidPin")
# applying average filter
avg=modE.moving_average(fingDat[0], 10)
t=np.zeros(shape=[len(avg),1])
t=np.append(t,avg,axis=1)
t=datAcM.sortData(t)
fingDat=None
fingDat=t
"""
    the artificial data...
"""
angInd = [-0.02037, 0.02272, 0.01087]         # to wooden-angle(index) (from sensor)
angMid = [0., 0.02272, 0.01087]         # to wooden-angle(middle) (from sensor)
angRin = [-0.01939, 0.02272, 0.01087]    # to wooden-angle(ring) (from sensor)
angPin = [-0.03840, 0.02272, 0.01087]     # to wooden-angle(pinky) (from sensor)
            # position of sensor
s0 = [0.00920 , 0.06755, 0.]    # sensor beneath middle
s1 = [-0.0292, 0.06755, 0.]      # sensor beneath pinky
rInd = 0.08                      # length of index finger (from angle)
rMid = 0.08829                    # length of middle finger (from angle)
rRin = 0.07979                    # length of ring finger (from angle)
rPin = 0.07215                    # length of pinky finger (from angle)
# values for the half circle
t = np.arange(0, 1/2.*np.pi, 0.001)  
pos1 = [[0.,0.,0.]]      
pos2 = [[0.,0.,0.]]
for i in t:
    pos1 = np.append(pos1, [[s0[0]+angMid[0],
                            s0[1]+angMid[1]+rMid*np.cos(i),        
                            s0[2]+angMid[2]+rMid*np.sin(i)]], axis=0)
    pos2 = np.append(pos2, [[s0[0]+angPin[0],
                            s0[1]+angPin[1],        
                            s0[2]+angPin[2]]], axis=0)
    
pos = np.zeros(shape=(2,len(pos1)-1,3))
pos[0] = pos1[1:]
pos[1] = pos2[1:]

calcB = [[[0.,0.,0.]]]      # The cumulative field measured with sensor at s0
calcB2 = [[[0.,0.,0.]]]     # The field, measured from different sensorposition (s1)
calcBMid = [[0.,0.,0.]]
cnt=0
for i in range(pos.shape[1]):
    allPos = [[[0.,0.,0.]]]
    for k in range(pos.shape[0]):
        allPos = np.append(allPos,[[pos[k][i]]],axis=0)
    allPos=allPos[1:]
    calcB = np.append(calcB,
                      modE.evalfuncMag(allPos,s0), axis=0)
    calcB2 = np.append(calcB2, 
                       modE.evalfuncMag(allPos,s1), axis=0) 
#    calcBMid = np.append(calcBMid, modE.evalfuncMag(i,s0),axis=0)
#    cnt+=1
tmp = calcB.reshape(calcB.shape[0],3)
calcB = tmp
calcB = calcB[1:]  
tmp2 = calcB2.reshape(calcB2.shape[0],3)
calcB2 = tmp2
calcB2 = calcB2[1:] 
#calcBMid = calcBMid[1:]
# add a row of zeros for plotting...
calc=np.zeros(shape=[len(calcB),1])
calc=np.append(calc,calcB,axis=1)
calc=datAcM.sortData(calc)
calc2=np.zeros(shape=[len(calcB2),1])
calc2=np.append(calc2,calcB2,axis=1)
calc2=datAcM.sortData(calc2)

delta=np.zeros(shape=[1,len(calcB),3])
delta[0]=calc[0]-calc2[0]

#calcMid=np.zeros(shape=[len(calcBMid),1])
#calcMid=np.append(calcMid,calcBMid,axis=1)
#calcMid=datAcM.sortData(calcMid)

"""
fitting the data to the model
"""
#data=modE.fitMeasurements(calc[0], fingDat[0], (0,5))
### 150825 EarthMagField = [-154.94878, -394.42383, -63.25812]
#dataS=np.zeros(shape=[len(data),1])
#dataS=np.append(dataS,data,axis=1)
#dataS=datAcM.sortData(dataS)

"""
estimating the position from the measurments
"""
#estPos = np.zeros(shape=(2,len(calcB)+1,3))
#estPos[0][0] = np.array([angMid[0]+s0[0], angMid[1]+s0[1]+rMid, s0[2]+angMid[2]])
#estPos[1][0] = np.array([angPin[0]+s0[0], angPin[1]+s0[1]+rPin, s0[2]+angPin[2]])
#                   
#bnds=((estPos[0][0][0]-0.005, estPos[0][0][0]+0.005),
#      (estPos[0][0][1], estPos[0][0][1]+rMid+0.01),
#      (estPos[0][0][2], estPos[0][0][2]+rMid+0.01),
#      
#      (estPos[1][0][0]-0.005, estPos[1][0][0]+0.005),
#      (estPos[1][0][1], estPos[1][0][1]+rPin+0.01),
#      (estPos[1][0][2], estPos[1][0][2]+rPin+0.01))                   
#      
#cnt = 0      
#for i in calcB:
#    tmp = modE.estimatePos(np.array([[estPos[0][cnt]],
#                                     [estPos[1][cnt]]]), s0, i,bnds)
#    print "estimated: ", tmp
#    estPos[0][cnt+1] = tmp[:3]      
#    estPos[1][cnt+1] = tmp[3:]
#    cnt+=1

#estimated = modE.estimatePos(estPos,s0,calcB[1],bnds)
#print "result estimation: ", estimated.reshape(2,1,3)
#print "real position: ", pos[0][1],pos[1][1]

## estimating the measured data    
##estPos=[[0.,0.,0.]]
#cnt = 0
## bounds for index finger
#bnds=((angMid[0]+s0[0]-0.003,angMid[0]+s0[0]+0.003),  
#      (angMid[1]+s0[1],angMid[1]+s0[1]+rMid),
#      (angMid[2]+s0[2],angMid[2]+s0[2]+rMid))
## bounds for middle finger
#
#for i in dataS[0]:
##    estPos = np.append(estPos, [modE.estimatePos(estPos[cnt], s0,i) * [1.,0.,1.]+[0.,angle[1]+s0[1], 0.]], axis=0)
#    estPos = np.append(estPos, [modE.estimatePos(estPos[cnt], s0, i,bnds)], axis=0)
#    cnt+=1 
## round everything to 4 decimals
#estPos = np.around(estPos,4)


plo.plotter2d((calc,calc2,delta),("calcMiddle","calcPinky","raw"), True)
#plo.plotter3d((pos[0],pos[1], estPos), ("middle","pinky", "estPos"))
#print "delta x: ", max(estPos[:,0])-min(estPos[:,0])




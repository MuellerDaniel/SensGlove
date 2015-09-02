
"""
Created on Wed Aug 12 09:40:01 2015

@author: daniel
"""

import dataAcquisitionMulti as datAcM
import plotting as plo
import numpy as np
import modelEq as modE
import matplotlib.pyplot as plt

"""
the sensor is below the middle finger and the magnet is on the middle finger
"""

"""
    acquiring data...
"""
#print "t:"
#middleOff=datAcM.pipeAcquisition("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen",
#                         "150814_middleOff", measNr=500, offset=50)
#index=datAcM.textAcquistion("150813_onHand")
middleOff=datAcM.textAcquistion("150814_middleOff")
#middleNoOff=datAcM.textAcquistion("150814_middleNoOff")
middleOff=modE.movingAvg(middleOff, 10)
"""
    the artificial data...
"""
#angle = [-0.02586, 0., 0.]         # -0.02586 to wooden-angle(index)
angle = [-0.02265, 0., 0.]         # -0.02586 to wooden-angle(middle)
            # position of sensor
#s1 = [-0.07789, 0.02825, 0.]        # index finger
s0 = [-0.06983, 0.01150, 0.]        # middle finger
#p0 = [-0.10375, 0.02825, 0.]      # initial position of magnet (index)
#r = -0.08                      # length of index finger (from angle)
r = -0.08829                    # length of middle finger
# values for the half circle
t = np.arange(0, (1/2.*np.pi), 0.01)
pos = [[0.,0.,0.]]      # representing the real positions (shifted!)
for i in t:
    pos = np.append(pos, [[((np.add(s0[0],angle[0])+r*np.cos(i))),
                                 s0[1],
                                 (s0[2]+(-1)*r*np.sin(i))]], axis=0)

pos=pos[1:]

calcB = [[0.,0.,0.]]

cnt=0
for i in pos:
    calcB = np.append(calcB, modE.evalfuncMag(i,s0), axis=0)
    cnt+=1

calcB = calcB[1:]

calc=np.zeros(shape=[len(calcB),1])
calc=np.append(calc,calcB,axis=1)
calc=datAcM.sortData(calc)

# fitting the data to the model
#offset = [30.,0.,-33.37]
#scale = [2.4505,0.,3.7334]
#bla = middleOff[0][110:370]
#bla = (bla * scale) + offset
bla=modE.fitMeasurements(calc[0],middleOff[0],(0,110))      # GREAT! the fitting things work here!
data=np.zeros(shape=[len(bla),1])
data=np.append(data,bla,axis=1)
data=datAcM.sortData(data)

# estimating the position from the measurments
estPos=[[(angle[0]+s0[0]+r), 0.01150, 0.]]
cnt = 0
for i in data[0]:
    estPos = np.append(estPos, [modE.estimatePos(estPos[cnt], s0, i)], axis=0)
    cnt+=1
# round everything to 4 decimals
estPos = np.around(estPos,4)

plo.plotter2d((calc,data),("calcB", "middleOff"), True)
plo.plotter3d((pos,estPos),("model","calc"))
#plt.clf()
#plt.plot(estPos[:,0], estPos[:,2], color='b')
#plt.plot(pos[:,0], pos[:,2], color='r')
#plt.show()

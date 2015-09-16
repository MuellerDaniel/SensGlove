
"""
Created on Wed Aug 12 09:40:01 2015

@author: daniel
"""

import dataAcquisitionMulti as datAcM
import plotting as plo
import numpy as np
import modelEqMultiTWO as modE
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
#middleOff=modE.movingAvg(middleOff, 10)
"""
    the artificial data...
"""
#angle = [-0.02586, 0., 0.]         # -0.02586 to wooden-angle(index)
angle = [0.00920, 0.09138, 0.01087]        # -0.02586 to wooden-angle(middle)
            # position of sensor
#s1 = [-0.07789, 0.02825, 0.]        # index finger
s0 = [0.00920 , 0.02755, 0.]        # middle finger
#p0 = [-0.10375, 0.02825, 0.]      # initial position of magnet (index)
#r = -0.08                      # length of index finger (from angle)
r = 0.08829                    # length of middle finger
# values for the half circle
t = np.arange(0, (1/2.*np.pi), 0.01)
pos = [[0.,0.,0.]]      # representing the real positions (shifted!)
for i in t:
    pos = np.append(pos, [[angle[0],
                            angle[1]+r*np.cos(i),
                            angle[2]+r*np.sin(i)]], axis=0)
                                 
#    pos1 = np.append(pos1, [[angInd[0],       
#                            angInd[1]+rInd*np.cos(i),        
#                            angInd[2]+rInd*np.sin(i)]], 
#                            axis=0)
pos=pos[1:]

calcB_cross = [[0.,0.,0.]]
calcB_dot = [[0.,0.,0.]]


cnt=0
for i in pos:
    calcB_cross = np.append(calcB_cross, modE.evalfuncMag(i,s0), axis=0)
    calcB_dot = np.append(calcB_dot, modE.evalfuncMagDot(i,s0), axis=0)
    cnt+=1

calcB_cross = calcB_cross[1:]
calcB_dot = calcB_dot[1:]

calc_cross=np.zeros(shape=[len(calcB_cross),1])
calc_cross=np.append(calc_cross,calcB_cross,axis=1)
calc_cross=datAcM.sortData(calc_cross)
calc_dot=np.zeros(shape=[len(calcB_dot),1])
calc_dot=np.append(calc_dot,calcB_dot,axis=1)
calc_dot=datAcM.sortData(calc_dot)

# fitting the data to the model
#offset = [30.,0.,-33.37]
#scale = [2.4505,0.,3.7334]
#bla = middleOff[0][110:370]
#bla = (bla * scale) + offset
#bla=modE.fitMeasurements(calc[0],middleOff[0],(0,110))      # GREAT! the fitting things work here!
#data=np.zeros(shape=[len(bla),1])
#data=np.append(data,bla,axis=1)
#data=datAcM.sortData(data)

# estimating the position from the measurments
#estPos=[[(angle[0]+s0[0]+r), 0.01150, 0.]]
#cnt = 0
#for i in data[0]:
#    estPos = np.append(estPos, [modE.estimatePos(estPos[cnt], s0, i)], axis=0)
#    cnt+=1
## round everything to 4 decimals
#estPos = np.around(estPos,4)

plo.plotter2d((calc_cross,calc_dot,middleOff),("calc_cross", "calc_dot", "raw meas"), True)
#plo.plotter3d((pos,estPos),("model","calc"))
#plt.clf()
#plt.plot(estPos[:,0], estPos[:,2], color='b')
#plt.plot(pos[:,0], pos[:,2], color='r')
#plt.show()

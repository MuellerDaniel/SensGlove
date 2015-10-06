
"""
Created on Wed Aug 12 09:40:01 2015

@author: daniel
"""

import dataAcquisitionMulti as datAcM
import plotting as plo
import numpy as np
import modelEqMultiTWO as modE
import matplotlib.pyplot as plt
import fcnCyPy as fcn


"""
the sensor is below the middle finger and the magnet is on the middle finger
"""


"""
    the artificial data...
"""
angle = [0.09138, 0.02957, 0.01087]         # to wooden-angle(middle)
#angle = [0., 0.02272, 0.01087]         # to wooden-angle(middle) (from sensor)
#angle = [-0.01939, 0.02272, 0.01087]    # to wooden-angle(ring) (from sensor)
#angle = [-0.03840, 0.02272, 0.01087]     # to wooden-angle(pinky) (from sensor)
            # position of sensor
s0 = [0.06755, 0.02957, 0.]     # sensor beneath middle
#s0 = [-0.06983, 0.01150, 0.]        # position of the sensor beneath the middle finger
#s0 = [0.00920 , 0.06755, 0.]
#s0=[0.,0.,0.]
#r = 0.08                      # length of index finger (from angle)
r = 0.08933                    # length of middle finger (from angle)
#r = 0.07979                    # length of ring finger (from angle)
#r = 0.07215                    # length of pinky finger (from angle)
l1 = 0.03494
l2 = 0.03102
l3 = 0.02337
# values for the half circle
t = np.arange(0, 1/2.*np.pi, 0.001)  
pos = [[0.,0.,0.]]      # representing the real positions (shifted!)
for i in t:
    pos = np.append(pos, [[angle[0]+r*np.cos(i),
                           angle[1],        
                           angle[2]+r*np.sin(i)]],
                            axis=0)
    
pos=pos[1:]

calcB = [[0.,0.,0.]]
for i in pos:
    calcB = np.append(calcB, modE.evalfuncMagDot(i,s0), axis=0)
   

calcB = calcB[1:]  
# add a row of zeros for plotting...
calc=np.zeros(shape=[len(calcB),1])
calc=np.append(calc,calcB,axis=1)
calc=datAcM.sortData(calc)


"""
estimating the positions
"""
estPos = np.zeros((len(calc[0]),3))
estPos[0] = np.array([angle[0]+r, angle[1], s0[2]])

# bounds for index finger
bnds=((angle[0],angle[0]+r),
      (angle[1]-0.003,angle[1]+0.003),        
      (angle[2],angle[2]+r))
# bounds for middle finger
cnt = 1
for i in range(len(calc[0])-1):
    res = modE.estimatePos(estPos[i],[s0],calc[0][cnt],i,bnds)
    estPos[i+1] = res.x
    # and now the angle estimation...
    cnt+=1 
# round everything to 4 decimals
estPos = np.around(estPos,4)

# just for testing. With artificial data
estPos2=[[angle[0], angle[1]+r, angle[2]]]
#estPos=[[0.,0.,0.]]
cnt = 0
#for i in calc[0]:
#    res = modE.estimatePos(estPos2[cnt], [s0], i, bnds)
#    cnt+=1 
# round everything to 4 decimals
estPos2 = np.around(estPos2,4)

plo.plotter3d((pos, estPos), ("calc","estPos2"))
plo.multiPlotter(estPos,"test",pos)
print "delta x: ", max(estPos[:,1])-min(estPos[:,1])
#print "delta y: ", max(estPos[:,1])-min(estPos[:,1])
#print "delta z: ", max(estPos[:,2])-min(estPos[:,2])
#plo.plotter3d((pos,estPosCalc),("model","calc"))
#plt.clf()




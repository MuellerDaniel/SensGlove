
"""
Created on Wed Aug 12 09:40:01 2015

@author: daniel
"""

import dataAcquisitionMulti as datAcM
import plotting as plo
import numpy as np
#import modelEqMultiTWO as modE
import modelEqMultiCython as modE
import matplotlib.pyplot as plt
import fcnCyPy as fcn


"""
the sensor is below the middle finger and the magnet is on the middle finger
"""


"""
    the artificial data...
"""
joint = [0.09138, 0.02957, -0.01087]         # to wooden-angle(middle)(MCP)
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
# length of the phalanges
phal = [0.03494, 0.03102, 0.02337]
# values for the half circle
t = np.arange(0, 1/2.*np.pi, 0.001)  
pos = [[0.,0.,0.]]      # representing the real positions (shifted!)
for i in t:
    pos = np.append(pos, [[joint[0]+r*np.cos(i),
                           joint[1],        
                           joint[2]-r*np.sin(i)]],
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
estPos[0] = np.array([joint[0]+r, joint[1], joint[2]])
# bounds for finger
bndsPos=((joint[0],joint[0]+r),
      (joint[1]-0.0001,joint[1]+0.0001),        
      (joint[2]-r,joint[2]))
      
estAngle = np.zeros((len(calc[0]),3))
estAngle[0] = np.array([0.,0.,0.])
# static bounds for angle
bndsAngle = ((0,np.pi/2),
             (0,(110/180*np.pi)),
             (0,np.pi/2))

      
cnt = 1
for i in range(len(calc[0])-1):
    epos = modE.estimatePosPy(estPos[i],[s0],calc[0][i+1],i,bndsPos)
    estPos[i+1] = epos.x
    # and now the angle estimation...
    angle = modE.estimateAngle_s(epos.x,estAngle[i],joint,phal,bndsAngle)
    estAngle[i+1] = angle.x
    
    cnt+=1 
    
# remove the y-axis motion...    
estPos[:,1] = pos[:,1]

plo.plotter3d((pos, estPos), ("calc","estPos2"))
plo.multiPlotter(estPos,"test",pos)
print "delta x: ", max(estPos[:,1])-min(estPos[:,1])
#print "delta y: ", max(estPos[:,1])-min(estPos[:,1])
#print "delta z: ", max(estPos[:,2])-min(estPos[:,2])
#plo.plotter3d((pos,estPosCalc),("model","calc"))
#plt.clf()




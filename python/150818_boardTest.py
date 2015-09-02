# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 15:53:36 2015

@author: daniel
"""
""" 
150825 The solution to the curved shape in the x-direction: there are slight 
differences in x and z b-field values (bigger!) See plots!
"""

import dataAcquisitionMulti as datAcM
import plotting as plo
import numpy as np
import modelEq as modE
import matplotlib.pyplot as plt
from timeit import default_timer as timer

""" acquiring data... """
#dat=datAcM.pipeAcquisition("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen",
#                               "150820_boardLSM1", measNr=400, offset=100)
dat=datAcM.textAcquistion("150820_boardLSM1")                       
#tmp = dat[0][45:245]
#t=np.zeros(shape=[len(tmp),1])
#t=np.append(t,tmp,axis=1)
#t=datAcM.sortData(t)
#dat=None
#dat=t
avg=modE.moving_average(dat[0], 10)
t=np.zeros(shape=[len(avg),1])
t=np.append(t,avg,axis=1)
filtered=datAcM.sortData(t)
#dat=None
#dat=t
""" the artificial data... """
angle = [0.02, 0., 0.02]    # position of the nail in the board
s0=[0.,0.,0.]               # the sensor is the origin
#r = 0.04705                      # length of index finger (from angle)
r = 0.05100
# values for the half circle
t = np.arange(0, np.pi, 0.015707963267948967)  
pos = [[0.,0.,0.]]      # representing the real positions (shifted!)
pos2 = [[0.,0.,0.]]
y=[[0.]]
cnt = 0
for i in t:
    pos = np.append(pos, [[s0[0]+angle[0],
                            s0[1]+angle[1]+r*np.cos(i),        
                            s0[2]+angle[2]+r*np.sin(i)]], axis=0)
    # the estimated position varies around 0.0105 in x-direction
    pos2 = np.append(pos2, [[s0[0]+angle[0]+(0.0105-(0.0105/10000)*(cnt-100)**2),
                            s0[1]+angle[1]+r*np.cos(i),        
                            s0[2]+angle[2]+r*np.sin(i)]], axis=0)
#    print "pos2: ", s0[0]+angle[0]+(0.0105-(0.0105/10000)*(cnt-100)**2)
#    y = np.append(y,0.0105-(0.0105/10000)*(cnt-100)**2)
    cnt+=1
    
pos=pos[1:]
pos2=pos2[1:]

calcB = [[0.,0.,0.]]
for i in pos:
    calcB = np.append(calcB, modE.evalfuncMag(i,s0), axis=0)    

calcB = calcB[1:] 

calcB2 = [[0.,0.,0.]]
for i in pos2:
    calcB2 = np.append(calcB2, modE.evalfuncMag(i,s0),axis=0)
calcB2 = calcB2[1:]
# add a row of zeros for plotting...
calc=np.zeros(shape=[len(calcB),1])
calc=np.append(calc,calcB,axis=1)
calc=datAcM.sortData(calc)
calc2=np.zeros(shape=[len(calcB2),1])
calc2=np.append(calc2,calcB2,axis=1)
calc2=datAcM.sortData(calc2)

""" fitting the data """
data=modE.fitMeasurements(calc[0], filtered[0], (0,1))
dataS=np.zeros(shape=[len(data),1])
dataS=np.append(dataS,data,axis=1)
dataS=datAcM.sortData(dataS)
#dataS=np.append(dataS,[[[-100.83703048, 247.72548755,-100.83703048]]],axis=1)   # adjusting x and z values...

# fit the curved data
dataC=modE.fitMeasurements(calc[0],calc2[0],(0,1))
dataCS=np.zeros(shape=[len(dataC),1])
dataCS=np.append(dataCS,dataC,axis=1)
dataCS=datAcM.sortData(dataCS)

#tmp=np.copy(dataS)
#tmp2 = dataS
## replace the estimated z-values with the calculated (B-field!)
#tmp2[0][:,2] = calc[0][:,2]


""" estimating position """
estPos=[[angle[0]+s0[0], angle[1]+s0[1]+r, s0[2]+angle[2]]]
#estPos=[[0.,0.,0.]]
cnt = 0
bnds = ((0.01,0.03),   # for board example
        (-0.06,0.06),
        (-0.08,0.08))
#delta1 = np.zeros(len(calc2[0]))
for i in dataS[0]:
#for i in calc2[0]:
#    estPos = np.append(estPos, [modE.estimatePos(estPos[cnt], s0,i) * [1.,0.,1.]+[0.,angle[1]+s0[1], 0.]], axis=0)
#    start = timer()
    estPos = np.append(estPos, [modE.estimatePos(estPos[cnt], s0, i, bnds)], axis=0)
#    delta1[cnt] = timer()-start
    cnt+=1 
# round everything to 4 decimals
estPos = np.around(estPos,4)

#delta2 = np.zeros(len(dataCS[0]))
# just for testing. With artificial data
estPos2=[[angle[0]+s0[0], angle[1]+s0[1]+r, s0[2]+angle[2]]]
#estPos=[[0.,0.,0.]]
cnt = 0
#for i in dataCS[0]:
##for i in calc2[0]:
##    estPos = np.append(estPos, [modE.estimatePos(estPos[cnt], s0,i) * [1.,0.,1.]+[0.,angle[1]+s0[1], 0.]], axis=0)
##    start=timer()    
#    estPos2 = np.append(estPos2, [modE.estimatePos(estPos2[cnt], s0, i)], axis=0)
##    delta2[cnt] = timer()-start
#    cnt+=1 
## round everything to 4 decimals
#estPos2 = np.around(estPos2,4)


#plo.plotter2d((calc, dataS),("calcB","measured-fit"), True)
plo.plotter3d((pos,estPos),("pos", "measured"))
# do a scatter plot of the B-values for better comparison

print "delta in x estPos: ",(max(estPos[:,0])-min(estPos[:,0]))
print "delta in x estPos2: ",(max(estPos2[:,0])-min(estPos2[:,0]))

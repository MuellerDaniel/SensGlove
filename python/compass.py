# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:53:08 2015

@author: daniel
"""

from visual import *
import serial
import signal
import sys
import string
import math
import time
from scipy.optimize import *
import numpy as np
import matplotlib.pyplot as plt


def drawCoordinates(len):
    curve(pos = [(0,0,0), (-len,0,0)], radius = 0.5, color = color.red)
    label(text = 'x', pos = (-len,0,0))
    curve(pos = [(0,0,0), (0,0,-len)], radius = 0.5, color = color.green)
    label(text = 'y', pos = (0,0,-len))
    curve(pos = [(0,0,0), (0,-len,0)], radius = 0.5, color = color.blue)
    label(text = 'z', pos = (0,-len,0))
    
    
# calculate H as crossproduct of P and R
def getH(P,S):
    return np.cross(P,(S-P))

# magnetic function
#P position of magnet
#S position of sensor
def evalfuncMag(P,S):
    H=getH(P,S)
    R = (S-P)
    return np.array([(3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5) - 
                                        H/(np.linalg.norm(R)**3))])

# magnetic function subtracting the measured B-field                                     
def funcMagY(P,S,B):    
    val = evalfuncMag(P,S)    
    #print "P",P
    #print "S",S
    #print "B", B
    res = np.linalg.norm(B - val)       
    #print "funcMag res: ",res 
    return res
    
def estimatedPos(P,S,B):
    res = minimize(funcMagY,P,args=(S,B),method='bfgs',tol=1e-2)
    return res.x

# make the window and draw the coordinate system
#scene=display(title="Compass", x=0, y=0, width=1000, height=1000)
#drawCoordinates(100)

# serial configuration
ser = serial.Serial(port='/dev/ttyACM0',baudrate=115200, timeout=1)

magMat = np.empty(shape=[0,3])     #initialize as matrix
magMat2 = np.empty(shape=[0,3])
calcPM = np.empty(shape=[0,3])
calcHM = np.empty(shape=[0,3])

b = np.array([0.,0.,0.])
s0 = np.array([0.,1.,0.])          # static location of the sensor S = (x,y,z)
estP = np.array([1.,0.,0.])          # the position of the magnet P = (a,b,c)

# for displaying an arrow
#pointer = arrow(pos = (0,0,0), axis = (0,0,0), shaftwidth = 0.5, color = color.yellow)

start_time = time.time()
cur_time = time.time()
fl = open('150707_dataMoveHo', 'w')
fl.write("# measurement started at start_time " + str(start_time) + "\n")
cnt = 0

# for plotting
#plt.ion()
#line, = plt.plot(magMat[:,0])

#signal.signal(signal.SIGINT, sigint_handler)
offset = 0
measNr = 400

try:
    while True:
        message = ser.readline()
        if(cnt < offset):
            pass
        else:
            if(cnt == offset):
                print "recording... taking " + str(measNr) + " measurements"
            mlist = string.split(message, "\t")
            #print message
            if len(mlist) > 2:       
                b[0] = 1*float(mlist[0])
                b[1] = 1*float(mlist[1])
                b[2] = 1*float(mlist[2])
            else: 
                pass

            magMat = np.append(magMat, [b])            
            
             # taking only measNr of measurements   
#            if(cnt < measNr + offset):  
#                magMat = np.append(magMat, [b])
#            else:
#                break
                
            #print "b: " + str(b[0]) + "\t" + str(b[1]) + "\t" + str(b[2])
            #estP = estimatedPos(estP, s0, b)
            #calcPM = np.append(calcPM, [estP])
            fl.write(format((time.time()-start_time), '.3f') + "\t" + str(b[0]) + "\t" + str(b[1]) + "\t" + str(b[2]) + "\n")
            #pointer.axis = 30 * norm(b)
        cnt+=1


# to catch a ctrl-c
except KeyboardInterrupt:
    print "here!"
    #pass
  
print str(cnt) + " measurements taken"
magMat = np.reshape(magMat, (magMat.size/3, 3))

offsetX = 14.741774999999986
offsetY = 8.5498749999999806
offsetZ = 33.112424999999973
i=0
for i in range (magMat.shape[0]):
    magMat[i][0] -= offsetX
    magMat[i][1] -= offsetY
    magMat[i][2] -= offsetZ
    i+=1

meanMeas = np.array([mean(magMat[:,0]), mean(magMat[:,1]), mean(magMat[:,2])])
print "meanMeas:\n" + str(meanMeas)
plt.cla()
plt.plot(magMat[:,0], 'r')
plt.plot(magMat[:,1], 'g')
plt.plot(magMat[:,2], 'b')

plt.show()

ser.close()
fl.close()







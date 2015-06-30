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
scene=display(title="Compass", x=0, y=0, width=1000, height=1000)
drawCoordinates(100)

# serial configuration
ser = serial.Serial(port='/dev/ttyACM0',baudrate=115200, timeout=1)

magMat = np.empty(shape=[0,3])     #initialize as matrix
calcPM = np.empty(shape=[0,3])
calcHM = np.empty(shape=[0,3])

b = np.array([0.,0.,0.])
s0 = np.array([0.,1.,0.])          # static location of the sensor S = (x,y,z)
estP = np.array([1.,0.,0.])          # the position of the magnet P = (a,b,c)

# for displaying an arrow
pointer = arrow(pos = (0,0,0), axis = (0,0,0), shaftwidth = 0.5, color = color.yellow)

start_time = time.time()
cur_time = time.time()
f = open('data', 'w')
f.write("# measurement started at start_time " + str(start_time) + "\n")
cnt = 0

# for plotting
#plt.ion()
#line, = plt.plot(magMat[:,0])

#signal.signal(signal.SIGINT, sigint_handler)

try:
    while True:
        
        if ((int)(time.time() - cur_time) == 5):        
            f.write("# time: " + str(time.time()-start_time) + 
                    " call nr " + str(cnt) + "\n" + "#magX\tmagY\tmagZ\n")
            print str(time.time() - start_time) + " elapsed"
            cur_time = time.time()
                   
        message = ser.readline()
        mlist = string.split(message, "\t")
        #print message
        if len(mlist) > 2:       
            b[0] = 1*float(mlist[0])
            b[1] = 1*float(mlist[1])
            b[2] = 1*float(mlist[2])
        magMat = np.append(magMat, [b])
        print "b: " + str(b[0]) + "\t" + str(b[1]) + "\t" + str(b[2])
        estP = estimatedPos(estP, s0, b)
        calcPM = np.append(calcPM, [estP])
        f.write(str(b[0]) + "\t" + str(b[1]) + "\t" + str(b[2]) + "\n")
        pointer.axis = 30 * norm(b)
        cnt+=1


# to catch a ctrl-c
except KeyboardInterrupt:
    print "here!"
    pass
  
print "tada"
magMat = np.reshape(magMat, (magMat.size/3, 3))
calcPM = np.reshape(calcPM, (calcPM.size/3, 3))
#print calcPM
#plt.subplot(212)
plt.plot(magMat[:,0], 'r') 
plt.plot(magMat[:,1], 'g') 
plt.plot(magMat[:,2], 'b')
plt.ylabel('Magnetic field strength [ugauss]')
plt.legend(('x','y','z'), loc='lower right')
plt.title('Motion')

ser.close()
f.close()







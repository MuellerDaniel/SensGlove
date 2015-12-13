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
import dataAcquisitionMulti as datAc
import subprocess


def drawCoordinates(origin,length):
    curve(pos = [origin, add(origin,(-length,0,0))], radius = 0.5, color = color.green)
    label(text = 'y', pos = add(origin,(-length,0,0)))
    curve(pos = [origin, add(origin,(0,length,0))], radius = 0.5, color = color.red)
    label(text = 'x', pos = add(origin,(0,length,0)))
    curve(pos = [origin, add(origin,(0,0,length))], radius = 0.5, color = color.blue)
    label(text = 'z', pos = add(origin,(0,0,length)))
                            

# make the window and draw the coordinate system
scene=display(title="Compass", x=0, y=0, width=1000, height=1000)
#drawCoordinates(100)


# BLE acquisition
proc = subprocess.Popen("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen".split(), 
                        stdout=subprocess.PIPE, close_fds=True)
# serial acquisition
#proc = subprocess.Popen("stty -F /dev/ttyUSB0 time 50; cat /dev/ttyUSB0", 
#                        stdout=subprocess.PIPE, close_fds=True, shell=True)                         

factor = -50
# for displaying an arrow
or1 = (-50,0,0)
or2 = (0,0,0)
or3 = (50,0,0)
or4 = (100,0,0)
pointer1 = arrow(pos = or1, axis = (factor/2,0,0), shaftwidth = 0.5, color = color.yellow)
drawCoordinates(or1,50)
pointer2 = arrow(pos = or2, axis = (factor/2,0,0), shaftwidth = 0.5, color = color.yellow)
drawCoordinates(or2,50)
pointer3 = arrow(pos = or3, axis = (factor/2,0,0), shaftwidth = 0.5, color = color.yellow)
drawCoordinates(or3,50)
pointer4 = arrow(pos = or4, axis = (factor/2,0,0), shaftwidth = 0.5, color = color.yellow)
drawCoordinates(or4,50)

#(scaleInd,offInd) = ([ 0.3218384   ,0.   ,       0.36636369], [ 145.68701635   , 0.,            3.95038916])
#(scaleMid,offMid) = ([ 0.33061685  ,0.  ,        0.32499331] ,[ 138.0537331    , 0. ,          31.91457046])
#(scaleRin,offRin) = ([ 0.36110299  ,0. ,         0.23765936] ,[ 167.70599149  ,  0.  ,         34.33928554])
#(scalePin,offPin) = ([ 0.45254456  ,0.,          0.17790589] ,[ 237.61826379 ,   0.   ,        49.06973457])

(scaleInd,offInd) = ([ 1.,1.,1.], [ 0.,0.,0.])
(scaleMid,offMid) = ([ 1.,1.,1.] ,[0.,0.,0.])
(scaleRin,offRin) = ([ 1.,1.,1.] ,[ 0.,0.,0.])
(scalePin,offPin) = ([ 1.,1.,1.] ,[ 0.,0.,0.])

try:
    while True:          
        output = proc.stdout.readline()
        b = datAc.structDataBLE(output)    
#        b = datAc.structDataSer(output)
        print "received: ",b        
        if b[0] == 0:       
            val = np.array([b[1],b[2],b[3]])            
            val = val*scaleInd+offInd
            val = np.array([val[1],-val[0],-val[2]])            
            n = factor*val/np.linalg.norm(val)
            pointer1.axis=(n)
        if b[0] == 1:          
            val = np.array([b[1],b[2],b[3]])            
            val = val*scaleMid+offMid
            val = np.array([val[1],-val[0],-val[2]])
            n = factor*val/np.linalg.norm(val)        
            pointer2.axis=(n)
        if b[0] == 2:            
            val = np.array([b[1],b[2],b[3]])            
            val = val*scaleRin+offRin
            val = np.array([val[1],-val[0],-val[2]])
            n = factor*val/np.linalg.norm(val)
            pointer3.axis=(n)
        if b[0] == 3:            
            val = np.array([b[1],b[2],b[3]])
            val = val*scalePin+offPin
            val = np.array([val[1],-val[0],-val[2]])
            n = factor*val/np.linalg.norm(val)
            pointer4.axis=(n)            


# to catch a ctrl-c
except KeyboardInterrupt:
    print "here!"
    proc.stdout.close()
    proc.kill()
    pass
  
print "tada"
#magMat = np.reshape(magMat, (magMat.size/3, 3))


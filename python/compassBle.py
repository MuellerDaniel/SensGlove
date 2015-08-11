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
import dataAcquisition as datAc
import subprocess


def drawCoordinates(len):
    curve(pos = [(0,0,0), (-len,0,0)], radius = 0.5, color = color.red)
    label(text = 'x', pos = (-len,0,0))
    curve(pos = [(0,0,0), (0,-len,0)], radius = 0.5, color = color.green)
    label(text = 'y', pos = (0,-len,0))
    curve(pos = [(0,0,0), (0,0,len)], radius = 0.5, color = color.blue)
    label(text = 'z', pos = (0,0,len))
                            

# make the window and draw the coordinate system
scene=display(title="Compass", x=0, y=0, width=1000, height=1000)
drawCoordinates(100)


# BLE acquisition
#proc = subprocess.Popen("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen".split(), 
#                        stdout=subprocess.PIPE, close_fds=True)
# serial acquisition
proc = subprocess.Popen("stty -F /dev/ttyUSB0 time 50; cat /dev/ttyUSB0", 
                        stdout=subprocess.PIPE, close_fds=True, shell=True)                         


magMat = np.empty(shape=[0,3])     #initialize as matrix

# for displaying an arrow
pointer = arrow(pos = (0,0,0), axis = (0,0,0), shaftwidth = 0.5, color = color.yellow)

start_time = time.time()
cur_time = time.time()
f = open('data', 'w')
f.write("# measurement started at start_time " + str(start_time) + "\n")
cnt = 0

try:
    while True:          
        output = proc.stdout.readline()
#        b = datAc.structDataBLE(output)    
        b = datAc.structDataSer(output)
        print "b: " + str(b[0]) + "\t" + str(b[1]) + "\t" + str(b[2])
        magMat = np.append(magMat, b)
        pointer.axis = 30 * norm(b)
        cnt+=1


# to catch a ctrl-c
except KeyboardInterrupt:
    print "here!"
    proc.stdout.close()
    proc.kill()
    pass
  
print "tada"
magMat = np.reshape(magMat, (magMat.size/3, 3))


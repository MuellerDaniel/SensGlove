# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:53:08 2015

@author: daniel
"""

"""
For displaying the sensor data as a 3D compass needle
"""

from visual import *
import serial
import string

import numpy as np



def drawCoordinates(len):
    curve(pos = [(0,0,0), (len,0,0)], radius = 0.5, color = color.red)
    label(text = 'x', pos = (len,0,0))
    curve(pos = [(0,0,0), (0,len,0)], radius = 0.5, color = color.blue)
    label(text = 'y', pos = (0,len,0))
    curve(pos = [(0,0,0), (0,0,-len)], radius = 0.5, color = color.green)
    label(text = 'z', pos = (0,0,-len))
    
    
    

# make the window and draw the coordinate system
scene=display(title="Compass", x=0, y=0, center=(0,0,-700), width=700, height=700)
drawCoordinates(100)

# serial configuration
ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600, timeout=1)

# for displaying an arrow
pointer = arrow(pos = (0,0,0), axis = (50,0,0), shaftwidth = 0.5, color = color.yellow)

cnt = 0
try:
    while True:
        message = ser.readline()
        #print message                 
        #print "recording... taking " + str(measNr) + " measurements"
        mlist = string.split(message, "\t")
        print message
        if len(mlist) > 2:  
            try: 
                b[0] = 1*float(mlist[0])
                b[1] = -1*float(mlist[2])
                b[2] = 1*float(mlist[1])
            except ValueError:
                print 'float conversion not possible ', mlist
                pass
        else: 
            pass        
#         
        pointer.axis = 30 * norm(b)
#        b = np.array([1.,1.,0.])
#        pointer.axis = b*cnt
#        cnt += 0.001
        


# to catch a ctrl-c
except KeyboardInterrupt:
    print "here!"
    
  

#print str(cnt) + " measurements taken"
#magMat = np.reshape(magMat, (magMat.size/3, 3))

ser.close()







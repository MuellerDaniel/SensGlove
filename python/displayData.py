# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 14:57:20 2015

@author: daniel
"""

import string
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import *

"""
reading the data from a textfile and saving it in a matrix
"""
def scanData(fileName):
    try:
        f = open(fileName, 'r')
    except IOError:
        print "File not found!"
    
    line = f.readline()    
    dataMat = np.empty(shape=[0,3])     
    while(line != ""):    
        if (line.startswith("#")):
            print line
        else:  
            dataString = string.split(line, "\t")
            dataMat = np.append(dataMat, 
                                [[float(dataString[0]), 
                                  float(dataString[1]), 
                                  float(dataString[2])]],axis=0)        
        line = f.readline() 
        
    return dataMat
    
"""
 functions for estimating the position and orientation
"""
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

def estimate(P,S,B):
    res = minimize(funcMagY,P,args=(S,B),method='bfgs',tol=1e-2)
    return res.x
    

noMotion = scanData("dataNoMotion")
motion = scanData("data")
p0 = np.array([1,0,0])
s0 = np.array([0,1,0])

estimatedData = []

#for i in range(noMotion.size/3):
#    print "evaluating row ", i
#    estimatedData.append(estimate(p0,s0,noMotion[i]))
    
mat = np.array(estimatedData)

   
plt.subplot(211)
plt.plot(noMotion[:,0], 'r') 
plt.plot(noMotion[:,1], 'g') 
plt.plot(noMotion[:,2], 'b')
plt.ylabel('Magnetic field strength [ugauss]')
plt.legend(('x','y','z'), loc='lower right')
plt.title('No motion')

plt.subplot(212)
plt.plot(motion[:,0], 'r') 
plt.plot(motion[:,1], 'g') 
plt.plot(motion[:,2], 'b')
plt.ylabel('Magnetic field strength [ugauss]')
plt.legend(('x','y','z'), loc='lower right')
plt.title('Motion')

plt.show()
    
#print "finished!"
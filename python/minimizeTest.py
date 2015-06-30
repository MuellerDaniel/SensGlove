# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:34:30 2015

@author: daniel
"""
from scipy.optimize import *
from math import *
import numpy as np
import time

#
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

        
def jacMag(P,S,B):
    t = evalfuncMag(P,S)
    I=np.identity(3)
    res = np.dot((I-np.dot(t,np.linalg.pinv(t))),B)
    print "jac: ",res
    return res

                
#X0 = np.array([0,0.2,-0.45,0.1,0.3,0])
X0 = np.array([0,0.2,-0.45])                
#X0 = np.reshape(X0,(6,1))
Y0 = np.array([ 1,2,3])
p0 = np.array([1,0,0])
s0 = np.array([0,1,0])
b0 = np.array([1,0.5,0.1])

start_time = time.time()
res = minimize(funcMagY,p0,args=(s0,b0),method='bfgs',tol=1e-2)
print "duration ", (time.time()-start_time)

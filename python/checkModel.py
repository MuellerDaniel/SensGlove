import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import *

def getH(P,S):
    return np.cross(P,(S-P))


def evalfuncMag(P,S):
    #H=getH(P,S)
    H = P-S
    #H = np.array([0,0,0])
    R = (S-P)
    factor = np.array([1, 1, 1])
    return np.array([((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) - 
                                        (H/(np.linalg.norm(R)**3)))] * factor)

def funcMagY(P,S,B):    
    val = evalfuncMag(P,S)    
    res = np.linalg.norm(B - val)       
    #print "funcMag res: ",res 
    return res
  
def estimate(P,S,B):
    res = minimize(funcMagY,P,args=(S,B),method='bfgs',tol=1e-5)
    return res.x        # as result you will get the P vector!                                                                        

r = 0.06
center = [-0.04, -0.01]
t = np.arange(((-1/2.)*np.pi), ((1/2.)*np.pi), 0.01)
#t = np.arange(-np.pi, 0, 0.01)

values = np.empty(shape=[0,3]) 
valuesH = np.empty(shape=[0,3])
resMat = np.empty(shape=[0,3])
res = np.array([0.,0.,0.])
i=0

s0=np.array([-0.04, -0.01, 0])

# calculate the position values
while i < t.size:
    res[0] = (center[0] + r*np.cos(t[i]))
    res[1] = (center[1] + r*np.sin(t[i]))
    res[2] = 0
    values = np.append(values, [res])    
    i+=1
    
values = np.reshape(values, (values.size/3, 3))

# calculate the orientation values
#i=0
#while i < t.size:
#    res[0] = (r*np.cos(t[i]))
#    res[1] = (r*np.sin(t[i]))
#    res[2] = 0
#    valuesH = np.append(valuesH, [res])    
#    i+=1
#
#valuesH = np.reshape(valuesH, (values.size/3, 3))

# calculate the magnetic field with the model
i=0
while i < values.shape[0]:
    resMat = np.append(resMat, evalfuncMag(values[i], s0))
    #resMat = np.append(resMat, evalfuncMagH(values[i], s0, valuesH[i]))
    i+=1
    
resMat = np.reshape(resMat, (resMat.size/3, 3))

estPos = np.empty(shape=[0,3]) 
p0 = np.array([-0.07, -0.1, 0])

i=0
for i in range (resMat.shape[0]):
    if (i == 0):     
        estPos = np.append(estPos, estimate(p0, s0, resMat[i]))
        estPos = np.reshape(estPos, (estPos.size/3, 3))
        #print "calc position nr: " + str(i) + " " + str(estPos[i])
        #print "real position: " + str(values[i])
    else:
        estPos = np.append(estPos, estimate(estPos[i-1], s0, resMat[i]))        
        estPos = np.reshape(estPos, (estPos.size/3, 3))
        #print "calc position nr: " + str(i) + " " + str(estPos[i])
        #print "real position: " + str(values[i])
    i+=1
    
plt.cla()
#plt.plot(values[:,0], values[:,1], color='y', label='values')
#plt.plot(values, color = 'y', label='values')
#plt.plot(t, resMat[:,0], color='r', label='x')
#plt.plot(t, resMat[:,1], color='g', label='y')
#plt.plot(t, resMat[:,2], color='b', label='z')
plt.plot(values[:,0], values[:,1], color='r')
plt.scatter(estPos[:,0], estPos[:,1], color='g', linestyle='solid')
#plt.xlim((t[0], t[-1]))
#plt.legend()
plt.show()
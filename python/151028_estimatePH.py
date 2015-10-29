import modelEqMultiCython as modE
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import *
import time



def evalfuncMagDotH(V,S):
    """returns the magnetic field

    Parameters
    ----------
    P : array
        the position
    H : array
        the orientation
    S : array
        the position of the sensor
    """
#    H = 1*(P-S)        # this worked for the example on the flat paper...
    R = 1*(S-V[:3])
    H = V[3:]
#    H = -R+(P-S)
    factor = np.array([1, 1, 1])
#    return [((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) -
#                                        (H/(np.linalg.norm(R)**3)))] * factor
    no = np.sqrt(R[0]**2+R[1]**2+R[2]**2)
    return [((3*(np.dot(H,R)*R)/(no**5)) - (H/(no**3)))] * factor


def funcMagY_PH(V,S,B):
    cal = evalfuncMagDotH(V,S)
    return np.linalg.norm(B-cal)
    

"""-----------------------------------------------"""

''' data for turning only the magnet (p is fixed) '''
#p = np.array([0.08, 0.,0.])
#s = np.array([0.,0.,0.])
#orien = np.array([[0.,0.,0.]])
#
#t = np.arange(0, 2*np.pi, 0.01)
#
#
#for i in t:
#    orien = np.append(orien, [[1*np.cos(i),
#                               1*np.sin(i),
#                               0]],axis=0)     
#orien = orien[1:]                              
#
#calcB = np.array([[0.,0.,0.]])
#for i in orien:
#    var = np.concatenate((p,i))
#    calcB = np.append(calcB, evalfuncMagDotH(var,s), axis=0)
#     
#calcB = calcB[1:]     

''' data for moving the magnet around the sensor on a half circle '''
p = np.array([[0., 0.,0.]])
s = np.array([0.,0.,0.])
orien = np.array([[0.,0.,0.]])
r = 0.08

t = np.arange(0, 1/2.*np.pi, 0.01)
for i in t:
    p = np.append(p,[[r*np.cos(i),
                      0,
                      r*np.sin(i)]],axis=0)    
                      
    orien = np.append(orien, [[-1*np.cos(i),
                           0,
                           1*np.sin(i)]],axis=0)    

p = p[1:]
orien = orien[1:]                              

calcB = np.array([[0.,0.,0.]])
for i in range(len(t)):
    var = np.concatenate((p[i],orien[i]))
    calcB = np.append(calcB, evalfuncMagDotH(var,s), axis=0)
     
calcB = calcB[1:]     

''' estimation '''
estimated = np.zeros((len(calcB)*2,3))
estimated[0] = p[0]
estimated[1] = orien[0]

bnds = ((-0.01, 0.09),     # the position
        (-0.001, 0.001),
        (-0.01, 0.09),
        (-1.05,1.05),    # the orientation
        (-0.05,0.05),
        (-1.05,1.05))
        
#val = minimize(funcMagY_PH,np.concatenate((estimated[0],estimated[1])),               
#                args=(s,calcB[1]),
#                method = 'slsqp',
#                bounds=bnds)
                
cnt = 0
hurray = 0
lst = np.zeros((len(calcB[1:]),))
startTime = time.time()
for i in calcB[1:]:    
    val = minimize(funcMagY_PH, np.concatenate((estimated[cnt*2],estimated[cnt*2+1])), 
                   args=(s,i), method='slsqp',
                   tol=1e-5,
                   bounds=bnds)     
    if val.success:
        hurray += 1
    lst[cnt] = val.fun
    estimated[cnt*2+2] = val.x[:3]            
    estimated[cnt*2+3] = val.x[3:]
    cnt += 1                   
#    
#    
#    
print "time needed: ",time.time()-startTime

estPos = np.zeros((len(estimated)/2,3))
estOrien = np.zeros((len(estimated)/2,3))
cnt = 0
#for i in range(len(estimated)/2):
#    estPos[i] = estimated[i*2]
#    estOrien[i] = estimated[i*2+1]
i = 0
while cnt < len(estimated):
    estPos[i] = estimated[cnt]
    estOrien[i] = estimated[cnt+1]
    i += 1
    cnt += 2

''' plotting stuff '''
plt.figure()            # estimated position
plt.plot(estPos[:,0],linestyle='-')
plt.plot(estPos[:,1],linestyle='--')
plt.plot(estPos[:,2],linestyle=':')
plt.title("estPos")

plt.figure()            # estimated orientation
plt.plot(estOrien[:,0],linestyle='-')
plt.plot(estOrien[:,1],linestyle='--')
plt.plot(estOrien[:,2],linestyle=':')
plt.title("estOrien")

plt.figure()            # the given orientation
plt.plot(p[:,0],linestyle='-')
plt.plot(p[:,1],linestyle='--')
plt.plot(p[:,2],linestyle=':')
plt.title("given position")

plt.figure()            # the given orientation
plt.plot(orien[:,0],linestyle='-')
plt.plot(orien[:,1],linestyle='--')
plt.plot(orien[:,2],linestyle=':')
plt.title("given orien")

plt.figure()            # the given orientation
plt.plot(calcB[:,0],linestyle='-')
plt.plot(calcB[:,1],linestyle='--')
plt.plot(calcB[:,2],linestyle=':')
plt.title("measured B-field")
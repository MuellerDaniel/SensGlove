import modelEqMultiCython as modE
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import *
import time


def xPos(angle,phal,off):
    return phal[0]*np.cos(angle[0])+phal[1]*np.cos((angle[0])+(angle[1]))+phal[2]*np.cos((angle[0])+(angle[1])+(angle[2]))+off
            
# for simplicity neglect it...            
def yPos(angle,phal,off):
    return off            

def zPos(angle,phal,off):
    return (phal[0]*np.sin((angle[0]))+
            phal[1]*np.sin((angle[0])+(angle[1]))+
            phal[2]*np.sin((angle[0])+(angle[1])+(angle[2])))*-1+off

def evalfuncMagAngle(theta,finger,off,S):
    """returns the magnetic field

    Parameters
    ----------
    theta : array
            the angles of the finger
    finger : array
            the length of the phalanges
    off : array
        the absolute position of the MCP
    S : array
        the position of the sensor
    """
#    H = 1*(P-S)        # this worked for the example on the flat paper...
    P = np.array([xPos(theta,finger,off[0]),
                  yPos(theta,finger,off[1]),
                  zPos(theta,finger,off[2])])
    R = S-P
#    print "R: ", R
    H = np.array([np.sin(-np.pi/2+abs(-theta[0]-theta[1]-theta[2])),
                  0,
                  np.cos(-np.pi/2+abs(-theta[0]-theta[1]-theta[2]))])
#    print "H: ",H                  
#    factor = np.array([1, 1, 1])

    no = np.sqrt(R[0]**2+R[1]**2+R[2]**2)
#    print "evalfuncMagAngle: ", ((3*(np.dot(H,R)*R)/(no**5)) - (H/(no**3))) * factor
    return np.array([((3*(np.dot(H,R)*R)/(no**5)) - (H/(no**3)))])

def funcMagY_angle(theta,finger,off,S,B):
    """The function to minimize 
        REMEMBER: pass in everything as list(or concatenated???)!!!   
        like: [theta0,theta1,...]
    """
    cal = np.zeros((len(S)*3,))  
#    print cal.shape          
    for i in range(len(S)):
        for j in range(len(theta)/3):
#            print "j: ",j
            tmp = evalfuncMagAngle(theta[j*3:j*3+3],finger[j],off[j],S[i]).reshape((3,))           
            cal[i*3:i*3+3] += tmp
        
#    cal = evalfuncMagAngle(theta,finger,off,S)     # simple approach for one magnet and one sensor
#    print "cal: ",cal
#    print "B: ", B
    return np.linalg.norm(B-cal)**2     #take the square of it!
    
'''---------------------------------------------------------------------'''

# absolute positions of wooden-joints
jointInd = [0.09138, 0.02957, -0.01087]         # to wooden-joint(index)
jointMid = [0.09138, 0.00920, -0.01087]          # to wooden-joint(middle)
jointRin = [0.09138, -0.01117, -0.01087]         # to wooden-joint(ring)
jointPin = [0.09138, -0.03154, -0.01087]         # to wooden-joint(pinky)

# position of sensor
s1 = [0.06755, 0.02957, 0.]     # sensor beneath index
#s1 = [0.08755, 0.02957, 0.]
#s2 = [0.06755, 0.00920, 0.]    
s2 = [0.04755, 0.00920, 0.]     # sensor beneath middle
s3 = [0.06755, -0.01117, 0.]    # sensor beneath ring
#s3 = [0.08755, -0.01117, 0.]
#s4 = [0.06755, -0.03012, 0.]     
s4 = [0.04755, -0.03012, 0.]    # sensor beneath pinky

# lengths of phalanges
phalInd = [0.03038, 0.02728, 0.02234]
phalMid = [0.03640, 0.03075, 0.02114]
phalRin = [0.03344, 0.02782, 0.01853]
phalPin = [0.02896, 0.02541, 0.01778]

t = np.arange(0,1/2.*np.pi,0.01)
angles = np.array([[0.,0.,0.]])
#orienN = np.array([[0.,0.,0.]])

for i in t:
    angles = np.append(angles,[[i,0,0]],axis=0)
#    orienN = np.append(orienN, [[-1*np.cos(i),        # verifying the orientation
#                               0,
#                               1*np.sin(i)]],axis=0)    
angles = angles[1:]        
#orienN = orienN[1:]
#calcOrien = np.array([[0.,0.,0.]])      # verifying the orientation
#for i in angles:
#    calcOrien = np.append(calcOrien,[[np.sin(-np.pi/2+abs(-i[0]-i[1]-i[2])),
#                  0,
#                  np.cos(-np.pi/2+abs(-i[0]-i[1]-i[2]))]], axis=0)                  
#calcOrien = calcOrien[1:]

#calcPos = np.array([[0.,0.,0.]])        # verifying the position...
#for i in angles:
#    calcPos=np.append(calcPos,
#                 [[xPos(i,phalInd,jointInd[0]),
#                  yPos(i,phalInd,jointInd[1]),
#                  zPos(i,phalInd,jointInd[2])]],axis=0)
#calcPos = calcPos[1:]                  

''' calculating the B-field '''
#calcBInd = np.array([[0.,0.,0.]])
#calcBMid = np.array([[0.,0.,0.]])
#calcBRin = np.array([[0.,0.,0.]])
#calcBPin = np.array([[0.,0.,0.]])
#calcB_old = np.array([[0.,0.,0.]])
#cnt = 0
#for i in angles:
#    calcBInd = np.append(calcBInd,evalfuncMagAngle(i,phalInd,jointInd,s1)+
#                                  evalfuncMagAngle(i,phalMid,jointMid,s1)+
#                                  evalfuncMagAngle(i,phalRin,jointRin,s1)+
#                                  evalfuncMagAngle(i,phalPin,jointPin,s1),axis=0)
#    
#    calcBMid = np.append(calcBMid,evalfuncMagAngle(i,phalInd,jointInd,s2)+
#                                  evalfuncMagAngle(i,phalMid,jointMid,s2)+
#                                  evalfuncMagAngle(i,phalRin,jointRin,s2)+
#                                  evalfuncMagAngle(i,phalPin,jointPin,s2),axis=0)
#                                  
#    calcBRin = np.append(calcBRin,evalfuncMagAngle(i,phalInd,jointInd,s3)+
#                                  evalfuncMagAngle(i,phalMid,jointMid,s3)+
#                                  evalfuncMagAngle(i,phalRin,jointRin,s3)+
#                                  evalfuncMagAngle(i,phalPin,jointPin,s3),axis=0)
#
#    calcBPin = np.append(calcBPin,evalfuncMagAngle(i,phalInd,jointInd,s4)+
#                                  evalfuncMagAngle(i,phalMid,jointMid,s4)+
#                                  evalfuncMagAngle(i,phalRin,jointRin,s4)+
#                                  evalfuncMagAngle(i,phalPin,jointPin,s4),axis=0)                                  
##    calcB_old = np.append(calcB_old,modE.evalfuncMagDotH(calcPos[cnt],calcOrien[cnt],s1),axis=0)
#    cnt += 1    
#calcBInd = calcBInd[1:]    
#calcBMid = calcBMid[1:]    
#calcBRin = calcBRin[1:]    
#calcBPin = calcBPin[1:]    
#calcB_old = calcB_old[1:]

# simply get the data from the textfile...
calcBdata = datAc.textAcquisition("151030_perfectB_H")

''' estimating the angles '''
estAngInd = np.zeros((len(t),3))
#estAngInd[0] = angles[0]
estAngMid = np.zeros((len(t),3))
#estAngMid[0] = angles[0]
estAngRin = np.zeros((len(t),3))
#estAngRin[0] = angles[0]
estAngPin = np.zeros((len(t),3))
#estAngPin[0] = angles[0]

bnds = ((0.0,np.pi/2),    # index
        (0.0,np.pi/2),
        (0.0,np.pi/2),
        (0.0,np.pi/2),    # middle
        (0.0,np.pi/2),
        (0.0,np.pi/2),
        (0.0,np.pi/2),    # ring
        (0.0,np.pi/2),
        (0.0,np.pi/2),
        (0.0,np.pi/2),    # pinky
        (0.0,np.pi/2),
        (0.0,np.pi/2))
cnt = 0
hurray = 0
#i=0
#a=funcMagY_angle(np.concatenate((estAngInd[i], estAngMid[i], estAngRin[i], estAngPin[i])),
#             [phalInd,phalMid,phalRin,phalPin],
#             [jointInd,jointMid,jointRin,jointPin],
#             [s1,s2,s3,s4],
#             np.concatenate((calcBdata[0][0],calcBdata[1][0],calcBdata[2][0],calcBdata[3][0])))
                       
for i in range(len(calcBdata[0][1:])):
    res = minimize(funcMagY_angle,
                   np.concatenate((estAngInd[i], estAngMid[i], estAngRin[i], estAngPin[i])),
                   args=([phalInd,phalMid,phalRin,phalPin],
                         [jointInd,jointMid,jointRin,jointPin],
                         [s1,s2,s3,s4],
                         np.concatenate((calcBdata[0][i+1],calcBdata[1][i+1],calcBdata[2][i+1],calcBdata[3][i+1]))),
                    method='slsqp',bounds=bnds)
    if res.success:
        hurray += 1
    else:
        print "error, iteration: ",cnt
    
    
    estAngInd[i+1] = res.x[0:3]
    estAngMid[i+1] = res.x[3:6]
    estAngRin[i+1] = res.x[6:9]
    estAngPin[i+1] = res.x[9:12]
    
    cnt += 1
    


'''----------PLOTTING----------'''

plt.close('all')

#plo.plotter2d((calcBdata[0],calcBdata[1],calcBdata[2],calcBdata[3]),("oldind","oldmid","oldrin","oldpin"))
#plo.plotter2d((calcBInd,calcBMid,calcBRin,calcBPin),("ind","mid","rin","pin"))
plo.plotter2d((estAngInd,estAngMid,estAngRin,estAngPin),("angleInd","angleMid","angleRin","anglePin"))

#plt.figure()            # the given orientation
#plt.plot(calcB[:,0],linestyle='-')
#plt.plot(calcB[:,1],linestyle='--')
#plt.plot(calcB[:,2],linestyle=':')
#plt.title("B-field")
#
#plt.figure()            # the given orientation
#plt.plot(estAng[:,0],linestyle='-')
#plt.plot(estAng[:,1],linestyle='--')
#plt.plot(estAng[:,2],linestyle=':')
#plt.title("angles")

#plt.figure()            # the given orientation
#plt.plot(orienN[:,0],linestyle='-')
#plt.plot(orienN[:,1],linestyle='--')
#plt.plot(orienN[:,2],linestyle=':')
#plt.title("optimal orientation")

#plt.figure()            # the given orientation
#plt.plot(calcOrien[:,0],linestyle='-')
#plt.plot(calcOrien[:,1],linestyle='--')
#plt.plot(calcOrien[:,2],linestyle=':')
#plt.title("calc orientation")

#plt.figure()            # the given orientation
#plt.plot(calcPos[:,0],calcPos[:,2],linestyle='-')
#plt.plot(calcPos[:,1],linestyle='--')
#plt.plot(calcPos[:,2],linestyle=':')
#plt.title("position x vs z")
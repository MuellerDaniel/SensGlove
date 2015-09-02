# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 09:53:19 2015

@author: daniel
"""

import numpy as np
import calcJacobian as cal
from scipy.optimize import *

"""
estimation equations
"""

#def evalfuncMag(P,S):
#    """returns the magnetic field
#    
#    Parameters
#    ----------
#    P : array
#        the position
#    S : array
#        the position of the sensor    
#    """
#    magnets = P.shape[0]/3      # improvement needed...
#    if magnets>1:
#        tmp=P.reshape(magnets,1,3)
#        P=tmp
##    print "P ",P
#    H = np.zeros(shape=(P.shape[0],1,3))
#    R = np.zeros(shape=(P.shape[0],1,3))
#    cnt=0
#    for i in P:
#        H[cnt] = 1*(i-S)        
#        R[cnt] = 1*(S-i)
#        cnt+=1
#    
#    factor = np.array([1, 1, 1])
#    B = np.zeros(shape=(magnets,1,3))
#    for k in range(magnets):
#        B[k] = [((3*(np.cross(H[k],R[k])*R[k])/(np.linalg.norm(R[k])**5)) - 
#                                        (H[k]/(np.linalg.norm(R[k])**3)))] * factor
##    print "B ",B
#    return B
             

def evalfuncMag(P,S):
    """returns the magnetic field
    
    Parameters
    ----------
    P : array
        the position
    S : array
        the position of the sensor    
    """
    H = 1*(P-S)        # this worked for the example on the flat paper...    
    R = 1*(S-P)
#    H = -R+(P-S)
    factor = np.array([1, 1, 1])
#    return [((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) - 
#                                        (H/(np.linalg.norm(R)**3)))] * factor
    no = np.sqrt(R[0]**2+R[1]**2+R[2]**2)
    return [((3*(np.cross(H,R)*R)/(no**5)) - 
                                        (H/(no**3)))] * factor
  

def deriv(P,S):
    # calculated by 
    a = cal.evaluate()
    
    dfxdx = a[0][0]
    dfxdy = 
    dfxdz =

    dfydx = 
    dfydy = 
    dfydz = 
    
    dfzdx = 
    dfzdy = 
    dfzdz = 

    return np.array([[dfxdx,dfxdy,dfxdz],
                     [dfydx,dfydy,dfydz],
                     [dfzdx,dfzdy,dfzdz]])    
    

                     
def funcMagY(P,S,B):
    val = np.zeros(shape=(B.shape))

    for i in range(len(S)):
#        print "P.shape ",val
        b = 0.
        for j in range(len(P)/3):
            b += evalfuncMag(P[j*3:j*3+3],S[i]) 
#            print j

#        b = evalfuncMagOne(P[:3],S[i]) + evalfuncMagOne(P[3:],S[i])     # for more than one magnet
#        b = evalfuncMagOne(P[:3],S[i])     # for one magnet
#        print "with: ", b 
        val[i*3:(i*3)+3] = b
#    print "value: ", val
#    print "B: ", B
    res = np.linalg.norm(B - val)   
#    res = np.linalg.norm(B - b)
    return res
  
def estimatePos(P,S,B,cnt,bnds=None,jaco=None):
    """returns the estimated position
    
    Parameters
    ----------
    P : array
        the initial guess of the position
    S : array
        the position of the sensor
    B : array
        the magnetic field
    bnds : tuple
            the lower and upper bounds for the position coordinates
            ((lbx,ubx),(lby,uby),(lbz,ubz))
        
    Returns
    -------
    res.x : array
        the result of the minimize function, i.e. the estimated position
    
    """
#    print "P: ", P.shape
#    c=0.1
#    cons = ({'type':'ineq',
#             'fun':lambda x: c/10 - abs(P[0]-x[0])},
#            {'type':'ineq',
#             'fun':lambda x: c - abs(P[1]-x[1])},
#            {'type':'ineq',
#             'fun':lambda x: c - abs(P[2]-x[2])},
#            {'type':'ineq',
#             'fun':lambda x: c/10 - abs(P[3]-x[3])},
#            {'type':'ineq',
#             'fun':lambda x: c - abs(P[4]-x[4])},
#            {'type':'ineq',
#             'fun':lambda x: c - abs(P[5]-x[5])},)
#    cons = ({'type':'ineq',
#             'fun':lambda x: c - abs(P-x)},)
        
#    val = minimize(funcMagY,P,args=(S,B),method='slsqp',tol=1e-5,options={'disp':True})
    val = minimize(funcMagY, P, args=(S,B), method='slsqp', 
                   tol=1e-5, bounds=bnds, jac=jaco)
#    val.x is a 2d-vector, so reshape it!
    res = np.reshape(val.x,(len(P)/3,1,3))     # improve it!
#    res = np.reshape(val.x,(1,1,3))
    if val.success:
#        print "jacobian ", val.jac
        return res        # as result you will get the P vector! 
    else:
        print "No solution found! Iteration Nr ",cnt
        print "Error message ",val.message
#        print res.message        
#        return np.zeros(shape=(2,1,3))
        return res
    
    
"""
fitting the data to the model
"""    
def fitMeasurements(ref, meas, valOffset):
    """returns the measurement data fitted to the reference data
    
    Parameters
    ----------
    ref : array
        the reference values
    meas : array
        the measured values
    valOffset : tuple
        the values for defining the initial offset (meas[valOffset[0]:valOffset[1]])
        
    Returns
    -------
    fitted : array
        the fitted measurement data
    
    """
    scaled = scaleMeasurements(ref, meas)
    fitted = shiftMeasurements(ref, scaled, valOffset)
    return fitted

def scaleMeasurements(real, meas):
    i=0
    raReal=0
    raMeas=0
    scale = np.array([0.,0.,0.])
    resMat = meas.copy()
    
    for i in range(3):
        raReal = max(real[:,i]) - min(real[:,i])
        raMeas = max(meas[:,i]) - min(meas[:,i])
        print "raMeas ", raMeas
        print "raReal ", raReal
        scale[i] = raReal/raMeas
        i+=1    
    print "scale " + str(scale)
    
    i=0
    for i in range(resMat.shape[0]):
        resMat[i][0] *= scale[0]
        resMat[i][1] *= scale[1]
        resMat[i][2] *= scale[2]
        i+=1
        
    return resMat
    
    
def shiftMeasurements(real, meas, valOffset):
    offset = real[0] - meas[0]
    resMat = meas.copy()   
    
    startMat = meas[valOffset[0]:valOffset[1]]
    meanMeas = np.array([np.mean(startMat[:,0]),
                         np.mean(startMat[:,1]),
                         np.mean(startMat[:,2])])
    offset = real[0] - meanMeas
    
    i=0
    for i in range (resMat.shape[0]):
        resMat[i][0] += offset[0]
        resMat[i][1] += offset[1]
        resMat[i][2] += offset[2]
    #    yShiftArr[i][0] += offset[0]*scale[0]
    #    yShiftArr[i][1] += offset[1]*scale[1]
    #    yShiftArr[i][2] += offset[2]*scale[2]
        i+=1
    print "offset: " + str(offset)
    return resMat

def moving_average(data, n) :
    """simple moving average filter, returns the filtered data
    
    Parameters
    ----------
    data : array
        the dataset to be filtered
    n : int
        nr of points used for the avg filter
        
    Returns
    -------
    dataFiltered : array
        the filtered dataset
    """
    ret = np.cumsum(data, dtype=float, axis=0)
#    print ret
    
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def movingAvg(data, n):
    """simple moving average filter, returns the filtered data
    
    Parameters
    ----------
    data : array
        the dataset to be filtered
    n : int
        nr of points used for the avg filter
        
    Returns
    -------
    dataFiltered : array
        the filtered dataset
    """
    dataFiltered = np.copy(data)
    cnt = n
    while cnt < data.shape[0]:
        dataFiltered[cnt] = dataFiltered[cnt-1] + (data[cnt]/n) - (data[cnt-n]/n)
        cnt+=1
        
    return dataFiltered
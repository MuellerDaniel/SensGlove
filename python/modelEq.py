# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 09:53:19 2015

@author: daniel
"""

import numpy as np
from scipy.optimize import *

"""
estimation equations
"""

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
    return np.array([((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) - 
                                        (H/(np.linalg.norm(R)**3)))] * factor)
                                    
def funcMagY(P,S,B):    
    val = evalfuncMag(P,S)    
    res = np.linalg.norm(B - val)       
#    print "funcMag res: ",res
    return res
  
def estimatePos(P,S,B,bnds=None):
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
#    print "P: ", type(P)
#    cons = ({'type':'ineq',
#             'fun':lambda x: 0.0009 - P[0]+x[0]},
#            {'type':'ineq',
#             'fun':lambda x: 0.0009 - P[1]+x[1]},
#            {'type':'ineq',
#             'fun':lambda x: 0.0009 - P[2]+x[2]},)
    
    # has to be adjusted for every position/finger
#    bnds = ((-0.04,0.04),   # for board example
#            (-0.06,0.06),
#            (-0.08,0.08))
#    bnds = ((-0.03,0.03),   # for index finger
#            (-0.2,0.2),
#            (-0.1,0.1))
             
#    res = minimize(funcMagY,P,args=(S,B),method='bfgs',tol=1e-5)
   
#    res = minimize(funcMagY, P, args=(S,B), method='slsqp', 
#                   constraints=cons, tol=1e-5, bounds=bnds)
    res = minimize(funcMagY, P, args=(S,B), method='slsqp', tol=1e-5)
#    print "The whole result thing"
#    print res
    if res.success:
#        print "Success!"
#        if (P-res.x).any() > 0.5:
#            print "delta: ", (P-res.x)
#        else: print "BELOW!!!!"
        return res.x        # as result you will get the P vector! 
    else:
        print "No solution found!", B
#        print res.message
        return res.x
    
    
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
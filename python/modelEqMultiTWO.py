# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 09:53:19 2015

@author: daniel
"""

import numpy as np
from scipy.optimize import *
from sympy import *
import time

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
#    return [((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) -
#                                        (H/(np.linalg.norm(R)**3)))] * factor
    no = np.sqrt(R[0]**2+R[1]**2+R[2]**2)
#    print "cross product: ",np.cross(H,R)
    return [((3*(np.cross(H,R)*R)/(no**5)) - (H/(no**3)))] * factor

def evalfuncMagDot(P,S):
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
    factor = np.array([-1, -1, -1])
#    return [((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) -
#                                        (H/(np.linalg.norm(R)**3)))] * factor
    no = np.sqrt(R[0]**2+R[1]**2+R[2]**2)
    return [((3*(np.dot(H,R)*R)/(no**5)) - (H/(no**3)))] * factor

def evalfuncMagH(P,H,S):
    """returns the magnetic field

    Parameters
    ----------
    P : array
        the position
    S : array
        the position of the sensor
    """
#    H = 1*(P-S)        # this worked for the example on the flat paper...
    R = 1*(S-P)
#    H = -R+(P-S)
    factor = np.array([1, 1, 1])
#    return [((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) -
#                                        (H/(np.linalg.norm(R)**3)))] * factor
    no = np.sqrt(R[0]**2+R[1]**2+R[2]**2)
    return [((3*(np.cross(H,R)*R)/(no**5)) -
                                        (H/(no**3)))] * factor

def evalfuncMagH_dot(P,H,S):
    """returns the magnetic field

    Parameters
    ----------
    P : array
        the position
    S : array
        the position of the sensor
    """
#    H = 1*(P-S)        # this worked for the example on the flat paper...
    R = 1*(S-P)
#    H = -R+(P-S)
    factor = np.array([1, 1, 1])
#    return [((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) -
#                                        (H/(np.linalg.norm(R)**3)))] * factor
    no = np.sqrt(R[0]**2+R[1]**2+R[2]**2)
    return [((3*(np.dot(H,R)*R)/(no**5)) -
                                        (H/(no**3)))] * factor

def funcMagY(P,S,B):
    # straight forward approach,
    # shape (12,)
#    print "P ", type(P)
#    print "S ", type(S)
#    print "B ", type(B)
    #l = len(P)
    #P = np.zeros((P.shape))
    val = np.zeros(shape=(B.shape))
    for i in range(len(S)):
#        print "P.shape ",val
        b = 0.
        for j in range(len(P)/3):
            b += evalfuncMagDot(P[j*3:j*3+3],S[i])
#            print "S[i] ", S[i]
#            print "P ", P[j*3:j*3+3]
        val[i*3:i*3+3] = b
    
    res = np.linalg.norm(B - val)
    #print "time needed: ", time.time()-start
    #print "result: ", res
    #print "P: ", P
    return res

def evalfuncMagMulti(P,S):
    # F matrix has the shape like in the paper
    F = np.zeros((len(S)*3,len(P)/3))     #version 1: F.shape(12,4)  B.shape(12,1)
    for i in range(len(S)):
        for j in range(int(len(P)/3)):
            F[:,j][i*3:i*3+3] = evalfuncMagDot(P[j*3:j*3+3],S[i]).T.reshape((3,))
#    F = np.zeros((len(S),len(P)))     #version 2: F.shape(4,12)    B.shape(4,3)
#    for i in range(len(S)):
#        for j in range(int(len(P)/3)):
#            F[i][j*3:j*3+3] = evalfuncMagDot(P[j*3:j*3+3],S[i])
    return F

def funcMagYmulti(P,S,B):
    # advanced approach with pseudo-inverse...
    val = evalfuncMagMulti(P,S)
#    ident = np.identity(len(S))    # version 1
    ident = np.identity(len(P))    # version 2
#    print "matrix\n", val
    res = np.linalg.norm((ident-np.mat(val)*np.mat(np.linalg.pinv(val)))*np.mat(B).T)    # version 1
#    res = np.linalg.norm((ident-np.mat(val)*np.mat(np.linalg.pinv(val)))*np.mat(B).T)    # version 2
#    valPlus=np.dot(inv(np.dot(val.T,val)),val.T)
#    res = np.linalg.norm(B-(np.dot(val,np.dot(valPlus,B))))
    return res

def estimatePos(P,S,B,cnt,bnds=None,jacobian=None):
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

    opt = ({'maxiter':30})
    '''   advanced approach (pseudo-inverse thing)  '''
#    val = minimize(funcMagYmulti, P, args=(S,B), method='slsqp',
#                   tol=1e-5, bounds=bnds, jac=jacobian)
    '''    straight forward approach norm(B(estPos)-B(measured))    '''
#    print "evaluation Nr.: ", cnt, "\n"
    val = minimize(funcMagY, P, args=(S,B), method='slsqp',
                   tol=1e-4, bounds=bnds, jac=jacobian)
    #val = fmin_slsqp(funcMagY, P, args=(S,B),
    #               bounds=bnds)
    return val    
    if val.success:
#        print "jacobian\n", val.jac
        return val        # as result you will get the P vector!
    else:
        print "No solution found! Iteration Nr ",cnt
        print "Error message ",val.message
#        print res.message
#        return np.zeros(shape=(2,1,3))
        return val


"""
calculating the jacobi
"""

def calcJacobi():
    x,y,z = symbols('x y z')
    s0,s1,s2 = symbols('s0 s1 s2')
    bx,by,bz = symbols('bx by bz')

    #H0,H1,H2 = symbols('H0 H1 H2')
    #R0,R1,R2 = symbols('R0 R1 R2')

    P = np.array([x,y,z])
    #H = np.array([H1,H2,H3])
    #R = np.array([R1,R2,R3])
    s0 = np.array([s0,s1,s2])
    H = P-s0
    R = s0-P


    fun = np.array([(3*(np.cross(H,R)*R)/(sqrt(R[0]**2+R[1]**2+R[2]**2)**5)) -
                    (H/(sqrt(R[0]**2+R[1]**2+R[2]**2))**3)])

    global symJac,norPrime
    symJac = Matrix([[fun[0][0].diff(x), fun[0][0].diff(y), fun[0][0].diff(z)],
                     [fun[0][1].diff(x), fun[0][1].diff(y), fun[0][1].diff(z)],
                     [fun[0][2].diff(x), fun[0][2].diff(y), fun[0][2].diff(z)]])

    nor =  sqrt((bx-np.sum(symJac[0:3]))**2+
                (by-np.sum(symJac[3:6]))**2+
                (bz-np.sum(symJac[6:9]))**2)

#    norPrime = np.zeros((3,1))

    norPrime = Matrix([[nor.diff(x)],
                         [nor.diff(y)],
                         [nor.diff(z)]])

    return norPrime

def jaco(P,S,B):
#    print "P ", P.shape
#    print "S ", S[0][0]
#    print "B ", B
#    print "symJac\n", symJac
    s0,s1,s2,x,y,z=symbols('s0 s1 s2 x y z')
    bx,by,bz = symbols('bx by bz')
    funSubst = np.zeros((12,1))
    res = np.zeros((12,1))
    for i in range(len(S)):
        tmp = np.zeros((3,1))
        for j in range(len(P)/3):
#                if funSubst.any()!=0:
            tmp += np.array(norPrime.subs({s0:S[i][0],s1:S[i][1],s2:S[i][2],
                                         x:P[j*3],y:P[j*3+1],z:P[j*3+2],
                                         bx:B[i*3],by:B[i*3+1],bz:B[i*3+2]}))
#                else:
#                    funSubst = np.array(symJac.subs({s0:S[i][0],s1:S[i][1],s2:S[i][2],
#                                                      x:P[j*3],y:P[j*3+1],z:P[j*3+2]}))
        funSubst[i*3] += tmp[0]
        funSubst[i*3+1] += tmp[1]
        funSubst[i*3+2] += tmp[2]

#        print funSubst

# diverentiate the norm now...
#    root=0
#    for i in range(12):
#        root += (B[i]-funSubst[i])**2
#    for i in range(12):
#        res[i] = (funSubst[i]-B[i])/sqrt(root)


#    res = funSubst.tolist()
#    funSubst = np.append(funSubst,[0.,0.,0.])
    print "res ", res
    return funSubst

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

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 09:53:19 2015

@author: daniel
"""

import numpy as np
from scipy.optimize import *
from sympy import *
import time
import fcnCyPy as fcn



"""
estimating the positions
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

def evalfuncMagDotH(P,H,S):
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
    R = 1*(S-P)
#    H = -R+(P-S)
    factor = np.array([1, 1, 1])
#    return [((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) -
#                                        (H/(np.linalg.norm(R)**3)))] * factor
    no = np.sqrt(R[0]**2+R[1]**2+R[2]**2)
    return [((3*(np.dot(H,R)*R)/(no**5)) - (H/(no**3)))] * factor

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
    val = np.zeros(shape=(B.shape))
    for i in range(len(S)):
        b = 0.
        for j in range(len(P)/3):
            b += evalfuncMagDot(P[j*3:j*3+3],S[i])
        val[i*3:i*3+3] = b
    res = np.linalg.norm(B - val)
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
    """returns the estimated position (using Cython function)

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

#    opt = ({'maxiter':100})
    '''   advanced approach (pseudo-inverse thing)  '''
#    val = minimize(funcMagYmulti, P, args=(S,B), method='slsqp',
#                   tol=1e-5, bounds=bnds, jac=jacobian)
    '''    straight forward approach norm(B(estPos)-B(measured))    '''
#    val = minimize(funcMagY, P, args=(S,B), method='slsqp',
#                   tol=1e-4, bounds=bnds, jac=jacobian, options=opt)
    val = minimize(fcn.funcMagY_cy, P, args=(S,B), method='slsqp',
                    bounds=bnds, jac=jacobian)

    if val.success:
        return val        # as result you will get the P vector!
    else:
        print "No solution found! Iteration Nr ",cnt
        print "Error message ",val.message
        return val


def estimatePosPy(P,S,B,cnt,bnds=None,jacobian=None):
    """returns the estimated position (using Python function)

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
    opt = ({'maxiter':100})
    '''   advanced approach (pseudo-inverse thing)  '''
    val = minimize(funcMagYmulti, P, args=(S,B), method='slsqp',
                   tol=1e-5, bounds=bnds, jac=jacobian)
    '''    straight forward approach norm(B(estPos)-B(measured))    '''
#    val = minimize(funcMagY, P, args=(S,B), method='slsqp',
#                   tol=1e-4, bounds=bnds, jac=jacobian, options=opt)
    if val.success:

        return val        # as result you will get the P vector!
    else:
        print "No solution found! Iteration Nr ",cnt
        print "Error message ",val.message
        return val

"""
estimating the angles
"""

def xPos(angle,phal,off):
    return (phal[0]*np.cos(angle[0])+
            phal[1]*np.cos((angle[0])+(angle[1]))+
            phal[2]*np.cos((angle[0])+(angle[1])+(angle[2]))+off)
            
# for simplicity neglect it...            
def yPos(angle,phal,off):
    return off            

def zPos(angle,phal,off):
    return (phal[0]*np.sin((angle[0]))+
            phal[1]*np.sin((angle[0])+(angle[1]))+
            phal[2]*np.sin((angle[0])+(angle[1])+(angle[2])))*-1+off
          
def calcPosition_s(angle,phal,offSet):
    res = np.array([xPos(angle,phal,offSet[0]),
                    yPos(angle,phal,offSet[1]),
                    zPos(angle,phal,offSet[2])])
    return res
          
def posFun_s(angle,pos,phal,off):
#    print "angle", angle
#    print "pos", pos
#    print "off", off
    estimated = calcPosition_s(angle,phal,off)
    diff = pos - estimated
#    print "diff: ", diff
    res = np.linalg.norm(diff)
    return res                  
                     
def estimateAngle_s(pos,guess,off,phal,bnds):
    """estimate the angle(rad) for a position (using Python function)

    Parameters
    ----------
    pos : array
        the position
    guess : array
        initial guess for the angle (in rad)
    off : array
        the offset of the finger joint 
    phal : array
        length of the three phalanges (proximal, middle, distal)
    bnds : tuple
            the (static) lower and upper bounds for the angle
            ((lbx,ubx),(lby,uby),(lbz,ubz))

    Returns
    -------
    res.x : array
        the result of the minimize function, i.e. the estimated position

    """
#    print "bla"
    res = minimize(posFun_s,guess,args=(pos,phal,off),method='slsqp',
                   bounds=bnds)
    return res    
   
   
    
def calcPosition_m(angle,phal,offSet):
    res = np.zeros((12,))
    for i in range(4):
        res[i*3:i*3+3] = np.array([xPos(angle[i*3:i*3+3],phal[i*3:i*3+3],offSet[i*3]),
                            yPos(angle[i*3:i*3+3],phal[i*3:i*3+3],offSet[i*3+1]),
                            zPos(angle[i*3:i*3+3],phal[i*3:i*3+3],offSet[i*3+2])])
    return res
          
def posFun_m(angle,pos,phal,off):
#    print "angle", angle
#    print "pos", pos
#    print "off", off
    estimated = calcPosition_m(angle,phal,off)
    diff = estimated - pos
#    print "diff: ", diff
    res = np.linalg.norm(diff)
    print "function ",res
    return res                  
                     
def estimateAngle_m(pos,guess,off,phal,bnds):
    """estimate the angle(rad) for a position (using Python function)

    Parameters
    ----------
    pos : array
        the position
    guess : array
        initial guess for the angle (in rad)
    off : array
        the offset of the finger joint 
    phal : array
        length of the three phalanges (proximal, middle, distal)
    bnds : tuple
            the (static) lower and upper bounds for the angle
            ((lbx,ubx),(lby,uby),(lbz,ubz))

    Returns
    -------
    res.x : array
        the result of the minimize function, i.e. the estimated position

    """
    # normal version
#    res = minimize(posFun_m,guess,args=(pos,phal,off),method='slsqp',
#                   bounds=bnds,tol=1e-12)    
    # calling the cython function
    res = minimize(fcn.posFun_cy,guess,args=(pos,phal,off),method='slsqp',
                   bounds=bnds)
#    res = fcn.estimateAngle_mCy(pos,guess,off,phal,bnds)

    return res       


"""
describing the whole estimation as angle-estimation
"""

def angToP(theta,finger,off):
     P = np.array([xPos(theta,finger,off[0]),
                  yPos(theta,finger,off[1]),
                  zPos(theta,finger,off[2])])
     return P             
     
def angToH(theta):
    H = np.array([np.sin(-np.pi/2+abs(-theta[0]-theta[1]-theta[2])),
                  0,
                  np.cos(-np.pi/2+abs(-theta[0]-theta[1]-theta[2]))])*factorH
    return H                  
    

def angToB(theta,finger,off,S):
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
#    factorH = np.array([0.75,0.25,0.5])
    factorH = np.array([1.,1.,1.])
    H = np.array([np.sin(-np.pi/2+abs(-theta[0]-theta[1]-theta[2])),
                  0,
                  np.cos(-np.pi/2+abs(-theta[0]-theta[1]-theta[2]))])*factorH

#    factor = np.array([1, 1, 1])
    
    factorB = np.array([1.,1.,1.])
    no = np.sqrt(R[0]**2+R[1]**2+R[2]**2)
#    print "evalfuncMagAngle: ", ((3*(np.dot(H,R)*R)/(no**5)) - (H/(no**3))) * factor
    res = np.array([((3*(np.dot(H,R)*R)/(no**5)) - (H/(no**3)))])*factorB
#    print "P[0]_py ", P[0]
#    print "res[0]_py ", res[0][0]
    return res

def funcMagY_angle(theta,finger,off,S,B):
    """The function to minimize 
    
    Parameters
    ----------
    theta : array (concatenated)
            the angles of the finger
    finger : list (of arrays)
            the length of the phalanges
    off : list (of arrays)
        the absolute positions of the MCP
    S : list (of arrays)
        the positions of the sensors
    B : array (concatenated)    
        the measured B-field
    """
    cal = np.zeros((len(S)*3,))  
#    print cal.shape          
    for i in range(len(S)):
        for j in range(len(theta)/3):
#            print "j: ",j
            tmp = angToB(theta[j*3:j*3+3],finger[j],off[j],S[i]).reshape((3,))           
            cal[i*3:i*3+3] += tmp
        
#    cal = evalfuncMagAngle(theta,finger,off,S)     # simple approach for one magnet and one sensor
#    print "python cal: ",cal
#    print "B: ", B
    return np.linalg.norm(B-cal)**2     #take the square of it!

def estimate_BtoAng(theta_0, fingerL, offL, sL, measB,bnds):
    """Estimates the angles for a certain (measured) B-field
    
    Parameters
    ----------
    theta_0 : array (concatenated)
            the angles of the finger
    fingerL : list (of arrays)
            the length of the phalanges
    offL : list (of arrays)
        the absolute positions of the MCP
    sL : list (of arrays)
        the positions of the sensors
    measB : array (concatenated)    
        the measured B-field
    bnds : tuple
        the static (inequality) bounds for the angles
    """

    # python version
    res = minimize(funcMagY_angle, theta_0, 
                   args=(fingerL, offL, sL, measB),
                   method='slsqp', bounds=bnds)
    
    # cython version
#    res = minimize(fcn.funcMagY_angle_cy, theta_0, 
#                   args=(np.reshape(fingerL,((12,))), 
#                         np.reshape(offL,((12,))), 
#                         np.reshape(sL,((12,))), measB),
#                   method='slsqp', bounds=bnds)
                      
    # returning only the angles
#    return np.array([res[0:3], res[3:6], res[6:9], res[9:12]])    
    return res

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
#    offset = real[0] - meas[0]
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


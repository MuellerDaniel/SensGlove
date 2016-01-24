import numpy as np
from scipy.optimize import *
from sympy import *
import dipModel as cy

''' BEWARE!!!
    only for list elements and multiple sensor/magnet constelations! '''


def calcB(r,h):
    Br = 12.6e+03
    mu_0 = 4*np.pi*1e-07
    mu_r = 1.05
    addFact = 1
    lamb = (Br*mu_0*mu_r)/(4*np.pi)*addFact
    factor = np.array([lamb, lamb, lamb])
    no = sqrt(float(r[0]**2+r[1]**2+r[2]**2))
    b = np.array([((3*r*np.dot(h,r))/(no**5)) - (h/(no**3))])*factor
    return b[0]
    
    
    
def angToP(theta,finger,off):
    finger_0 = 0.
    theta_k = 0.0
    theta = np.array([theta[0], theta[1], theta[1]*2./3.])
    P = np.array([(1*(finger_0*np.sin(np.pi/2.) + finger[0]*np.sin(np.pi/2-theta[0]) +              # x
                finger[1]*np.sin(np.pi/2.-theta[0]-theta[1]) +
                finger[2]*np.sin(np.pi/2.-theta[0]-theta[1]-theta[2]))+off[0]),
                ((finger[0]*np.cos(np.pi/2.-theta[0]) +                  # y
                finger[1]*np.cos(np.pi/2.-theta[0]-theta[1]) +
                finger[2]*np.cos(np.pi/2.-theta[0]-theta[1]-theta[2]))*np.sin(theta_k)+off[1]),
                (-1*(finger[0]*np.cos(np.pi/2.-theta[0]) +               # z (*-1 because you move in neg. z-direction)
                finger[1]*np.cos(np.pi/2.-theta[0]-theta[1]) +
                finger[2]*np.cos(np.pi/2.-theta[0]-theta[1]-theta[2]))*np.cos(theta_k)+off[2])])
    return P

def angToH(theta):
    # for axial magnetised cylinder magnet
    theta = np.array([theta[0], theta[1], theta[1]*2./3.])
    H = np.array([np.cos(-theta[0]-theta[1]-theta[2]),
                     0,
                     1*np.sin(-theta[0]-theta[1]-theta[2])])

    return H    
    
    

def angToBm(theta,finger,S,off):
    """returns the magnetic field

    Parameters
    ----------
    theta : array
            the angles of the finger
            [MCP,PIP,DIP]
    finger : array
            the length of the phalanges
            [proximal-, middle-, distal-phalange]
    off : array
        the shift of the joint in y-direction
    S : array
        the position of the sensor
    """
    
#    theta = np.array([theta[0], theta[1], theta[1]*(2./3.)])
#    P = angToP(theta,finger,off)
#    H = angToH(theta)
    
    B = np.zeros((1,len(S)*3))
    sensCnt = 0
    for sens in S:        
#        print "sensCnt: ", sensCnt
        for i in range(len(finger)):
#            print "i: ", i
            r = sens - angToP(theta[i*3:i*3+3],finger[i],off[i])
            h = angToH(theta[i*3:i*3+3])
            B[0][sensCnt*3:sensCnt*3+3] += calcB(r,h)            
        sensCnt += 1

    return B    
    
    
    
def minimizeAng(theta,finger,S,off,B):
    """The function to minimize

    Parameters
    ----------
    theta : array (concatenated)
            the angles of the finger
    finger : list (of arrays)
            the length of the phalanges
    off : list (of arrays)
        the y-shift of the joint
    S : list (of arrays)
        the positions of the sensors
    B : array (concatenated)
        the measured B-field
    """
    if len(S)*3 != len(B):
        print "wrong number of sensors, to corresponding B-fields!"
        return 0
    elif len(finger) != len(off):
        print "wrong number of fingerlength, to finger offsets!"
        return 0
    else:
        dif = B - angToBm(theta,finger,S,off)        
        dif = dif.astype('float')
        res = np.linalg.norm(dif)
    
        return res
        
            
def estimate_BtoAng(theta_0, fingerL, offL, sL, measB,bnds=None):
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
            
#    res = minimize(minimizeAng, theta_0,
#                    args=(fingerL, sL, offL, measB),
#                    method='slsqp', bounds=bnds)
    res = minimize(cy.minimizeAng_cy, theta_0,
                    args=(fingerL, sL, offL, measB),
                    method='slsqp', tol=1.e-05, bounds=bnds)


    return res    


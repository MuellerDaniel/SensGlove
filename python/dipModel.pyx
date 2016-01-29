import numpy as np
cimport numpy as np
# import time
# from scipy.optimize import *
# # you have to include the 'math.h' library for sqrt() and pow()!!!
from libc.math cimport pow, sqrt, cos, sin
from libc.stdlib cimport malloc,free

DTYPE = np.double

''' BEWARE!!!
    only for list elements and multiple sensor/magnet constelations! '''


def calcB_cy(np.ndarray r, np.ndarray h):
    cdef long double Br = 12.6e+03
    cdef long double mu_0 = 4*np.pi*1e-07
    cdef long double mu_r = 1.05
    cdef long double addFact = 1
    cdef long double lamb = (Br*mu_0*mu_r)/(4*np.pi)*addFact
    cdef np.ndarray factor = np.array([lamb, -lamb, lamb])
    cdef long double no = sqrt(float(r[0]**2+r[1]**2+r[2]**2))
    cdef np.ndarray b = np.array([((3*r*np.dot(h,r))/(no**5)) - (h/(no**3))])*factor
    return b[0]



def angToP_cy(np.ndarray thetaIn, np.ndarray finger, np.ndarray off):
    cdef long double finger_0 = 0.
    cdef long double theta_k = 0.0
    cdef np.ndarray theta = np.array([thetaIn[0], thetaIn[1], thetaIn[1]*2./3.])

    cdef np.ndarray P = np.array([(1*(finger_0*np.sin(np.pi/2.) + finger[0]*np.sin(np.pi/2-theta[0]) +              # x
                                    finger[1]*np.sin(np.pi/2.-theta[0]-theta[1]) +
                                    finger[2]*np.sin(np.pi/2.-theta[0]-theta[1]-theta[2]))+off[0]),
                                    ((finger[0]*np.cos(np.pi/2.-theta[0]) +                  # y
                                    finger[1]*np.cos(np.pi/2.-theta[0]-theta[1]) +
                                    finger[2]*np.cos(np.pi/2.-theta[0]-theta[1]-theta[2]))*np.sin(theta_k)+off[1]),
                                    (-1*(finger[0]*np.cos(np.pi/2.-theta[0]) +               # z (*-1 because you move in neg. z-direction)
                                    finger[1]*np.cos(np.pi/2.-theta[0]-theta[1]) +
                                    finger[2]*np.cos(np.pi/2.-theta[0]-theta[1]-theta[2]))*np.cos(theta_k)+off[2])])
    return P

def angToH_cy(np.ndarray thetaIn):
    # for axial magnetised cylinder magnet
    cdef np.ndarray theta = np.array([thetaIn[0], thetaIn[1], thetaIn[1]*2./3.])
    cdef np.ndarray H = np.array([np.cos(-theta[0]-theta[1]-theta[2]),
                                 0,
                                 1*np.sin(-theta[0]-theta[1]-theta[2])])

    return H



def angToBm_cy(np.ndarray theta,finger,S,off):
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

    cdef np.ndarray B = np.zeros((1,len(S)*3))
    cdef np.ndarray actS
    cdef np.ndarray actTheta
    cdef np.ndarray actFinger
    cdef np.ndarray actOff
    cdef np.ndarray r
    cdef np.ndarray h

    cdef int sensCnt = 0
    for sens in S:
        actS = sens
        # print "actS: ", actS
        for i in range(len(finger)):
#            print "i: ", i
            actTheta = theta[i*2:i*2+2]
            actFinger = finger[i]
            actOff = off[i]

            r = actS - angToP_cy(actTheta,actFinger,actOff)
            h = angToH_cy(actTheta)

            B[0][sensCnt*3:sensCnt*3+3] += calcB_cy(r,h)

        sensCnt += 1

    return B



def minimizeAng_cy(np.ndarray theta,finger,S,off, np.ndarray B):
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
    cdef np.ndarray dif = np.zeros((len(S),))
    cdef long double res

    if len(S)*3 != len(B):
        print "wrong number of sensors, to corresponding B-fields!"
        return 0
    elif len(finger) != len(off):
        print "wrong number of fingerlength, to finger offsets!"
        return 0
    else:
        dif = B - angToBm_cy(theta,finger,S,off)
        # dif = dif.astype('float')
        res = np.linalg.norm(dif)

        return res


def minimizePos_cy(np.ndarray p, np.ndarray h, np.ndarray measB)        :
    cdef np.ndarray dif = measB - calcB_cy(p,h)
    cdef long double res = np.linalg.norm(dif)

    return res

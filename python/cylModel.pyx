import numpy as np
cimport numpy as np
# import time
# from scipy.optimize import *
# # you have to include the 'math.h' library for sqrt() and pow()!!!
from libc.math cimport pow, sqrt, cos, sin
from libc.stdlib cimport malloc,free

DTYPE = np.double

# ctypedef np.double long_double_t DTYPE_t

def cel_bul_cy(long double kc, long double p, long double c, long double s):
    ''' approximate a complete elliptical integral with Bulirsch algorithm '''

    if kc == 0:
        c = None    # or nan???

    # errtol = 1.0e-6;
    cdef long double errtol = 1.0e-6
    cdef long double k = abs(kc)
    cdef long double em = 1.0

    cdef long double f = 0.0
    cdef long double q = 0.0
    cdef long double g = 0.0
    cdef long double kk = 0.0

    if p > 0:
        p = sqrt(p)
        s /= p
    else:
        # f = kc**2
        f = pow(kc,2)
        q = (1-f)*(s-c*p)
        g = 1-p
        f -= p
        p = sqrt(f/g)
        c = (c-s)/g
        # s = -q/((g**2)*p)+c*p
        s = -q/(pow(g,2)*p)+c*p

    f = c
    c += (s/p)
    s = 2*(s+f*k/p)
    p += k/p
    g = em
    em += k
    kk = k

    cnt = 0
    while (abs(g-k) > (g*errtol)):
       k = 2*sqrt(kk)
       kk = k*em
       f = c
       c += (s/p)
       s = 2*(s+f*kk/p)
       p = kk/p+p
       g = em
       em = k+em

       cnt += 1

    c = (np.pi/2)*(s+c*em)/(em*(em+p))
    return c


def calcB_cyl_cy(np.ndarray pos, long double ang):
    ''' calculate the B-field at a given distance and with a certain rotation of the magnet '''

    cdef np.ndarray rotMatPos = np.array([[cos(ang), -sin(ang)],
                          [sin(ang), cos(ang)]])
    cdef np.ndarray cylCo = np.dot(pos,rotMatPos)    # rotated cylindrical coordinates

    cdef long double z = cylCo[0]
    cdef long double rho = cylCo[1]

    cdef long double a = 0.0025     # radius [m]
    cdef long double b = 0.015/2    # half length of magnet [m]
    # magic value...
    cdef long double Bo = 1.0e+3*4.0107      # magnetic constant

    # component calculations
    cdef long double z_pos = z+b
    cdef long double z_neg = z-b

    cdef long double alpha_pos = a/sqrt(z_pos**2+(rho+a)**2)
    cdef long double alpha_neg = a/sqrt(z_neg**2+(rho+a)**2)

    cdef long double beta_pos = z_pos/sqrt(z_pos**2+(rho+a)**2)
    cdef long double beta_neg = z_neg/sqrt(z_neg**2+(rho+a)**2)

    cdef long double gamma = (a-rho)/(a+rho)

    cdef long double k_pos = sqrt((z_pos**2+(a-rho)**2)/(z_pos**2+(a+rho)**2))
    cdef long double k_neg = sqrt((z_neg**2+(a-rho)**2)/(z_neg**2+(a+rho)**2))

    # cel calculation with Bulirsch's algorithm
    cdef long double B_rho = Bo*(alpha_pos*cel_bul_cy(k_pos,1.,1.,-1.)-alpha_neg*cel_bul_cy(k_neg,1.,1.,-1.))
    cdef long double B_z   = (Bo*a)/(a+rho)*(beta_pos*cel_bul_cy(k_pos,gamma**2,1.,gamma)-beta_neg*cel_bul_cy(k_neg,gamma**2,1.,gamma))

    cdef np.ndarray B = np.dot(np.array([B_z, B_rho]),np.linalg.inv(rotMatPos))
#    B[1] *= -1
#    return (B, cylCo)
    return B



def angToP_cyl_cy(np.ndarray angles, np.ndarray finger):
    ''' calculate the 2d(cylindrical) position according to joint angles and fingerlengths '''

    cdef long double finger_0 = 0.
    cdef long double theta_k = 0.0
    cdef np.ndarray theta = np.array([angles[0], angles[1], angles[1]*(2./3.)])
    cdef np.ndarray pos = np.array([(1*(finger_0*np.sin(np.pi/2.) + finger[0]*np.sin(np.pi/2-theta[0]) +              # x
                                  finger[1]*np.sin(np.pi/2.-theta[0]-theta[1]) +
                                  finger[2]*np.sin(np.pi/2.-theta[0]-theta[1]-theta[2]))),

                                  (-1*(finger[0]*np.cos(np.pi/2.-theta[0]) +               # z (*-1 because you move in neg. z-direction)
                                  finger[1]*np.cos(np.pi/2.-theta[0]-theta[1]) +
                                  finger[2]*np.cos(np.pi/2.-theta[0]-theta[1]-theta[2]))*np.cos(theta_k))])

    return pos


def diffRadial(p1,p2):
    cdef long double tmp = sqrt((p1[1][0]-p2[1][0])**2+(p1[1][1]-p2[1][1])**2)*-1
    cdef np.ndarray res = np.array([p1[0]-p2[0],tmp])
    return res


def angToB_cyl_cy(np.ndarray angles, np.ndarray fingerL, sPos, jointPos):   # version positions
    ''' calculate the B-field for given finger angels '''

    cdef np.ndarray p = np.array([0., 0.])

    if type(sPos[1]) == type(jointPos[1]) == list:
        p = angToP_cyl_cy(angles,fingerL)+diffRadial(sPos,jointPos)
        # print "cy p\n",p
    else:
        p = angToP_cyl_cy(angles,fingerL)+np.array(sPos)-np.array(jointPos)
        # print "cy p else\n",p

    cdef long double ang = sum(angles)+(2./3.*angles[1])
    ang *= -1

    cdef np.ndarray B = calcB_cyl_cy(p,ang)
    B[1] *= 1      # really?
    # B = B.astype('long double')
    return B

def angToBm_cyl_cy(angles, fingerL, sPos, jointPos):
    ''' calculating the cummulative B-field for arbitrary fingers and sensors '''
    # sensCnt = 0
    # fingCnt = 0
    if type(fingerL) == type(jointPos) == type(sPos) == list:   # check whether you have everything as lists!
        # print "multiple case!"
        B = np.zeros((1,len(sPos)*2))
#        B = np.zeros((len(sPos)*2,))
        sensCnt = 0
        for sens in sPos:      # iterating over the sensors
            fingCnt = 0
            for j in fingerL:
                # cdef np.ndarray actAngles = angles[fingCnt]
                # cdef np.ndarray actFingL = fingerL[fingCnt]
                actAngles = angles[fingCnt*2:fingCnt*2+2]
                actFingL = fingerL[fingCnt]
                # B[0][sensCnt*2:sensCnt*2+2] += angToB_cyl_cy(angles[fingCnt],fingerL[fingCnt],sens,jointPos[fingCnt])
                B[0][sensCnt*2:sensCnt*2+2] += angToB_cyl_cy(actAngles,actFingL,sens,jointPos[fingCnt])
                fingCnt += 1
            sensCnt += 1

    else:
        # print "normal case!"
        B = angToB_cyl_cy(angles, fingerL, sPos, jointPos)

    return B


# this fcn is the interface to python!
def minimizeAng_cyl_cy(np.ndarray ang, fingerL, sPos, jointPos, np.ndarray measB): # version positions
    ''' objective function to minimize... '''

    # cdef np.ndarray dif = measB - angToB_cyl_cy(ang, fingerL, sPos, jointPos) # version positions
    cdef np.ndarray dif = measB - angToBm_cyl_cy(ang, fingerL, sPos, jointPos) # version positions
    cdef long double res = np.linalg.norm(dif)

    return res

import numpy as np
cimport numpy as np
# import time
# from scipy.optimize import *
# # you have to include the 'math.h' library for sqrt() and pow()!!!
from libc.math cimport pow, sqrt, cos, sin
from libc.stdlib cimport malloc,free

DTYPE = np.float

ctypedef np.float_t DTYPE_t


def cel_bul_cy(float kc, float p, float c, float s):
    ''' approximate a complete elliptical integral with Bulirsch algorithm '''

    if kc == 0:
        c = None    # or nan???

    # errtol = 1.0e-6;
    cdef float errtol = 1.0e-6
    cdef float k = abs(kc)
    cdef float em = 1.0

    cdef float f = 0.0
    cdef float q = 0.0
    cdef float g = 0.0
    cdef float kk = 0.0


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


def calcB_cyl_cy(np.ndarray pos, float ang):
    ''' calculate the B-field at a given distance and with a certain rotation of the magnet '''

    cdef np.ndarray rotMatPos = np.array([[cos(ang), -sin(ang)],
                          [sin(ang), cos(ang)]])
    cdef np.ndarray cylCo = np.dot(pos,rotMatPos)    # rotated cylindrical coordinates

    cdef float z = cylCo[0]
    cdef float rho = cylCo[1]

    cdef float a = 0.0025     # radius [m]
    cdef float b = 0.015/2    # half length of magnet [m]
    # magic value...
    cdef float Bo = 1.0e+3*4.0107      # magnetic constant

    # component calculations
    cdef float z_pos = z+b
    cdef float z_neg = z-b

    cdef float alpha_pos = a/sqrt(z_pos**2+(rho+a)**2)
    cdef float alpha_neg = a/sqrt(z_neg**2+(rho+a)**2)

    cdef float beta_pos = z_pos/sqrt(z_pos**2+(rho+a)**2)
    cdef float beta_neg = z_neg/sqrt(z_neg**2+(rho+a)**2)

    cdef float gamma = (a-rho)/(a+rho)

    cdef float k_pos = sqrt((z_pos**2+(a-rho)**2)/(z_pos**2+(a+rho)**2))
    cdef float k_neg = sqrt((z_neg**2+(a-rho)**2)/(z_neg**2+(a+rho)**2))

    # cel calculation with Bulirsch's algorithm
    cdef float B_rho = Bo*(alpha_pos*cel_bul_cy(k_pos,1.,1.,-1.)-alpha_neg*cel_bul_cy(k_neg,1.,1.,-1.))
    cdef float B_z   = (Bo*a)/(a+rho)*(beta_pos*cel_bul_cy(k_pos,gamma**2,1.,gamma)-beta_neg*cel_bul_cy(k_neg,gamma**2,1.,gamma))

    cdef np.ndarray B = np.dot(np.array([B_z, B_rho]),np.linalg.inv(rotMatPos))
#    B[1] *= -1
#    return (B, cylCo)
    return B



def angToP_cyl_cy(np.ndarray angles, np.ndarray finger):
    ''' calculate the 2d(cylindrical) position according to joint angles and fingerlengths '''

    cdef float finger_0 = 0.
    cdef float theta_k = 0.0
    cdef np.ndarray theta = np.array([angles[0], angles[1], angles[1]*(2./3.)])
    cdef np.ndarray pos = np.array([(1*(finger_0*np.sin(np.pi/2.) + finger[0]*np.sin(np.pi/2-theta[0]) +              # x
                                  finger[1]*np.sin(np.pi/2.-theta[0]-theta[1]) +
                                  finger[2]*np.sin(np.pi/2.-theta[0]-theta[1]-theta[2]))),

                                  (-1*(finger[0]*np.cos(np.pi/2.-theta[0]) +               # z (*-1 because you move in neg. z-direction)
                                  finger[1]*np.cos(np.pi/2.-theta[0]-theta[1]) +
                                  finger[2]*np.cos(np.pi/2.-theta[0]-theta[1]-theta[2]))*np.cos(theta_k))])

    return pos


def angToB_cyl_cy(np.ndarray angles, np.ndarray fingerL, np.ndarray sPos, np.ndarray jointPos):   # version positions
# def angToB_cyl_cy(np.ndarray angles, np.ndarray fingerL, np.ndarray radDist):   # version radial distance
    ''' calculate the B-field for given finger angels. CYLINDRICAL MODEL!!! '''

    cdef np.ndarray p = angToP_cyl_cy(angles,fingerL)+jointPos-sPos   #version positions
    # cdef np.ndarray p = angToP_cyl_cy(angles,fingerL)+radDist   #version radial distance

    cdef float ang = sum(angles)+(2./3.*angles[1])
    ang *= -1

    cdef np.ndarray B = calcB_cyl_cy(p,ang)
    B[1] *= 1      # really?
    B = B.astype('float')


    return B


# this fcn is the interface to python!
def minimizeAng_cyl_cy(np.ndarray ang, np.ndarray fingerL, np.ndarray sPos, np.ndarray jointPos, np.ndarray measB): # version positions
# def minimizeAng_cyl_cy(np.ndarray ang, np.ndarray fingerL, np.ndarray radDist, np.ndarray measB): # version radial distance
    ''' objective function to minimize... '''

    cdef np.ndarray dif = measB - angToB_cyl_cy(ang, fingerL, sPos, jointPos) # version positions
    # cdef np.ndarray dif = measB - angToB_cyl_cy(ang, radDist)   # version radial distance
    dif = dif.astype('float')
    cdef float res = np.linalg.norm(dif)

    return res

import numpy as np
cimport numpy as np
from libc.math cimport pow, sqrt, cos, sin
from libc.stdlib cimport malloc,free

'''
Functions for cylindrical model without adduction-abduction in Cython
compile the code by running the setupCylModel.py script
'''


DTYPE = np.double

def cel_bul(long double kc, long double p, long double c, long double s):
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


def calcB_cyl(np.ndarray pos, long double ang):
    ''' calculate the B-field at a given distance and with a certain rotation of the magnet

    Parameters
    ----------
    pos : array
        the position in 2d representation [z,rho] or [dist_lateral, dist_radial]
    ang : float
        the angle between magnetization axis and sensor orientation [rad]

     Returns
    -------
    B : array
        the magnetic field [B_z, B_rho]
    '''

    cdef np.ndarray rotMatPos = np.array([[np.cos(ang) , 0, np.sin(ang)],
                                          [0           , 1, 0       ],
                                          [-np.sin(ang), 0, np.cos(ang)]])

    cdef np.ndarray posRot = np.dot(pos,rotMatPos)

    cdef long double z = posRot[0]
    cdef long double rho = np.sqrt(posRot[1]**2+posRot[2]**2)

    cdef long double phi = np.arctan2(posRot[1], posRot[2])  # perhaps +np.pi or *-1, because z is neg???

    cdef long double a = 0.0025     # radius [m]
    cdef long double b = 0.015/2    # half length of magnet [m]
    cdef long double Br = 1.26
    # magic value...
    cdef long double Bo = Br/np.pi      # magnetic constant

    # component calculations
    cdef long double z_pos = z+b
    cdef long double z_neg = z-b

    cdef long double alpha_pos = a/np.sqrt(z_pos**2+(rho+a)**2)
    cdef long double alpha_neg = a/np.sqrt(z_neg**2+(rho+a)**2)

    cdef long double beta_pos = z_pos/np.sqrt(z_pos**2+(rho+a)**2)
    cdef long double beta_neg = z_neg/np.sqrt(z_neg**2+(rho+a)**2)

    cdef long double gamma = (a-rho)/(a+rho)

    cdef long double k_pos = np.sqrt((z_pos**2+(a-rho)**2)/(z_pos**2+(a+rho)**2))
    cdef long double k_neg = np.sqrt((z_neg**2+(a-rho)**2)/(z_neg**2+(a+rho)**2))

    # cel calculation with Bulirsch's algorithm
    cdef long double B_rho = Bo*(alpha_pos*cel_bul(k_pos,1.,1.,-1.)-alpha_neg*cel_bul(k_neg,1.,1.,-1.))
    cdef long double B_lat   = (Bo*a)/(a+rho)*(beta_pos*cel_bul(k_pos,gamma**2,1.,gamma)-beta_neg*cel_bul(k_neg,gamma**2,1.,gamma))

    cdef np.ndarray B = np.array([B_lat, B_rho*np.sin(phi), B_rho*np.cos(phi)])
    B = np.dot(B,np.linalg.inv(rotMatPos))

    # cdef long double convert = 1e+6
    # B *= convert

    return B



def angToP_cyl(np.ndarray angles, np.ndarray finger):
    ''' calculate the 2d(cylindrical) position according to joint angles and fingerlengths

    Parameters
    ----------
    angles : array
        angle of the joints [angle_MCP, angle_PIP]
    finger : array
        length of the finger phalanges [length_proximal, length_intermediate, length_distal]

    Returns
    -------
    pos : array
        position in cylindrical coordinates [p_z, p_rho]
    '''

    cdef long double finger_0 = 0.
    cdef long double theta_k = 0.0
    cdef np.ndarray theta = np.array([angles[0], angles[1], angles[1]*(2./3.)])
    cdef np.ndarray pos = np.array([(1*(finger_0*np.sin(np.pi/2.) + finger[0]*np.sin(np.pi/2-theta[0]) +              # x
                                    finger[1]*np.sin(np.pi/2.-theta[0]-theta[1]) +
                                    finger[2]*np.sin(np.pi/2.-theta[0]-theta[1]-theta[2]))),
                                    0,
                                    (-1*(finger[0]*np.cos(np.pi/2.-theta[0]) +               # z (*-1 because you move in neg. z-direction)
                                    finger[1]*np.cos(np.pi/2.-theta[0]-theta[1]) +
                                    finger[2]*np.cos(np.pi/2.-theta[0]-theta[1]-theta[2]))*np.cos(theta_k))])
    return pos


def angToB_cyl(np.ndarray angles, fingerL, sPos, jointPos):
    ''' calculate the B-field for given finger angels. CYLINDRICAL MODEL!!!

    Parameters
    ----------
    angles : 2darray
        angle of the joints [angle_MCP, angle_PIP]
    fingerL : 3darray
        length of the finger phalanges [length_proximal, length_intermediate, length_distal]
    sPos : 3darray
        the sensor position, relative to the joint ([x_lateral, x_radial])
    jointPos : 3darray
        position of the finger joint, relative to the index joint ([x_lateral, x_radial])

    Returns
    -------
    B : 3darray
        the calculated B-field at the sensor
    '''
    # pass everything as lists!!!!
    cdef np.ndarray B = np.zeros((3,))
    cdef int sCnt = 0
    cdef np.ndarray actAngles = np.zeros((2,))
    cdef np.ndarray p = np.zeros((3,))
    cdef long double ang = 0.0

    if type(sPos) == type(jointPos) == type(fingerL) == list:
#        print "here!"
        if len(jointPos) == len(fingerL) == len(angles)/2:
            B = np.zeros((3*len(sPos),))
            # cdef int sCnt = 0
            for i in sPos:
                for j in range(len(jointPos)):
                    actAngles = angles[j*2:j*2+2]
                    p = ((angToP_cyl(actAngles,fingerL[j])+jointPos[j]) - i)
                    # print "cy cyl: ", p
                    ang = sum(actAngles)+(2./3.*actAngles[1])
                    B[sCnt*3:sCnt*3+3] += calcB_cyl(p,ang)
                sCnt += 1
            return B
        else:
            print "ERROR! wrong combination of lists"
            return -1

    else:
        p = angToP_cyl(angles, fingerL)+(sPos-jointPos)
        ang = sum(angles)+(2./3.*angles[1])
        B = calcB_cyl(p,ang)
        return B


def minimizeAng_cyl(np.ndarray ang, fingerL, sPos, jointPos, np.ndarray measB):
    ''' objective function to minimize for b-field on hand '''

    cdef np.ndarray dif = measB - angToB_cyl(ang, fingerL, sPos, jointPos)

    # dif = dif.astype('float')
    cdef long double res = np.linalg.norm(dif)

    return res



def minimizeB_cyl_cy(np.ndarray pos, long double ang, np.ndarray measB):
    ''' objective function to minimize for position-angle combinations '''

    cdef np.ndarray dif = measB - calcB_cyl(pos,ang)
    # dif = dif.astype('float')       # I have to do it, otherwise a numpy.linalg.norm can not be applied...
    cdef long double res = np.linalg.norm(dif)

    return res

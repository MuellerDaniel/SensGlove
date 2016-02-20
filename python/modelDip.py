import numpy as np
from scipy.optimize import *
from sympy import *
import dipModel as cy

''' BEWARE!!!
    only for list elements and multiple sensor/magnet constelations! '''


def calcB(r,h_in):
    # print "calcBDIP h:", h
    Br = 1.26
    mu_0 = 4*np.pi*1e-07
    r_mag = 0.0025
    l_mag = 0.015
    m = Br*(np.pi*r_mag**2*l_mag)/mu_0      # magnetic dipole moment
    h = h_in*m

    # print "calcBDIP m:", m

    no = np.sqrt(float(r[0]**2+r[1]**2+r[2]**2))
    b = np.array([((3*r*np.dot(h,r))/(no**5)) - (h/(no**3))]) * (mu_0/(4.*np.pi))

    res = b[0]
    # convert = 1e+6      # output is in muT
    # res = b[0]*convert
    return res



def angToP(theta,finger,off):
    theta_k = 0.0
    theta = np.array([theta[0], theta[1], theta[1]*2./3.])
    P = np.array([(finger[0]*np.sin(np.pi/2-theta[0]) +              # x
                finger[1]*np.sin(np.pi/2.-theta[0]-theta[1]) +
                finger[2]*np.sin(np.pi/2.-theta[0]-theta[1]-theta[2])+off[0]),
                (off[1]),
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
            r = (angToP(theta[i*2:i*2+2],finger[i],off[i]) - sens)
#            r = sens - angToP(theta[i*2:i*2+2],finger[i],off[i])
#            print "dipole: ",r
            h = angToH(theta[i*2:i*2+2])
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


def estimate_BtoAng(theta_0, fingerL, sL, offL, measB,bnds=None, method=0):
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

    dif = 1e-05

    # res = minimize(minimizeAng, theta_0,
    #                args=(fingerL, sL, offL, measB),
    #                method='slsqp', bounds=bnds)
    # res = minimize(minimizeAng, theta_0,
    #                args=(fingerL, sL, offL, measB),
    #                method='bfgs', tol=1.e-05)
    # return res

    if method == 0:
        res = minimize(cy.minimizeAng_cy, theta_0,
                         args=(fingerL, sL, offL, measB),
                         method='bfgs', tol=dif)
        return res

    if method == 1:
        res = minimize(cy.minimizeAng_cy, theta_0,
                         args=(fingerL, sL, offL, measB),
                         method='slsqp', tol=dif, bounds=bnds)
        return res

    if method == 2:
        res = minimize(cy.minimizeAng_cy, theta_0,
                         args=(fingerL, sL, offL, measB),
                         method='cobyla', tol=dif)
        return res


def estimateSeries(meas, fingerL, sL, offL, bnds=False, met=0, theta_0=None):
    b = ((0.0,np.pi/2.),
    (0.0,np.pi*(110./180.)),
    (0.0,np.pi/2.),
    (0.0,np.pi*(110./180.)),
    (0.0,np.pi/2.),
    (0.0,np.pi*(110./180.)),
    (0.0,np.pi/2.),
    (0.0,np.pi*(110./180.)))

    estAng = np.zeros((len(meas), 2*len(fingerL)))

    for i in range(1,len(meas)):
        # print "modelDip.py estimation step: ",i
        res = estimate_BtoAng(estAng[i-1], fingerL, sL, offL, meas[i], bnds=b[:len(fingerL)*2],method=met)
        estAng[i] = res.x
        # if met == 0:
        #     res = estimate_BtoAng(estAng[i-1], fingerL, sL, offL, meas[i], bnds=None,method=met)
        #     estAng[i] = res.x
        # elif bnds:
        #     res = estimate_BtoAng(estAng[i-1], fingerL, sL, offL, meas[i], bnds=b[:len(fingerL)*2],method=met)
        #     estAng[i] = res.x
        # else:
        #     res = estimate_BtoAng(estAng[i-1], fingerL, sL, offL, meas[i],method=0)
        #     estAng[i] = res.x


    # add the DIP states
    dips = np.zeros((len(estAng),len(estAng[0])/2))
    for i in range(0,int(len(estAng[0])/2)):
        dips[:,i] = (estAng[:,i*2+1]*(2./3.))
    cnt = 0
    for i in range(2,int(len(estAng[0])+2),3):
        estAng = np.insert(estAng,i,dips[:,cnt],1)
        cnt += 1

    return estAng



def minimizePos(p, h, measB):
    dif = measB - calcB(p, h)
    dif = dif.astype('float')       # I have to do it, otherwise a numpy.linalg.norm can not be applied...
    res = np.linalg.norm(dif)
    return res


def estimatePos(p_0, h, measB):

#    res = minimize(minimizePos, p_0, args=(h, measB), method='bfgs', tol=1.e-05)
    res = minimize(cy.minimizePos_cy, p_0, args=(h, measB), method='bfgs')

    return res

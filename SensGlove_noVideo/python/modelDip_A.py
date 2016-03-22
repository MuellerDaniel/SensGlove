import numpy as np
from scipy.optimize import *
import dipModel_A as cy
import math

'''
Functions for dipole model with adduction-abduction in Python
'''

def calcB(r,h_in):
    Br = 1.26
    mu_0 = 4*np.pi*1e-07
    r_mag = 0.0025
    l_mag = 0.015
    m = Br*(np.pi*r_mag**2*l_mag)/mu_0      # magnetic dipole moment
    h = h_in*m

    no = np.sqrt(float(r[0]**2+r[1]**2+r[2]**2))
    b = np.array([((3*r*np.dot(h,r))/(no**5)) - (h/(no**3))]) * (mu_0/(4.*np.pi))

    res = b[0]
    # convert = 1e+3      # output is in muT
    # res = b[0]*convert
    return res

def angToP(theta_in,finger,off):
    psi = theta_in[2]
    theta = np.array([theta_in[0], theta_in[1], theta_in[1]*2./3.])

    P = np.array([(finger[0]*np.sin(np.pi/2-theta[0]) +              # x
                finger[1]*np.sin(np.pi/2.-theta[0]-theta[1]) +
                finger[2]*np.sin(np.pi/2.-theta[0]-theta[1]-theta[2])+off[0]),

                ((finger[0]*np.cos(np.pi/2-theta[0]) +
                finger[1]*np.cos(np.pi/2-theta[0]-theta[1]) +
                finger[2]*np.cos(np.pi/2-theta[0]-theta[1]-theta[2]))*np.sin(psi)+off[1]),

                (-1*(finger[0]*np.cos(np.pi/2.-theta[0]) +               # z (*-1 because you move in neg. z-direction)
                finger[1]*np.cos(np.pi/2.-theta[0]-theta[1]) +
                finger[2]*np.cos(np.pi/2.-theta[0]-theta[1]-theta[2]))*np.cos(psi)+off[2])])
    return P

def angToH(theta_in):
    # for axial magnetised cylinder magnet
    psi = theta_in[2]
    theta = np.array([theta_in[0], theta_in[1], theta_in[1]*2./3.])

    H = np.array([np.cos(-theta[0]-theta[1]-theta[2]),
                  np.cos(-theta[0]-theta[1]-theta[2])*np.sin(psi),
                  np.sin(-theta[0]-theta[1]-theta[2])*np.cos(psi)])

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
            # r is pointing from sensor to magnet
            r = (angToP(theta[i*3:i*3+3],finger[i],off[i]) - sens)
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

def magnitude(x):
    return int(math.floor(math.log10(abs(-x))))

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
    dif = 1*10**(magnitude(measB[0])-7)

    # res = minimize(minimizeAng, theta_0,
    #               args=(fingerL, sL, offL, measB),
    #               method='bfgs', tol=1.e-05)

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
                         method='L-BFGS-B', bounds=bnds, tol=dif)
    return res



def estimateSeries(meas, fingerL, sL, offL, bnds=False, met=0, theta_0=None):
    b = ((0.0,np.pi/2.),
    (0.0,np.pi*(110./180.)),
    (-(30./180)*np.pi,(30./180)*np.pi),
    (0.0,np.pi/2.),
    (0.0,np.pi*(110./180.)),
    (-(30./180)*np.pi,(30./180)*np.pi),
    (0.0,np.pi/2.),
    (0.0,np.pi*(110./180.)),
    (-(30./180)*np.pi,(30./180)*np.pi),
    (0.0,np.pi/2.),
    (0.0,np.pi*(110./180.)),
    (-(30./180)*np.pi,(30./180)*np.pi))

    estAng = np.zeros((len(meas), 3*len(fingerL)))

    for i in range(1,len(meas)):
        # print "modelDip_A.py estimation step: ",i
        res = estimate_BtoAng(estAng[i-1], fingerL, sL, offL, meas[i], bnds=b[:len(fingerL)*3],method=met)
        estAng[i] = res.x
        # if met == 0:
        #     res = estimate_BtoAng(estAng[i-1], fingerL, sL, offL, meas[i], bnds=None,method=0)
        #     estAng[i] = res.x
        # elif bnds:
        #     res = estimate_BtoAng(estAng[i-1], fingerL, sL, offL, meas[i], bnds=b[:len(fingerL)*3],method=met)
        #     estAng[i] = res.x
        # else:
        #     res = estimate_BtoAng(estAng[i-1], fingerL, sL, offL, meas[i],method=0)
        #     estAng[i] = res.x

    # add the DIP states
    dips = np.zeros((len(estAng),len(estAng[0])/3))
    for i in range(0,int(len(estAng[0])/3)):
        dips[:,i] = (estAng[:,i*3+1]*(2./3.))
    cnt = 0
    for i in range(2,int(len(estAng[0])+3),4):
        estAng = np.insert(estAng,i,dips[:,cnt],1)
        cnt += 1

    return estAng

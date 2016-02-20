import numpy as np
from scipy.optimize import *
import cylModel_A as cy


def cel_bul(kc,p,c,s):
    ''' approximate a complete elliptical integral with Bulirsch algorithm '''

    if kc == 0:
        c = None    # or nan???

    # errtol = 1.0e-6;
    errtol = 1.0e-6
    k = abs(kc)
    em = 1.0

    if p > 0:
        p = np.sqrt(p)
        s /= p
    else:
        f = kc**2
        q = (1-f)*(s-c*p)
        g = 1-p
        f -= p
        p = np.sqrt(f/g)
        c = (c-s)/g
        s = -q/((g**2)*p)+c*p

    f = c
    c += (s/p)
    s = 2*(s+f*k/p)
    p += k/p
    g = em
    em += k
    kk = k

    cnt = 0
    while (abs(g-k) > (g*errtol)):
       k = 2*np.sqrt(kk)
       kk = k*em
       f = c
       c += (s/p)
       s = 2*(s+f*kk/p)
       p = kk/p+p
       g = em
       em = k+em

       cnt += 1

    c = (np.pi/2)*(s+c*em)/(em*(em+p))
#    c = float(c)
#    print "steps needed: ", cnt
    return c


def calcB_cyl(pos, angles):
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

    angY = angles[0]
    rotY = np.array([[np.cos(angY), 0., np.sin(angY)],
                      [0.          , 1., 0.       ],
                      [-np.sin(angY), 0., np.cos(angY)]])

    angZ = angles[1]
    rotZ = np.array([[np.cos(angZ), -np.sin(angZ), 0.],
                      [ np.sin(angZ),  np.cos(angZ), 0.],
                      [ 0.         , 0.          , 1.]])

    rotG = np.dot(rotZ,rotY)

    posRot = np.dot(pos,rotG)

    z = posRot[0]
    rho = np.sqrt(posRot[1]**2+posRot[2]**2)

    phi = np.arctan2(posRot[1], posRot[2])  # perhaps +np.pi or *-1, because z is neg???

#    print "phi: ",phi

    a = 0.0025     # radius [m]
    b = 0.015/2    # half length of magnet [m]
    Br = 1.26

    Bo = Br/np.pi      # magnetic constant

    # component calculations
    z_pos = z+b
    z_neg = z-b

    alpha_pos = a/np.sqrt(z_pos**2+(rho+a)**2)
    alpha_neg = a/np.sqrt(z_neg**2+(rho+a)**2)

    beta_pos = z_pos/np.sqrt(z_pos**2+(rho+a)**2)
    beta_neg = z_neg/np.sqrt(z_neg**2+(rho+a)**2)

    gamma = (a-rho)/(a+rho)

    k_pos = np.sqrt((z_pos**2+(a-rho)**2)/(z_pos**2+(a+rho)**2))
    k_neg = np.sqrt((z_neg**2+(a-rho)**2)/(z_neg**2+(a+rho)**2))

    # cel calculation with Bulirsch's algorithm
    B_rho = Bo*(alpha_pos*cel_bul(k_pos,1.,1.,-1.)-alpha_neg*cel_bul(k_neg,1.,1.,-1.))
    B_lat   = (Bo*a)/(a+rho)*(beta_pos*cel_bul(k_pos,gamma**2,1.,gamma)-beta_neg*cel_bul(k_neg,gamma**2,1.,gamma))

    B = np.array([B_lat, B_rho*np.sin(phi), B_rho*np.cos(phi)])
    B = np.dot(B,np.linalg.inv(rotG))

    # convert = 1e+6  # output is in muT
    # B *= convert

    return B


def angToP_cyl(angles, finger):
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

    finger_0 = 0.
    psi = angles[2]
    theta = np.array([angles[0], angles[1], angles[1]*2./3.])

    pos = np.array([(1*(finger_0*np.sin(np.pi/2.) + finger[0]*np.sin(np.pi/2-theta[0]) +              # x
                finger[1]*np.sin(np.pi/2.-theta[0]-theta[1]) +
                finger[2]*np.sin(np.pi/2.-theta[0]-theta[1]-theta[2]))),

                ((finger[0]*np.cos(np.pi/2-theta[0]) +
                finger[1]*np.cos(np.pi/2-theta[0]-theta[1]) +
                finger[2]*np.cos(np.pi/2-theta[0]-theta[1]-theta[2]))*np.sin(psi)),

                (-1*(finger[0]*np.cos(np.pi/2.-theta[0]) +               # z (*-1 because you move in neg. z-direction)
                finger[1]*np.cos(np.pi/2.-theta[0]-theta[1]) +
                finger[2]*np.cos(np.pi/2.-theta[0]-theta[1]-theta[2]))*np.cos(psi))])

    return pos


def angToB_cyl(angles, fingerL, sPos, jointPos):
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
    if type(sPos) == type(jointPos) == type(fingerL) == list:
#        print "here!"
        if len(jointPos) == len(fingerL) == len(angles)/3:
            B = np.zeros((3*len(sPos),))
            sCnt = 0
            for i in sPos:
                for j in range(len(jointPos)):
                    actAngles = angles[j*3:j*3+3]
                    p = ((angToP_cyl(actAngles,fingerL[j])+jointPos[j]) - i)
#                    print "cyl: ",p
                    ang = [actAngles[0]+actAngles[1]*5./3., actAngles[2]]
                    # print "py: ", ang
                    B[sCnt*3:sCnt*3+3] += calcB_cyl(p,ang)
                sCnt += 1
            return B
        else:
            print "ERROR! wrong combination of lists"
            return -1

    # or as a np.ndarray...
    else:
        p = angToP_cyl(angles, fingerL)+(sPos-jointPos)
        ang = sum(angles)+(2./3.*angles[1])
        B = calcB_cyl(p,ang)
        return B


def minimizeAng_cyl(ang, fingerL, sPos, jointPos, measB):
    ''' objective function to minimize... '''

    dif = measB - angToB_cyl(ang, fingerL, sPos, jointPos)

    dif = dif.astype('float')
    res = np.linalg.norm(dif)

    return res


def estimateAng_cyl(theta_0, fingerL, sL, offL, measB, bnds=None, method=0):
    ''' estimating the joint angles

    Parameters
    ----------
    ang_0 : 2darray
        initial guess of angles [angle_MCP, angle_PIP]
    fingerL : 3darray
        length of the finger phalanges [length_proximal, length_intermediate, length_distal]
    sPos : 2darray
        the sensor position, relative to the joint ([x_lateral, x_radial])
    jointPos : 2darray
        position of the finger joint, relative to the index joint ([x_lateral, x_radial])
        the measured B-field ([B_z, B_rho])

    Returns
    -------
    res : OptimizeResult

    '''
    dif = 1e-05
#    res = minimize(minimizeAng_cyl,ang_0,
#                   args=(fingerL, sPos, jointPos, measB),
#                    method='bfgs', tol=1.e-05)

#    res = minimize(cy.minimizeAng_cyl,ang_0,
#                   args=(fingerL, sPos, jointPos, measB),
#                    method='bfgs', tol=1.e-05)

    if method == 0:
        res = minimize(cy.minimizeAng_cyl, theta_0,
                         args=(fingerL, sL, offL, measB),
                         method='bfgs', tol=dif)
        return res

    if method == 1:
        res = minimize(cy.minimizeAng_cyl, theta_0,
                         args=(fingerL, sL, offL, measB),
                         method='slsqp', tol=dif, bounds=bnds)
        return res

    if method == 2:
        res = minimize(cy.minimizeAng_cyl, theta_0,
                         args=(fingerL, sL, offL, measB),
                         method='cobyla', tol=dif)
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
        # print "modelCyl_A.py estimation step: ", i
        res = estimateAng_cyl(estAng[i-1], fingerL, sL, offL, meas[i], bnds=b[:len(fingerL)*3],method=met)
        estAng[i] = res.x
        # if met == 0:
        #     res = estimateAng_cyl(estAng[i-1], fingerL, sL, offL, meas[i], bnds=None,method=0)
        #     estAng[i] = res.x
        # elif bnds:
        #     res = estimateAng_cyl(estAng[i-1], fingerL, sL, offL, meas[i], bnds=b[:len(fingerL)*3],method=met)
        #     estAng[i] = res.x
        # else:
        #     res = estimateAng_cyl(estAng[i-1], fingerL, sL, offL, meas[i],method=0)
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

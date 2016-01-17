import numpy as np
from scipy.optimize import *
from sympy import *
import time
import fcnCyPy as fcn


def cel(kc,p,c,s):
    ''' approximate a complete elliptical integral '''    
#    print "kc ", kc       
#    print "p ", p
#    print "c ", c
#    print "s ", s
       
    if kc == 0:
        c = None    # or nan???    
        return c
    
    # errtol = 1.0e-6;
    errtol = 1.0e-6
    k = abs(kc)
    pp = p
    cc = c
    ss = s
    em = 1.0
    
    if p > 0:
        pp = sqrt(p)
        ss = s/pp
    else:
        f = kc*kc
        q = 1.0-f
        g = 1.0-pp
        f = f-pp
        q = q*(ss-c*pp)
        pp = sqrt(f/g)
        cc = (c-ss)/g
        ss = q/((g*g)*pp)+cc*pp
    
    f = cc
    cc = cc+ss/pp
    g = k/pp
    ss = 2*(ss+f*g)
    pp = g+pp
    g = em
    em = k+em
    kk = k
    
#    print "before while\n", abs(g-k), g*errtol
    cnt = 0
    while (abs(g-k) > g*errtol):
       k = 2*sqrt(kk)
       kk = k*em
       f = cc
       cc = cc+ss/pp
       g = kk/pp
       ss = 2*(ss+f*g)
       pp = g+pp
       g = em
       em = k+em    
       
       cnt += 1
       
#       print "in while\n", g, k, g*errtol
       
#       if abs(g-k) > 10:
#           print "TOO BIG"
#           return 0
    
    c = (pi/2.0)*(ss+cc*em)/(em*(em+pp))
#    print "steps needed: ", cnt
    return c
    

def R_F(x,y,z):
    ''' Compute Carlson's elliptic integral of first kind '''
    print "in R_F"
    
    # some constants...
#    errtol = 0.0025
    errtol = 0.1
    C1 = 1.0/24.0
    C2 = 0.1
    C3 = 3.0/44.0
    C4 = 1.0/14.0
    
    # TODO checks on x,y,z are missing...
    
    xt = x
    yt = y
    zt = z    
    
    while True:
        sqrtx = sqrt(xt)
        sqrty = sqrt(yt)
        sqrtz = sqrt(zt)
        alamb = sqrtx*(sqrty+sqrtz)+sqrty*sqrtz
        xt = 0.25*(xt+alamb)
        yt = 0.25*(yt+alamb)
        zt = 0.25*(zt+alamb)
        ave = (xt+yt+zt)/3.
        delx = (ave-xt)/ave
        dely = (ave-yt)/ave
        delz = (ave-zt)/ave
        if max(max(abs(delx),abs(dely)),abs(delz)) > errtol:
            break
        
    e2 = delx*dely-delz*delz
    e3 = delx*dely*delz
    return (1.0+(C1*e2-C2-C3*e3)*e2+C4*e3)/sqrt(ave)
    
    
def R_C(x,y):
    ''' compute Carlson's elliptic integral of second kind '''
    print "in R_C"
    
#    errtol = 0.0012 
    errtol = 0.1
    C1 = 0.3
    C2 = 1.0/7.0
    C3 = 0.375
    C4 = 9.0/22.0
    
    # TODO checks on variables...    
    
    if y > 0.0:
        xt = x
        yt = y
        w = 1.0
    else:
        xt = x-y
        yt = -y
        w = sqrt(x)/sqrt(xt)
    
    while True:
        alamb = 2.0*sqrt(xt)*sqrt(yt)+yt
        xt = 0.25*(xt+alamb)
        yt = 0.25*(yt+alamb)
        ave = (xt+yt+yt)/3.
        s = (yt-ave)/ave
#        print ave
        if abs(s) > errtol:
            break

    return w*(1.0+s*s*(C1+s*(C2+s*(C3+s*C4))))/sqrt(ave);

    

def R_J(x,y,z,p):
    ''' compute Carlson's elliptic integral of third kind '''
    print "in R_J"
    
    # some constants...
#    errtol = 0.0015   
    errtol = 0.1
    C1=3.0/14.0 
    C2=1.0/3.0
    C3=3.0/22.0
    C4=3.0/26.0 
    C5=0.75*C3 
    C6=1.5*C4 
    C7=0.5*C2 
    C8=C3+C3
    
    # TODO checks on input variables are missing...   
    
    sum=0.0
    fac=1.0
    if p > 0.0: 
        xt = x
        yt = y
        zt = z
        pt = p
    else:
        xt = min(min(x,y),z)
        zt = max(max(x,y),z)
        yt = x+y+z-xt-zt
        a = 1.0/(yt-p)
        b = a*(zt-yt)*(yt-xt)
        pt = yt+b
        rho = xt*zt/yt
        tau = p*pt/yt
        rcx = R_C(rho,tau) 
        
    while True:
        sqrtx=sqrt(xt)
        sqrty=sqrt(yt)
        sqrtz=sqrt(zt)
        alamb=sqrtx*(sqrty+sqrtz)+sqrty*sqrtz
        alpha=(pt*(sqrtx+sqrty+sqrtz)+sqrtx*sqrty*sqrtz)**2
        beta=pt*((pt+alamb)**2)
        sum += fac*R_C(alpha,beta)
        fac=0.25*fac
        xt=0.25*(xt+alamb)
        yt=0.25*(yt+alamb)
        zt=0.25*(zt+alamb)
        pt=0.25*(pt+alamb)
        ave=0.2*(xt+yt+zt+pt+pt)
        delx=(ave-xt)/ave
        dely=(ave-yt)/ave
        delz=(ave-zt)/ave
        delp=(ave-pt)/ave                
        if max(max(abs(delx),abs(dely)),max(abs(delz),abs(delp))) > errtol:
            break

    ea=delx*(dely+delz)+dely*delz
    eb=delx*dely*delz
    ec=delp*delp
    ed=ea-3.0*ec
    ee=eb+2.0*delp*(ea-ec)
    ans=3.0*sum+fac*(1.0+ed*(-C1+C5*ed-C6*ee)+eb*(C7+delp*(-C8+delp*C4))
    		+delp*ea*(C2-delp*C3)-C2*delp*ec)/(ave*sqrt(ave))

    if p <= 0.0: 
        ans=a*(b*ans+3.0*(rcx-R_F(xt,yt,zt)))
    
    return ans
    
    
def cel_car(kc,p,c,s):
    ''' approximate a complete elliptical integral with Carlson's functions '''    
    print "cel_car"
    
    res = c*R_F(0.,kc**2,1.)+((s-p*c)*R_J(0.,kc**2,1.,p))/3.
    
    return res


def cel_bul(kc,p,c,s):
    ''' approximate a complete elliptical integral with Bulirsch algorithm '''    
       
    if kc == 0:
        c = None    # or nan???    
    
    # errtol = 1.0e-6;
    errtol = 1.0e-6
    k = abs(kc)
    em = 1.0
    
    if p > 0:
        p = sqrt(p)
        s /= p
    else:
        f = kc**2
        q = (1-f)*(s-c*p)
        g = 1-p
        f -= p
        p = sqrt(f/g)
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
       k = 2*sqrt(kk)
       kk = k*em
       f = c
       c += (s/p)
       s = 2*(s+f*kk/p)
       p = kk/p+p
       g = em
       em = k+em    
       
       cnt += 1
           
    c = (pi/2)*(s+c*em)/(em*(em+p))
#    print "steps needed: ", cnt
    return c    


def calcB_cyl(pos, ang):
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
             

    rotMatPos = np.array([[cos(ang), -sin(ang)],
                          [sin(ang), cos(ang)]])
    cylCo = np.dot(pos,rotMatPos)    # rotated cylindrical coordinates             
        
    z = cylCo[0]
    rho = cylCo[1]
    
    a = 0.0025     # radius [m]
    b = 0.015/2    # half length of magnet [m]
    # magic value...
    Bo = 1.0e+3*4.0107      # magnetic constant
    
    # component calculations
    z_pos = z+b
    z_neg = z-b
    
    alpha_pos = a/sqrt(z_pos**2+(rho+a)**2)
    alpha_neg = a/sqrt(z_neg**2+(rho+a)**2)
    
    beta_pos = z_pos/sqrt(z_pos**2+(rho+a)**2)
    beta_neg = z_neg/sqrt(z_neg**2+(rho+a)**2)
    
    gamma = (a-rho)/(a+rho)
    
    k_pos = sqrt((z_pos**2+(a-rho)**2)/(z_pos**2+(a+rho)**2))
    k_neg = sqrt((z_neg**2+(a-rho)**2)/(z_neg**2+(a+rho)**2))

    # cel calculation with Bulirsch's algorithm    
    B_rho = Bo*(alpha_pos*cel_bul(k_pos,1.,1.,-1.)-alpha_neg*cel_bul(k_neg,1.,1.,-1.))
    B_z   = (Bo*a)/(a+rho)*(beta_pos*cel_bul(k_pos,gamma**2,1.,gamma)-beta_neg*cel_bul(k_neg,gamma**2,1.,gamma))
        

    B = np.dot(np.array([B_z, B_rho]),(rotMatPos))  
    
#    return (B, cylCo)
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
    theta_k = 0.0
    theta = [angles[0], angles[1], angles[1]*(2./3.)]
    pos = np.array([(1*(finger_0*np.sin(np.pi/2.) + finger[0]*np.sin(np.pi/2-theta[0]) +              # x
                finger[1]*np.sin(np.pi/2.-theta[0]-theta[1]) +
                finger[2]*np.sin(np.pi/2.-theta[0]-theta[1]-theta[2]))),

                (-1*(finger[0]*np.cos(np.pi/2.-theta[0]) +               # z (*-1 because you move in neg. z-direction)
                finger[1]*np.cos(np.pi/2.-theta[0]-theta[1]) +
                finger[2]*np.cos(np.pi/2.-theta[0]-theta[1]-theta[2]))*np.cos(theta_k))])
                
    return pos                
    



def angToB_cyl(angles, fingerL, sPos, jointPos):
    ''' calculate the B-field for given finger angels. CYLINDRICAL MODEL!!!
    
    Parameters
    ----------    
    angles : 2darray 
        angle of the joints [angle_MCP, angle_PIP]
    fingerL : 3darray
        length of the finger phalanges [length_proximal, length_intermediate, length_distal]
    sPos : 2darray
        the sensor position, relative to the joint ([x_lateral, x_radial])
    jointPos : 2darray
        position of the finger joint, relative to the index joint ([x_lateral, x_radial])
        
    Returns
    -------
    B : 2darray
        the calculated B-field at the sensor [B_z, B_rho]
        
        
    '''
    
    p = angToP_cyl(angles,fingerL)+jointPos-sPos
#    p += [1.,-1.]
#    p = pFinger+jointPos-sPos        
    ang = sum(angles)+(2./3.*angles[1])
    
    B = calcB_cyl(p,ang)
    B[1] *= 1      # really?
    B = B.astype('float')
    return (B, p, ang)
    

''' estimation of joint angles '''
# TODO verify!!!

#def minimizeAng_cyl(ang, fingerL, sPos, jointPos, measB):
#    ''' objective function to minimize... '''
#    
#    dif = measB - angToB_cyl(ang, fingerL, sPos, jointPos)
#    dif = dif.astype('float')    
#    res = np.linal.norm(dif)
#    
#    return res
#    
#    
#def estimateAng_cyl(ang_0, fingerL, sPos, jointPos, measB):
#    ''' estimating the joint angles
#    
#    Parameters
#    ----------
#    ang_0 : 2darray
#        initial guess of angles [angle_MCP, angle_PIP]
#    fingerL : 3darray
#        length of the finger phalanges [length_proximal, length_intermediate, length_distal]
#    sPos : 2darray
#        the sensor position, relative to the joint ([x_lateral, x_radial])
#    jointPos : 2darray
#        position of the finger joint, relative to the index joint ([x_lateral, x_radial])
#        the measured B-field ([B_z, B_rho])
#        
#    Returns
#    -------
#    res : OptimizeResult
#    
#    '''
#    
#    res = minimize(minimizeAng_cyl,ang_0,args=(fingerL, sPos, jointPos, measB),method='bfgs', tol=1.e-05)
#    
#    return res
    


''' estimation of position, given angle '''

def minimizeB_cyl(pos, ang, measB):
    ''' objective function to minimize... '''
    
    dif = measB - calcB_cyl(pos,ang)
    dif = dif.astype('float')       # I have to do it, otherwise a numpy.linalg.norm can not be applied...
    res = np.linalg.norm(dif)
    
    return res
    
def estimatePos_cyl(pos_0, ang, measB):
    ''' estimating the position
    
    Parameters
    ----------
    pos_0 : 2darray
        initial guess of position (in cyl. coordinates)
    ang : float
        angle of the magnet in radians
    measB : 2darray
        the measured B-field ([B_z, B_rho])
        
    Returns
    -------
    res : OptimizeResult
    
    '''
    
##     res = fmin_l_bfgs_b(minimizeB_cyl,pos_0,args=(ang,measB),approx_grad=1)
#    res = minimize(minimizeB_cyl,pos_0,args=(ang,measB),method='slsqp')
    res = minimize(minimizeB_cyl,pos_0,args=(ang, measB),method='bfgs', tol=1.e-05)
    
    return res
    

#def estimateAng_cyl(measB, angles_0, fingerL, sPos, jointPos):
    
    
    

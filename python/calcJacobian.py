from sympy import *
import numpy as np


def myFunc(x,y,z):   
#                     3*    R                                                    /                |H|**5                                     H      /   |R|**3                  
    return np.array([ 3*(-x + 1.0)*(-(-y + 2.0)*(z - 3.0) + (y - 2.0)*(-z + 3.0))/((-x + 1.0)**2 + (-y + 2.0)**2 + (-z + 3.0)**2)**(5/2.) - (x - 1.0)/((-x + 1.0)**2 + (-y + 2.0)**2 + (-z + 3.0)**2)**(3/2.),
                      3*(-y + 2.0)*( (-x + 1.0)*(z - 3.0) - (x - 1.0)*(-z + 3.0))/((-x + 1.0)**2 + (-y + 2.0)**2 + (-z + 3.0)**2)**(5/2.) - (y - 2.0)/((-x + 1.0)**2 + (-y + 2.0)**2 + (-z + 3.0)**2)**(3/2.),
                      3*(-z + 3.0)*(-(-x + 1.0)*(y - 2.0) + (x - 1.0)*(-y + 2.0))/((-x + 1.0)**2 + (-y + 2.0)**2 + (-z + 3.0)**2)**(5/2.) - (z - 3.0)/((-x + 1.0)**2 + (-y + 2.0)**2 + (-z + 3.0)**2)**(3/2.)])
def calcJacobi():
    x,y,z = symbols('x y z')
    s0,s1,s2 = symbols('s0 s1 s2')
    
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
    
    j = Matrix([[fun[0][0].diff(x), fun[0][0].diff(y), fun[0][0].diff(z)],
                [fun[0][1].diff(x), fun[0][1].diff(y), fun[0][1].diff(z)],
                [fun[0][2].diff(x), fun[0][2].diff(y), fun[0][2].diff(z)]])
    
    return j
#a=1
#b=1
#c=1

#print "sympy function: ", myFunc(a,b,c)                                      
#print "numpy function: ", modE.evalfuncMagOne([a,b,c],s0)
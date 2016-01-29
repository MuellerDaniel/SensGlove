import numpy as np
#import matplotlib.dates as mdates
import matplotlib.pyplot as plt
#from sympy import *
#from sympy.interactive import printing
#from sympy.mpmath import *



def jacoMatlab(rx,ry,rz):
    ''' First derivative of dip function for H = [1,0,0]
        imported from Matlab... '''
    J = np.array([
        [(18303781807138305.*rx)/(2305843009213693952.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) + (18303781807138305.*abs(rx)*np.sign(rx))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx**2*abs(rx)*np.sign(rx))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)), 
         (18303781807138305.*abs(ry)*np.sign(ry))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx**2*abs(ry)*np.sign(ry))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)), 
         (18303781807138305.*abs(rz)*np.sign(rz))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx**2*abs(rz)*np.sign(rz))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2))],
        
        [ (18303781807138305.*ry)/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx*ry*abs(rx)*np.sign(rx))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)),
         (18303781807138305.*rx)/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx*ry*abs(ry)*np.sign(ry))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)),
        -(91518909035691525.*rx*ry*abs(rz)*np.sign(rz))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2))],

        [(18303781807138305.*rz)/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx*rz*abs(rx)*np.sign(rx))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)),
         -(91518909035691525.*rx*rz*abs(ry)*np.sign(ry))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)),
         (18303781807138305.*rx)/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx*rz*abs(rz)*np.sign(rz))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2))]])
    
    return J


#rx = Symbol('rx')
#ry = Symbol('ry')
#rz = Symbol('rz')
#
#R = Matrix([rx, ry, rz])
#H = Matrix([1., 0., 0.])
#Br = 12.6e+03
#mu_0 = 4*np.pi*1e-07
#mu_r = 1.05
#addFact = 1
#l = (Br*mu_0*mu_r)/(4*pi)*addFact;
#
#model = Function('model')
#
#model = l*(3*H.dot(R)*R)/(R.norm()**5) - H/(R.norm()**3)
#
#jaco = model.jacobian(R)
#
#res = jaco.subs({rx:0.04, ry:0.0, rz:0.0}).evalf()

a = jacoMatlab(0.04, 0., 0.)

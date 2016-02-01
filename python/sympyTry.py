from sympy import *
import numpy as np

''' Trying to formulate and differentiate the (calcB_dip) model with sympy

    Formulation and evaluation works!
    But differentiation leads strange results (a 'Subs(Derivative(...))' term resolves)
    and so the Jacobian is not evaluable

    However here the summing up of functions would work '''

rx, ry, rz = symbols('rx ry rz')
R = Matrix([[rx],[ry],[rz]])
H = Matrix([[1.],[0.],[0.]])

f = Matrix([3*R*H.dot(R)/(R.norm()**5) - H/R.norm()**3])

f_J = f.jacobian(R)
print "Jacobian:\n", f_J

res = f_J.subs([(rx,0.04),(ry,0.0),(rz,0.0)])
print "\n\nresult of evaluated jacobian:\n", res

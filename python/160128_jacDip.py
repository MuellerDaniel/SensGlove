import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from sympy import *
from sympy.interactive import printing
from sympy.mpmath import *


rx, ry, rz, hx, hy, hz = symbols('rx ry rz hx hy hz')
#init_session()
R = Matrix([[rx],[ry],[rz]])
H = Matrix([[hx], [hy], [hz]])

#M = (3*H.dot(R)*R)/(R.norm()**5) - H/(R.norm()**3)
#J = M.jacobian([R,H])
##J = M.jacobian([rx,ry,rz,hx,hy,hz])
#Me = M.subs([(rx,0.04), (ry,9), (rz,0.9),
#            (hx,0.7), (hy,0.), (hz,0.3)])
#print "Me\n", Me            
#
#Je = J.subs([(rx,0.04), (ry,9), (rz,0.9),
#            (hx,0.7), (hy,0.), (hz,0.3)])            
#print "Je\n", Je            

M = Function('M')(Matrix([[R],[H]]))
M = (3*H.dot(R)*R)/(R.norm()**5) - H/(R.norm()**3)

J = Function('J')(Matrix([[R],[H]]))
J = M.jacobian([R,H])
#J = M.jacobian([rx,ry,rz,hx,hy,hz])
Me = M.subs([(rx,0.04), (ry,9), (rz,0.9),
            (hx,0.7), (hy,0.), (hz,0.3)])
print "Me\n", Me            

Je = J.subs([(rx,0.04), (ry,9), (rz,0.9),
            (hx,0.7), (hy,0.), (hz,0.3)])            
print "Je\n", Je            
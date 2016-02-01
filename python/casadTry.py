from casadi import *
import numpy as np
import modelDip as modD

''' Trying to formulate and differentiate the (calcB_dip) model with casadi

    Formulation and differentiation works! The results are good

    But it is not possible to sum up the symbolic functions (like in Matlab)!

    It would be possible to do it in a cumbersome 'hard-code' way,
    by explicitly coding the 'r' and 'h' vector for each element
    (one can not describe a SXFunction with another SXFunction, like in Matlab done in 'angToB_sym.m')'''

R = SX.sym('R',3)
H = np.array([1.,0.,0.])

Br = 12.6e+03
mu_0 = 4*np.pi*1e-07
mu_r = 1.05
addFact = 1
lamb = (Br*mu_0*mu_r)/(4*np.pi)*addFact
factor = np.array([lamb, -lamb, lamb])

f = SXFunction([R], [factor*(((3*R*inner_prod(H,R))/(np.linalg.norm(R)**5)) -
                            (H/(np.linalg.norm(R)**3)))])
f.init()

r_test = DMatrix([0.04,0.,0.])
rOld = np.array([0.04,0.,0.])

f.setInput(r_test,0)
f.evaluate()
print "result casadi: ", f.getOutput(0)

print "result model: ", modD.calcB(rOld,H)


f_J = f.jacobian()
# f_J *= 2
f_J.init()

f_J.setInput(r_test,0)
f_J.evaluate()
print "result f_J: ", f_J.getOutput(0)

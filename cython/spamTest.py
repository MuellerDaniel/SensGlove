# this file represents my "main" python file, which is already existing
# ...but it is also possible to write everything in the .pyx file and compile it...


import fcnCyPy as fcn
import numpy as np

# P-vector
P = np.array([ 0.02957,  0.17138,  0.01087,  0.0092 ,  0.17967,  0.01087,
       -0.01117,  0.17117,  0.01087, -0.03154,  0.16353,  0.01087])
# S-vector
#S = [[0.02957, 0.06755, 0.0], [0.0092, 0.06755, 0.0], [-0.01117, 0.06755, 0.0], [-0.03154, 0.06755, 0.0]]
S = [0.02957, 0.06755, 0.0, 0.0092, 0.06755, 0.0, -0.01117, 0.06755, 0.0, -0.03154, 0.06755, 0.0]
# B-vector
B = np.array([166.87740309, -607.25412378,  -68.23099416,   70.76782614,
       -667.74956884,  -75.29786286,  -42.62948379, -678.25048025,
        -76.81066919, -150.20758011, -632.56596244,  -71.92946178])



#a = spamTest.fcn.funcMagY_py(spamTest.P,spamTest.S,spamTest.B)
b = fcn.funcMagY_cy(P,S,B)      # you have to pass S as a column list...
#b = spamTest.fcn.funcMagY_cy(spamTest.P,spamTest.S,spamTest.B)


'''
import standalonecypy as fcn

a = fcn.primesCy(50)
b = fcn.primesPy(50)
'''

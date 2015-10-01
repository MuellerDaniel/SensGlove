#import pyximport; pyximport.install()
import numpy as np
import time
from scipy.optimize import *
# you have to include the 'math.h' library for sqrt() and pow()!!!
from libc.math cimport pow
from libc.math cimport sqrt
from libc.stdlib cimport malloc


'''
      cython version
'''

cdef float cal_norm_cy(float *val, len):
# for calculating the norm of an array
# return a C float
    cdef float sum = 0
    cdef float result = 0
    cdef int i = 0
    for i in range(len):
        sum += pow(val[i],2)
    result = sqrt(sum)
    return result

def cal_norm_py(val):
# for calculating the norm of an array
# returning a python object
    cdef int i = 0
    cdef float sum = 0
    #cdef float result = 0
    for i in range(len(val)):
        sum += pow(val[i],2)
    result = sqrt(sum)
    return result


cdef float dot_product(float *a, float *b, int len):
# function to calculate the dot product of two arrays
    cdef float sum = 0
    cdef int i = 0
    for i in range(len):
        sum += a[i]*b[i]
    return sum

cdef float * sub(float *a, float *b, int len):
# function to subtract two arrays elementwise
    cdef float *res
    res = <float*>malloc(len*sizeof(float))

    cdef int i = 0
    for i in range(len):
        res[i] = a[i]-b[i]
    return res

cdef sub_py(float *a, b, int len):
# function to subtract two arrays elementwise
    res = [0] * len
    #res = <float*>malloc(len*sizeof(float))
    cdef int i = 0
    for i in range(len):
        res[i] = a[i]-b[i]
    return res

cdef add_py(a, float *b, int len):
# function to subtract two arrays elementwise
    res = [0] * len
    #res = <float*>malloc(len*sizeof(float))
    cdef int i = 0
    for i in range(len):
        res[i] = a[i]+b[i]
    return res


cdef float * evalfuncMagDot_cy(float *P, float *S, int lenP, int lenS):
# TODO convert to work with plain C-variables
    cdef float *result
    result = <float*>malloc(3*sizeof(float))
    cdef float *H
    H = <float*>malloc(3*sizeof(float))
    cdef float *R
    R = <float*>malloc(3*sizeof(float))

    H = sub(P,S,lenP)
    R = sub(S,P,lenP)
    cdef int i = 0
    for i in range(3):
      result[0] = ((3*(dot_product(H,R,lenP)*R[0])/pow(cal_norm_cy(R,3),5)) -
                    (H[0]/pow(cal_norm_cy(R,3),3))) * -1
      result[1] = ((3*(dot_product(H,R,lenP)*R[1])/pow(cal_norm_cy(R,3),5)) -
                    (H[1]/pow(cal_norm_cy(R,3),3))) * -1
      result[2] = ((3*(dot_product(H,R,lenP)*R[2])/pow(cal_norm_cy(R,3),5)) -
                    (H[2]/pow(cal_norm_cy(R,3),3))) * -1

    return result
'''
    H = sub(P,S,len(P))        # this worked for the example on the flat paper...
    R = sub(S,P,len(P))
    cdef float result[3]
    # calculate the result-values one by one...
    cdef int i = 0
    for i in range(3):
    #    print "Nr: ",i,"H ", H[i], " R ",R[i]
        result[0] = ((3*(dot_product(H,R)*R[0])/pow(cal_normCy(R,3),5)) -
                      (H[0]/pow(cal_normCy(R,3),3))) * -1
        result[1] = ((3*(dot_product(H,R)*R[1])/pow(cal_normCy(R,3),5)) -
                      (H[1]/pow(cal_normCy(R,3),3))) * -1
        result[2] = ((3*(dot_product(H,R)*R[2])/pow(cal_normCy(R,3),5)) -
                      (H[2]/pow(cal_normCy(R,3),3))) * -1
    print "result: ", result[0], " ", result[1], " ", result[2]
'''



def funcMagY_cy(P,S,B):
    start = time.time()
    #print "P\n", P
    #print "S\n", S
    #print "B\n", B
    cdef int lenP, lenS, lenB
    cdef int i, j, k
    # generate an int for the length, because it's safer to pass this variable
    # than handling sizes of arrays and types...
    lenP = len(P)
    lenS = len(S)
    lenB = len(B)
    # declaring the arrays...
    cdef float *pArr
    pArr = <float*> malloc(lenP*sizeof(float))
    i = 0
    for i in range(lenP):
        pArr[i] = P[i]
    cdef float *sArr = <float*>malloc(lenS*sizeof(float))
    i = 0
    for i in range(lenS):
        sArr[i] = S[i]
    cdef float *bArr = <float*>malloc(lenB*sizeof(float))
    i = 0
    for i in range(lenB):
        bArr[i] = B[i]

    cdef float *sAct    # the actual S-Array
    sAct = <float*> malloc(3*sizeof(float))
    cdef float *pAct    # the actual P-Array
    pAct = <float*> malloc(3*sizeof(float))

    #bArr = evalfuncMagDot_cy(pArr, sArr, lenP, lenS)
    #the calculations...
    val = [0] * lenB
    i = 0
    for i in range(lenS/3):
        b = [0] * 3
        k = 0
        for k in range(3):    # assign the actual s-Array
            sAct[k] = sArr[k+i*3]
        j = 0
        for j in range(lenP/3):
            k = 0
            for k in range(3):    # assign the actual p-Array
                pAct[k] = pArr[k+j*3]
            b = add_py(b,evalfuncMagDot_cy(pAct,sAct,3,3),3)
        val[i*3:i*3+3] = b
    #print "val: ", val
    res = cal_norm_py(sub_py(bArr,val,lenB))
    #print "res: ", res
    print "time needed: ", time.time()-start
    return res


def estimatePos(P,S,B,cnt,bnds=None,jacobian=None):
    """returns the estimated position

    Parameters
    ----------
    P : array
        the initial guess of the position
    S : array
        the position of the sensor
    B : array
        the magnetic field
    bnds : tuple
            the lower and upper bounds for the position coordinates
            ((lbx,ubx),(lby,uby),(lbz,ubz))

    Returns
    -------
    res.x : array
        the result of the minimize function, i.e. the estimated position

    """
#    c=0.1
#    cons = ({'type':'ineq',
#             'fun':lambda x: c/10 - abs(P[0]-x[0])},
#            {'type':'ineq',
#             'fun':lambda x: c - abs(P[1]-x[1])},
#            {'type':'ineq',
#             'fun':lambda x: c - abs(P[2]-x[2])},
#            {'type':'ineq',
#             'fun':lambda x: c/10 - abs(P[3]-x[3])},
#            {'type':'ineq',
#             'fun':lambda x: c - abs(P[4]-x[4])},
#            {'type':'ineq',
#             'fun':lambda x: c - abs(P[5]-x[5])},)
#    cons = ({'type':'ineq',
#             'fun':lambda x: c - abs(P-x)},)
    opt = ({'maxiter':30,
            'disp':True})
    '''   advanced approach (pseudo-inverse thing)  '''
#    val = minimize(funcMagYmulti, P, args=(S,B), method='slsqp',
#                   tol=1e-5, bounds=bnds, jac=jacobian)
    '''    straight forward approach norm(B(estPos)-B(measured))    '''
    #val = minimize(funcMagY, P, args=(S,B), method='slsqp',
    #               tol=1e-4, bounds=bnds, jac=jacobian, options=opt)

    val = minimize(funcMagY_cy, P, args=(S,B), method='slsqp',
                    bounds=bnds, jac=jacobian, options=opt)
#    print "evaluation ",cnt
#    print funcMagYmulti(val.x,S,B)
#    val = _minimize_slsqp(funcMagY, P, args=(S,B), method='slsqp',
#                   tol=1e-5, bounds=bnds, jac=jacobian)
#    val.x is a 1d-vector, so reshape it!
#    res = np.reshape(val.x,(len(P)/3,1,3))     # improve it!
#    res = np.reshape(val.x,(1,1,3))
    if val.success:
#        print "jacobian\n", val.jac
        #print "python, val.x\n", val.x
        return val        # as result you will get the P vector!
    else:
        print "No solution found! Iteration Nr ",cnt
        print "Error message ",val.message
#        print res.message
#        return np.zeros(shape=(2,1,3))
        return val


'''
###############################################################################
    python version
###############################################################################
'''

def evalfuncMagDot_py(P,S):
    """returns the magnetic field

    Parameters
    ----------
    P : array
        the position
    S : array
        the position of the sensor
    """
    H = 1*(P-S)        # this worked for the example on the flat paper...
    R = 1*(S-P)
#    H = -R+(P-S)
    factor = np.array([-1, -1, -1])
#    return [((3*(np.cross(H,R)*R)/(np.linalg.norm(R)**5)) -
#                                        (H/(np.linalg.norm(R)**3)))] * factor
    no = np.sqrt(R[0]**2+R[1]**2+R[2]**2)
    return [((3*(np.dot(H,R)*R)/(no**5)) - (H/(no**3)))] * factor

def funcMagY_py(P,S,B):
    start = time.time()
    #print "P ", type(P)
    #print "S ", type(S)
    #print "B ", type(B)

    val = np.zeros(shape=(B.shape))
    for i in range(len(S)):
    #        print "P.shape ",val
        b = 0.
        for j in range(len(P)/3):
            b += evalfuncMagDot_py(P[j*3:j*3+3],S[i])
        val[i*3:i*3+3] = b
    res = np.linalg.norm(B - val)
    print "time needed: ", time.time()-start
    return res

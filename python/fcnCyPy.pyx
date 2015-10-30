#import pyximport; pyximport.install()
import numpy as np
import time
from scipy.optimize import *
# you have to include the 'math.h' library for sqrt() and pow()!!!
from libc.math cimport pow, sqrt, cos, sin
from libc.stdlib cimport malloc,free


'''
###############################################################################
    cython version
###############################################################################
'''

cdef long double cal_norm_cy(long double *val, len):
# for calculating the norm of an array
# return a C long double
    cdef long double sum = 0
    cdef long double result = 0
    cdef int i = 0
    for i in range(len):
        sum += pow(val[i],2)
    result = sqrt(sum)
    #free(val)
    return result

def cal_norm_py(val):
# for calculating the norm of an array
# returning a python object
    cdef int i = 0
    cdef long double sum = 0
    #cdef long double result = 0
    for i in range(len(val)):
        sum += pow(val[i],2)
    result = sqrt(sum)
    return result


cdef long double dot_product(long double *a, long double *b, int len):
# function to calculate the dot product of two arrays
    cdef long double sum = 0
    cdef int i = 0
    for i in range(len):
        sum += a[i]*b[i]
    #free(a)
    #free(b)
    return sum

cdef long double * sub(long double *a, long double *b, int len):
# function to subtract two arrays elementwise
    cdef long double *res
    res = <long double*>malloc(len*sizeof(long double))

    cdef int i = 0
    for i in range(len):
        res[i] = a[i]-b[i]
    #free(a)
    #free(b)
    return res

cdef sub_py(long double *a, b, int len):
# function to subtract two arrays elementwise
    res = [0] * len
    #res = <long double*>malloc(len*sizeof(long double))
    cdef int i = 0
    for i in range(len):
        res[i] = a[i]-b[i]
    #free(a)
    return res

cdef add_py(a, long double *b, int len):
# function to subtract two arrays elementwise
    res = [0] * len
    #res = <long double*>malloc(len*sizeof(long double))
    cdef int i = 0
    for i in range(len):
        res[i] = a[i]+b[i]
    #free(b)
    return res


cdef long double * evalfuncMagDot_cy(long double *P, long double *S, int lenP, int lenS):
#cdef long double * evalfuncMagDot_cy(P, long double *S, int lenP, int lenS):
    cdef long double *result
    result = <long double*>malloc(3*sizeof(long double))
    cdef long double *H
    H = <long double*>malloc(3*sizeof(long double))
    cdef long double *R
    R = <long double*>malloc(3*sizeof(long double))

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
    free(H)
    free(R)
    return result
'''
    H = sub(P,S,len(P))        # this worked for the example on the flat paper...
    R = sub(S,P,len(P))
    cdef long double result[3]
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
    cdef int lenP, lenS, lenB
    cdef int i, j, k
    # generate an int for the length, because it's safer to pass this variable
    # than handling sizes of arrays and types...
    lenP = len(P)
    lenS = len(S)
    lenB = len(B)
    # declaring the arrays...
    cdef long double *pArr
    pArr = <long double*> malloc(lenP*sizeof(long double))
    i = 0
    for i in range(lenP):
        pArr[i] = P[i]
    cdef long double *sArr = <long double*>malloc(lenS*sizeof(long double))
    i = 0
    for i in range(lenS):
        sArr[i] = S[i]
    cdef long double *bArr = <long double*>malloc(lenB*sizeof(long double))
    i = 0
    for i in range(lenB):
        bArr[i] = B[i]

    cdef long double *sAct    # the actual S-Array
    sAct = <long double*> malloc(3*sizeof(long double))
    cdef long double *pAct    # the actual P-Array
    pAct = <long double*> malloc(3*sizeof(long double))

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
            #b = add_py(b,evalfuncMagDot_cy(P[j*3:j*3+3],sAct,3,3),3)
        val[i*3:i*3+3] = b
    res = cal_norm_py(sub_py(bArr,val,lenB))
    free(pAct)
    free(sAct)
    free(pArr)
    free(sArr)
    free(bArr)
    #print "cython called!"
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
    opt = ({'maxiter':50})
    '''   advanced approach (pseudo-inverse thing)  '''
#    val = minimize(funcMagYmulti, P, args=(S,B), method='slsqp',
#                   tol=1e-5, bounds=bnds, jac=jacobian)
    '''    straight forward approach norm(B(estPos)-B(measured))    '''
    #val = minimize(funcMagY, P, args=(S,B), method='slsqp',
    #               tol=1e-4, bounds=bnds, jac=jacobian, options=opt)

    val = minimize(funcMagY_cy, P, args=(S,B), method='slsqp',
                    bounds=bnds, jac=jacobian,options=opt)
    if val.success:
        return val        # as result you will get the P vector!
    else:
        print "No solution found! Iteration Nr ",cnt
        #print "Error message ",val.message
        print val.message
#        return np.zeros(shape=(2,1,3))
        return val


#'''
#  angle estimation
#'''

def xPos_py(angle,phal,off):
    return (phal[0]*np.cos(angle[0])+
            phal[1]*np.cos((angle[0])+(angle[1]))+
            phal[2]*np.cos((angle[0])+(angle[1])+(angle[2]))+off)

def yPos_py(angle,phal,off):
    return off

def zPos_py(angle,phal,off):
    return (phal[0]*np.sin((angle[0]))+
            phal[1]*np.sin((angle[0])+(angle[1]))+
            phal[2]*np.sin((angle[0])+(angle[1])+(angle[2])))*-1+off

def calcPosition_py(angle,phal,offSet):
    cdef int i = 0
    cdef int iEnd = 4
    res = np.zeros((12,))
    for i in range(iEnd):
        res[i*3:i*3+3] = np.array([xPos_py(angle[i*3:i*3+3],phal[i*3:i*3+3],offSet[i*3]),
                            yPos_py(angle[i*3:i*3+3],phal[i*3:i*3+3],offSet[i*3+1]),
                            zPos_py(angle[i*3:i*3+3],phal[i*3:i*3+3],offSet[i*3+2])])
    return res

def posFun_cy(angle,pos,phal,off):
    estimated = calcPosition_py(angle,phal,off)
    diff = estimated - pos
    res = np.linalg.norm(diff)    # it should work this way... though function returns a long...

    return res


def estimateAngle_mCy(pos,guess,off,phal,bnds):
  res = minimize(posFun_cy,guess,args=(pos,phal,off),method='slsqp',
                 bounds=bnds,tol=1e-12)
#    fcn.test(pos)
#    res = 0
  return res

#'''
#  describing the whole estimation as angle-estimation
#'''
cdef long double xPos_cy(long double *angle,long double *phal,long double off):
    return (phal[0]*np.cos(angle[0])+
            phal[1]*np.cos((angle[0])+(angle[1]))+
            phal[2]*np.cos((angle[0])+(angle[1])+(angle[2]))+off)

cdef long double yPos_cy(long double *angle,long double *phal,long double off):
    return off

cdef long double zPos_cy(long double *angle,long double *phal,long double off):
    return (phal[0]*np.sin((angle[0]))+
            phal[1]*np.sin((angle[0])+(angle[1]))+
            phal[2]*np.sin((angle[0])+(angle[1])+(angle[2])))*-1+off

cdef long double * angToB_cy(long double *theta,long double *finger,long double *off,long double *S):
    """returns the magnetic field

    Parameters
    ----------
    theta : array
            the angles of the finger
    finger : array
            the length of the phalanges
    off : array
        the absolute position of the MCP
    S : array
        the position of the sensor
    """
    cdef long double *P
    P = <long double*> malloc(3*sizeof(long double))
    P[0] = xPos_cy(theta,finger,off[0])
    P[1] = yPos_cy(theta,finger,off[1])
    P[2] = zPos_cy(theta,finger,off[2])

    cdef long double *R = sub(S,P,3)

    cdef long double *H
    H = <long double*> malloc(3*sizeof(long double))
    H[0] = np.sin(-np.pi/2+abs(-theta[0]-theta[1]-theta[2]))
    H[1] = 0
    H[2] = np.cos(-np.pi/2+abs(-theta[0]-theta[1]-theta[2]))
    #cdef long double normR = cal_norm_cy(R,3)

    cdef long double *res
    res = <long double*> malloc(3*sizeof(long double))
    res[0] = ((3*(dot_product(H,R,3)*R[0])/pow(cal_norm_cy(R,3),5)) -
                  (H[0]/pow(cal_norm_cy(R,3),3)))
    res[1] = ((3*(dot_product(H,R,3)*R[1])/pow(cal_norm_cy(R,3),5)) -
                  (H[1]/pow(cal_norm_cy(R,3),3)))
    res[2] = ((3*(dot_product(H,R,3)*R[2])/pow(cal_norm_cy(R,3),5)) -
                  (H[2]/pow(cal_norm_cy(R,3),3)))

    #no = np.sqrt(R[0]**2+R[1]**2+R[2]**2)
    #print "P[0]_cy ", P[0]
    free(H)
    free(P)
    free(R)
    #print "res[0]_cy ", res[0]
    return res

def funcMagY_angle_cy(theta,finger,off,S,B):
    # converting the input arrays to c arrays
    cdef int lenB = len(B)
    cdef int lenTheta = len(theta)
    cdef int lenFinger = len(finger)
    cdef int lenOff = len(off)
    cdef int lenS = len(S)
    cdef int i = 0
    cdef int k = 0
    cdef int l = 0

    # value arrays...
    cdef long double *arrCal
    arrCal = <long double*> malloc(lenB*sizeof(long double))

    cdef long double *tmp
    tmp = <long double*> malloc(3*sizeof(long double))

    cdef long double *actS
    actS = <long double*> malloc(3*sizeof(long double))
    cdef long double *actTheta
    actTheta = <long double*> malloc(3*sizeof(long double))
    cdef long double *actFinger
    actFinger = <long double*> malloc(3*sizeof(long double))
    cdef long double *actOff
    actOff = <long double*> malloc(3*sizeof(long double))

    cal = [0] * lenB

    cdef int iEnd = 4
    cdef int jEnd = 4

    cdef int j = 0
    i = 0
    for i in range(iEnd):
        b = [0]*3
        k = 0
        for k in range(3):
            actS[k] = S[k+i*3]
        for j in range(jEnd):
            l = 0
            for l in range(3):
                actTheta[l] = theta[l+j*3]
                actFinger[l] = finger[l+j*3]
                actOff[l] = off[l+j*3]
            b = add_py(b,angToB_cy(actTheta,actFinger,actOff,actS),3)
        cal[i*3:i*3+3] = b

    #cdef long double res_cy = cal_norm_cy(sub(arrB,arrCal,lenB),lenB)
    #print "cython cal: ", cal

    res_py = cal_norm_py(B-cal)
    res_py = res_py**2
    #res_py = res_cy     # don't know if it works....
    free(arrCal)
    free(tmp)
    free(actS)
    free(actTheta)
    free(actFinger)
    free(actOff)

    return res_py     #take the square of it!



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

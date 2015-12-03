# import pyximport; pyximport.install()
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

cdef double cal_norm_cy(double *val, len):
# for calculating the norm of an array
# return a C double
    cdef double sum = 0
    cdef double result = 0
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
    cdef double sum = 0
    cdef int length = len(val)
    #cdef double result = 0
    for i in range(length):
        sum += pow(val[i],2)
    result = sqrt(sum)
    return result


cdef double dot_product(double *a, double *b, int len):
# function to calculate the dot product of two arrays
    cdef double sum = 0
    cdef int i = 0
    for i in range(len):
        sum += a[i]*b[i]
    #free(a)
    #free(b)
    return sum

cdef double * sub(double *a, double *b, int len):
# function to subtract two c-arrays elementwise
    cdef double *res
    res = <double*>malloc(len*sizeof(double))

    cdef int i = 0
    for i in range(len):
        res[i] = a[i]-b[i]
    #free(a)
    #free(b)
    return res

cdef sub_py(double *a, b, int len):
# function to subtract a c-array and a python array elementwise
    res = [0] * len
    #res = <double*>malloc(len*sizeof(double))
    cdef int i = 0
    while i < len:
        print len
        res[i] = a[i]-b[i]
        i += 1
    return res

cdef add_py(a, double *b, int len):
# function to subtract two arrays elementwise
    res = [0] * len
    #res = <double*>malloc(len*sizeof(double))
    cdef int i = 0
    for i in range(len):
        res[i] = a[i]+b[i]
    #free(b)
    return res

cdef double * add_cy(double *a, double *b, int lenA):
    cdef int i = 0
    while i < lenA:
        a[i] += b[i]
        i += 1
    return a


'''
cdef double * evalfuncMagDot_cy(double *P, double *S, int lenP, int lenS):
#cdef double * evalfuncMagDot_cy(P, double *S, int lenP, int lenS):
    cdef double *result
    result = <double*>malloc(3*sizeof(double))
    cdef double *H
    H = <double*>malloc(3*sizeof(double))
    cdef double *R
    R = <double*>malloc(3*sizeof(double))

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

    H = sub(P,S,len(P))        # this worked for the example on the flat paper...
    R = sub(S,P,len(P))
    cdef double result[3]
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




def funcMagY_cy(P,S,B):
    cdef int lenP, lenS, lenB
    cdef int i, j, k
    # generate an int for the length, because it's safer to pass this variable
    # than handling sizes of arrays and types...
    lenP = len(P)
    lenS = len(S)
    lenB = len(B)
    # declaring the arrays...
    cdef double *pArr
    pArr = <double*> malloc(lenP*sizeof(double))
    i = 0
    for i in range(lenP):
        pArr[i] = P[i]
    cdef double *sArr = <double*>malloc(lenS*sizeof(double))
    i = 0
    for i in range(lenS):
        sArr[i] = S[i]
    cdef double *bArr = <double*>malloc(lenB*sizeof(double))
    i = 0
    for i in range(lenB):
        bArr[i] = B[i]

    cdef double *sAct    # the actual S-Array
    sAct = <double*> malloc(3*sizeof(double))
    cdef double *pAct    # the actual P-Array
    pAct = <double*> malloc(3*sizeof(double))

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
    opt = ({'maxiter':50})
#    val = minimize(funcMagYmulti, P, args=(S,B), method='slsqp',
#                   tol=1e-5, bounds=bnds, jac=jacobian)
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
'''

#'''
#  angle estimation
#'''
'''
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
'''
#'''
#  describing the whole estimation as angle-estimation
#'''
'''
cdef double xPos_cy(double *angle,double *phal,double off):
    return (phal[0]*np.cos(angle[0])+
            phal[1]*np.cos((angle[0])+(angle[1]))+
            phal[2]*np.cos((angle[0])+(angle[1])+(angle[2]))+off)

cdef double yPos_cy(double *angle,double *phal,double off):
    return off

cdef double zPos_cy(double *angle,double *phal,double off):
    return (phal[0]*np.sin((angle[0]))+
            phal[1]*np.sin((angle[0])+(angle[1]))+
            phal[2]*np.sin((angle[0])+(angle[1])+(angle[2])))*-1+off

cdef double * angToB_cy(double *theta,double *finger,double *off,double *S):
    cdef double *P
    P = <double*> malloc(3*sizeof(double))
    P[0] = xPos_cy(theta,finger,off[0])
    P[1] = yPos_cy(theta,finger,off[1])
    P[2] = zPos_cy(theta,finger,off[2])

    cdef double *R = sub(S,P,3)

    cdef double *H
    H = <double*> malloc(3*sizeof(double))
    H[0] = np.sin(-np.pi/2+abs(-theta[0]-theta[1]-theta[2]))
    H[1] = 0
    H[2] = np.cos(-np.pi/2+abs(-theta[0]-theta[1]-theta[2]))
    #cdef double normR = cal_norm_cy(R,3)

    cdef double *res
    res = <double*> malloc(3*sizeof(double))
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
    cdef double *arrCal
    arrCal = <double*> malloc(lenB*sizeof(double))

    cdef double *tmp
    tmp = <double*> malloc(3*sizeof(double))

    cdef double *actS
    actS = <double*> malloc(3*sizeof(double))
    cdef double *actTheta
    actTheta = <double*> malloc(3*sizeof(double))
    cdef double *actFinger
    actFinger = <double*> malloc(3*sizeof(double))
    cdef double *actOff
    actOff = <double*> malloc(3*sizeof(double))

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

    #cdef double res_cy = cal_norm_cy(sub(arrB,arrCal,lenB),lenB)
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



cdef double * angToP_cy(double *theta, double *finger, double *off):
    cdef double PI = 3.14159265358979323846
    cdef double *res = <double*> malloc(3*sizeof(double))
    cdef double finger_0 = 0.
    cdef double theta_k = 0.0
    #cdef int dk = off
    res[0] = (1*(finger_0*sin(PI/2) + finger[0]*sin(PI/2-theta[0]) +              # x
              finger[1]*sin(PI/2-theta[0]-theta[1]) +
              finger[2]*sin(PI/2-theta[0]-theta[1]-theta[2]))+off[0])
    res[1] = ((finger[0]*cos(PI/2-theta[0]) +                  # y
              finger[1]*cos(PI/2-theta[0]-theta[1]) +
              finger[2]*cos(PI/2-theta[0]-theta[1]-theta[2]))*sin(theta_k)+off[1])
    res[2] = (-1*(finger[0]*cos(PI/2-theta[0]) +               # z (*-1 because you move in neg. z-direction)
              finger[1]*cos(PI/2-theta[0]-theta[1]) +
              finger[2]*cos(PI/2-theta[0]-theta[1]-theta[2]))*cos(theta_k)+off[2])
    return res

cdef double * angToH_cy(double *theta):
    cdef double *res = <double*> malloc(3*sizeof(double))
    res[0] = cos(-theta[0]-theta[1]-theta[2])
    res[1] = 0.0
    res[2] = 1*sin(-theta[0]-theta[1]-theta[2])
    return res

cdef double * calcB_cy(double *r, double *h):
    cdef double PI = 3.14159265358979323846
    cdef double *b = <double*> malloc(3*sizeof(double))
    cdef double factor = (1./(4.*PI))
    cdef double no = cal_norm_cy(r,3)
    b[0] = (((3*r[0]*dot_product(h,r,3))/pow(no,5)) - (h[0]/pow(no,3)))*factor
    # b[1] = ((3*r[1]*dot_product(h,r,3))/pow(no,5)) - (h[1]/pow(no,3))*0
    b[1] = 0
    b[2] = (((3*r[2]*dot_product(h,r,3))/pow(no,5)) - (h[2]/pow(no,3)))*factor
    return b

cdef double * angToB_m_cy(double *theta, double *finger, double *S, double *off, int lenS):
    cdef double *res = <double*> malloc(lenS*sizeof(double))
    cdef double *sAct = <double*> malloc(3*sizeof(double))
    cdef double *r = <double*> malloc(3*sizeof(double))
    cdef double *P = <double*> malloc(3*sizeof(double))
    cdef double *H = <double*> malloc(3*sizeof(double))
    cdef double *tmp = <double*> malloc(3*sizeof(double))

    P = angToP_cy(theta,finger,off)
    H = angToH_cy(theta)

    cdef int i = 0
    cdef int j = 0
    while i < (lenS/3):
        j = 0
        while j < 3:
            sAct[j] = S[i*3+j]
            j += 1
        r = sub(sAct,P,3)
        tmp = calcB_cy(r,H)
        j = 0
        while j < 3:
            res[i*3+j] = tmp[j]
            j += 1
        i += 1

    free(sAct)
    free(r)
    free(P)
    free(H)
    free(tmp)

    return res

def funcMagY_angle_m2_cy(theta,finger,S,off,B):
    cdef int j = 0
    cdef int i = 0

    # allocate all arrays
    cdef int lB = len(B)
    cdef double *cal_c = <double*> malloc(lB*sizeof(double))
    while i < lB:
        cal_c[i] = 0
        i += 1

    cdef int lTheta = len(theta)
    cdef double *theta_c = <double*> malloc(3*sizeof(double))
    i = 0
    while i < 3:
        theta_c[i] = 0
        i += 1

    cdef int lFinger = len(finger)
    cdef double *finger_c = <double*> malloc(3*sizeof(double))
    i = 0
    while i < 3:
        finger_c[i] = 0
        i += 1

    cdef int lS = len(S)
    cdef double *sPos_c = <double*> malloc(lS*sizeof(double))
    i = 0
    while i < lS:
        sPos_c[i] = S[i]
        i += 1

    cdef int lOff = len(off)
    cdef double *off_c = <double*> malloc(lOff*sizeof(double))
    i = 0
    while i < lOff:
        off_c[i] = off[i]
        i += 1

    if lS != lB:
        print "wrong number of sensors, to corresponding B-fields!"
        return 0
    elif lFinger != lOff:
        print "wrong number of fingerlength, to finger offsets!"
        return 0

    else:
        while j < (lFinger/3):
            # assign the actual values to the arrays
            i = 0
            while i < 3:
                finger_c[i] = finger[i+j*3]
                off_c[i] = off[i+j*3]
                i += 1
            theta_c[0] = theta[j*2]
            theta_c[1] = theta[j*2+1]
            theta_c[2] = theta[j*2+1]*2/3
            cal_c = add_cy(cal_c,angToB_m_cy(theta_c,finger_c,sPos_c,off_c,lS),lB)
            j += 1
        i = 0
        a = [0]*lB
        while i < lB:
            a[i] = cal_c[i]
            i += 1
        # t = sub_py(cal_c,B,lB)
        t = a-B
        res_py = cal_norm_py(t)

        free(cal_c)
        free(theta_c)
        free(finger_c)
        free(sPos_c)
        free(off_c)
        return res_py**2     #take the square of it!

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

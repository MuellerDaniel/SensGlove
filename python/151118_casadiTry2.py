import casadi as cs
import numpy as np
import modelEqMultiCython as modE
import matplotlib.pyplot as plt
import plotting as plo

def H(x):
#    res = cs.SX.sym('res',3)
    res = np.array([0,0,0])
    arr = modE.angToH(x)
#    res[0] = arr[0]
#    res[1] = arr[1]
#    res[2] = arr[2]
#    res[0] = sin(-np.pi/2+cs.fabs(-x[0]-x[1]-x[2]))
#    res[1] = 0
#    res[2] = -cos(-np.pi/2+cs.fabs(-x[0]-x[1]-x[2]))
    
    return arr

def P(x,phal,off):
    theta = x
    finger = phal
    finger_0 = 0.    
    theta_k = 0.0
    dk = off
    arr = np.array([(1*(finger_0*np.sin(np.pi/2) + finger[0]*np.sin(np.pi/2-theta[0]) +              # x
                finger[1]*np.sin(np.pi/2-theta[0]-theta[1]) +
                finger[2]*np.sin(np.pi/2-theta[0]-theta[1]-theta[2]))),                 
                ((finger[0]*np.cos(np.pi/2-theta[0]) +                  # y
                finger[1]*np.cos(np.pi/2-theta[0]-theta[1]) +
                finger[2]*np.cos(np.pi/2-theta[0]-theta[1]-theta[2]))*np.sin(theta_k)+dk),
                (-1*(finger[0]*np.cos(np.pi/2-theta[0]) +               # z (*-1 because you move in neg. z-direction)
                finger[1]*np.cos(np.pi/2-theta[0]-theta[1]) +
                finger[2]*np.cos(np.pi/2-theta[0]-theta[1]-theta[2]))*np.cos(theta_k))])
    
    return arr
    
def B(H,R):
#    res = cs.SX.sym('res',3)
#    res = np.array([0,0,0])
    arr = modE.calcB(R,H)
    
    return arr
    
def angToB(theta,phal,joint,s):
    h = H(theta)
    print "h: ",h
    p = P(theta,phal,joint)
    print "p: ",p
#    r = s-P(theta,phal,joint)
#    a = B(h,r)
#    print "angToB: ",a
    return h
    
def testFun(x):
    a = cs.SX.sym('a',3)
    a[0] = x[0]*3
    a[1] = x[2]**2
    a[2] = x[1]+5
    print "testFun: ",a
    return a 
    
def estimate_BtoAng(theta_0,phal,joint,s,b):
    theta_x = cs.SX.sym('theta',3)
    print "theta_0", theta_0
    print "phal",phal
    measB = [float(i) for i in b.tolist()]
    print "b",measB
   
    f = cs.norm_2(angToB(theta_x,phal,joint,s)-measB)
#    f = cs.norm_2(testFun(theta_x)-b)
    nlp = cs.SXFunction( cs.nlpIn(x=theta_x), cs.nlpOut(f=f))
    solver = cs.NlpSolver("ipopt", nlp)
    
    solver.init()
    solver.setInput(theta_0,'x0')    
    solver.setInput(0.,'lbx')
    solver.setInput([np.pi/2,np.pi/(180/110),np.pi/2],'ubx')
    solver.evaluate()
    x = solver.getOutput('x')
#    val = solver.getOutput('f')
    return x
    
    
''' describing the data '''
t = np.arange(0, 1/2.*np.pi, 0.01) 
sMid = [-0.071, -0.022, 0.0]
yMid = -0.022
phalMid = [0.03593, 0.03137, 0.01684]

angles = np.zeros((len(t)*2,3))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0., 0.])
    cnt += 1

for i in t[::-1]:
    angles[cnt] = np.array([i, 0., 0.])
    cnt += 1

calcBMid = np.array([[0.,0.,0.]])
#pos = np.array([[0.,0.,0.]])
#orien = np.array([[0.,0.,0.]])
for i in angles:
    calcBMid = np.append(calcBMid, modE.angToB(i,phalMid,sMid,yMid),axis=0)
#    pos = np.append(pos, [modE.angToP(i,phalMid,jointMid)],axis=0)
#    orien = np.append(orien, [modE.angToH(i)],axis=0)
calcBMid = calcBMid[1:]
#pos = pos[1:]
#orien = orien[1:]
    
''' casadi version '''
estAngCalcCS = [[0.,0.,0.]] 
for i in range(len(calcBMid[1:])):
    estAngCalcCS = np.append(estAngCalcCS,np.array(estimate_BtoAng(estAngCalcCS[i],
                            phalMid,yMid,sMid,calcBMid[i+1])).T,axis=0)
    
    
#b = angToB(angles[0],phalMid,yMid,sMid)
#est = estimate_BtoAng([0.,0.,0.],phalMid,yMid,sMid,calcBMid[1])

''' python version '''
bnds = ((0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP  
        (0.0,np.pi/2))


estAngCalcMid = np.zeros((len(calcBMid),3)) 
#error = np.zeros((len(calcBMid),))       
cnt = 0
errCnt = 0
for i in range(len(calcBMid[1:])):    
    # for one magnet and one sensor...
    res = modE.estimate_BtoAng(estAngCalcMid[i],
                               [phalMid],
                               [yMid],
                               [sMid],
                               calcBMid[i+1],bnds)                                
    if not res.success:
        errCnt += 1
        print "error!", cnt                  
    estAngCalcMid[i+1] = res.x[:3]        
    cnt += 1
#    error[i+1] = res.fun                

plt.close('all')
plo.plotter2d((calcBMid,estAngCalcMid,estAngCalcCS),("b","anglePy","angleCS"),shareAxis=False)

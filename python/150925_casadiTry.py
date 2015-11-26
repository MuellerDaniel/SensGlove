from casadi import *
import numpy as np
import modelEqMultiCython as modE
import matplotlib.pyplot as plt
import plotting as plo

def estimate(P0,Sa,Ba):
    P = SX.sym('P',3)
#    s0 = [0.02957, 0.06755, 0.]
#    b0 = np.array([0.        , -182.50857868,  -19.10688867])
    s0 = Sa
    b0 = Ba
    H = P-s0
    R = s0-P
    factor = np.array([-1,-1,-1])
    
    B = np.linalg.norm(b0 - np.array((3*(np.dot(H.T,R)*R)/(np.linalg.norm(R)**5)) - (H/(np.linalg.norm(R)**3))) * factor)
    #g = x[2] + (1-x[0])**2 - x[1]
    
    # Create NLP function
    nlp = SXFunction( nlpIn(x=P), nlpOut(f=B,g=B) )
    
    # Formulate and solve NLP
    solver = NlpSolver("ipopt", nlp)
    
    solver.init()
#    solver.setInput([0.02957,  0.17138,  0.01087],'x0')
    solver.setInput(P0,'x0')
    solver.setInput(0,'lbg')
    solver.setInput(0,'ubg')
    solver.evaluate()
#    print "this is the output: ",solver.getOutput('x')
    return solver.getOutput('x')
    
    
''' describing the data '''
t = np.arange(0, 1/2.*np.pi, 0.01) 
pos1 = [[0.,0.,0.]] 
angInd = [0.02957, 0.09138, 0.01087]
rInd = 0.08

for i in t:    
    # position of the index finger
    pos1 = np.append(pos1, [[angInd[0],       
                            angInd[1]+rInd*np.cos(i),        
                            angInd[2]+rInd*np.sin(i)]], 
                            axis=0) 
pos1 = pos1[1:]                            
calcB = [[0.,0.,0.]]    
s1 = [0.02957, 0.06755, 0.]

for i in range(pos1.shape[0]):
    calcB = np.append(calcB,
                       modE.evalfuncMagDot(pos1[i],s1), axis=0)    
calcB = calcB[1:]                       
    
#P0 = [0.02957,  0.17138,  0.01087]
#S = [0.02957, 0.06755, 0.]
#B = [0.        , -182.50857868,  -19.10688867]
estPos = np.zeros((pos1.shape[0],3))
estPos[0] = pos1[0]

''' the estimation loop '''
for i in range(pos1.shape[0]-1):
#    print "ESTPOS.SHAPE: ", estPos[i].shape
    estPos[i+1] = estimate(estPos[i],s1,calcB[i+1]).T

plo.multiPlotter(estPos,"Index",pos1)
#    
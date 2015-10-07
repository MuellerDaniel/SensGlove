from scipy.optimize import *
import numpy as np


def xPos(angle,phal,off):
    return (phal[0]*np.cos(angle[0])+
            phal[1]*np.cos((angle[0])+(angle[1]))+
            phal[2]*np.cos((angle[0])+(angle[1])+(angle[2]))+off)
            
# for simplicity neglect it...            
def yPos(angle,phal,off):
    return off            

def zPos(angle,phal,off):
    return (phal[0]*np.sin((angle[0]))+
            phal[1]*np.sin((angle[0])+(angle[1]))+
            phal[2]*np.sin((angle[0])+(angle[1])+(angle[2]))+off)*-1

          
def calcPosition(angle,phal,offSet):
    res = np.array([xPos(angle,phal,offSet[0]),
                    yPos(angle,phal,offSet[1]),
                    zPos(angle,phal,offSet[2])])
    return res
          
def posFun(angle,pos,phal,off):
#    print "angle", angle
#    print "pos", pos
#    print "off", off
    estimated = calcPosition(angle,phal,off)
    diff = pos - estimated
    print "diff: ", diff
    res = np.linalg.norm(diff)
    return res                  
                     
def estimateAngle(pos,guess,off,phal,bnds):
#    print "bla"
    res = minimize(posFun,guess,args=(pos,phal,off),method='slsqp',
                   bounds=bnds,tol=1e-12)
    return res                       
            

"""Type I (static) constraints: """
#0 < phi1(MCP) < 90
#0 < phi2(PIP) < 110
#0 < phi3(DIP) < 90 
#(-15 < phi0(ab/adduction) < 15) 

bnds = ((0,np.pi/2),
        (0,(110/180*np.pi)),
        (0,np.pi/2))
  
""" Type II (dynamic, during motion) constraints: """
#phi2 = 2/3 * phi3 (intra finger constraint)    

angleOff = np.array([0.,0.,0.])
phal = [0.03494, 0.03102, 0.02337]
tstPos = np.array([0,0,-1*sum(phal)])
guess = np.array([10,0,5])

#print calcPosition(guess,angleOff)
print calcPosition([0,0,0],phal,angleOff)

a = estimateAngle(tstPos,guess,angleOff,phal,bnds)
#print a.x
#a = posFun(guess,tstPos,angleOff)

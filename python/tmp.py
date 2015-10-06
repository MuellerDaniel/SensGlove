import numpy as np

def gradToRad(grad):
    return (float(grad)/180.) * 2*np.pi

l1 = 0.03494
l2 = 0.03102
l3 = 0.02337
xOff = 0
yOff = 0
zOff = 0

def xPos(phi1,phi2,phi3):
    return (l1*np.sin(gradToRad(phi1))+
            l2*np.sin(gradToRad(phi1)-gradToRad(phi2))+
            l3*np.sin(gradToRad(phi1)-gradToRad(phi2)-gradToRad(phi3))+xOff)

    


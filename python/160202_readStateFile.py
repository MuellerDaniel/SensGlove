import numpy as np
import matplotlib.pyplot as plt
import plotting as plo
import dataAcquisitionMulti as datAc
    
    
#def readMagState(mStateF):
sstring = 'set4'    
        
leapFile = "../datasets/160217/160217_"+'set1'+"_leap"    
magFile = "../datasets/160217/160217_"+sstring+"_mag"

#caliFile = "../datasets/160217/160217_"+'cali3'
#(tC,s1c,s2c,s3c,s4c) = datAc.readMag(caliFile)

(tLeap,ind,mid,rin,pin) = datAc.readLeap(leapFile)
#(tMag,s1,s2,s3,s4) = datAc.readMag(magFile1)
(tMag,s1,s2,s3,s4) = datAc.readMag(magFile)

#plo.plotAngles(tLeap,(ind,mid,rin,pin),head='leapStates set5')

#plo.plotLeapVsMag((np.zeros((3,1)),np.zeros((3,3))),(tMag,s1,s2,s3,s4),head=sstring)
#plo.plotLeapVsMag((tLeap,ind),(tC,s1c,s2c,s3c,s4c),head="cli")
plo.plotLeapVsMag((tLeap,ind),(tMag,s1,s2,s3,s4),head=sstring)
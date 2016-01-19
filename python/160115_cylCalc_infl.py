import modelCyl as modC
import modelEqMultiCython as modE
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np
import time,random

''' script for calculation and estimation of several fingers, 
    WITH influencing each other  '''

def diffRadial(p1,p2):
    tmp = np.sqrt((p1[1][0]-p2[1][0])**2+(p1[1][1]-p2[1][1])**2)
    return np.array([p1[0]-p2[0],tmp])

#           prox-,   int-,     dist-    phalanges
phalInd = np.array([0.03080, 0.02581, 0.01678])
phalMid = np.array([0.03593, 0.03137, 0.01684])
phalRin = np.array([0.03404, 0.02589, 0.01820])
phalPin = np.array([0.02892, 0.02493, 0.01601])

# sensor positions 
#     [lateral(z(sensor_x)), radial[x_ulnar(sensor_-y),x_dorsal(sensor_+z)]]
sInd = [0.03,            [0,             0.024]]     # rack1
sMid = [0.03,            [0.02,             0.024]]
sRin = [0.03,            [0.04,             0.024]]
sPin = [0.03,            [0.06,             0.024]]

# joint position 
#        [lateral(z), [x_ulnar(sensor_-y),x_dorsal(sensor_+z)]]
jointInd = [0.0,             [0,                    0.0]]
jointMid = [0.0,             [0.02,                    0.0]]
jointRin = [0.0,             [0.04,                    0.0]]
jointPin = [0.0,             [0.06,                    0.0]]


t = np.arange(0,np.pi/2,0.01)
#t = np.arange(0.6,1.0,0.001)
angles = np.zeros((len(t),2))
angles_m = np.zeros((len(t),2*4))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0.])
    angles_m[cnt] = np.array([i, 0.,    # angle index
                              0, i,    # angle mid
                              i, i*0.5,    # angle rin
                              0.4, i*0.9])   # angle pin
    cnt += 1
    

#angList = [angles, angles[::-1]]
fingList = [phalMid]
sensList = [sInd]
jointList = [jointMid]

b_multA = np.zeros((len(angles),2*len(sensList)))
b_multB = np.zeros((len(angles),2*len(sensList)))
b_conA = np.zeros((len(angles),2))
b_conB = np.zeros((len(angles),2))

b_ind = np.zeros((len(angles),2))  
b_mid = np.zeros((len(angles),2))  
b_rin = np.zeros((len(angles),2))  
b_pin = np.zeros((len(angles),2))  

cnt = 0
startT = time.time()
for i in angles:
    # mult way...
#    b_mult[cnt] = modC.angToBm_cyl(np.concatenate(([i,angles[-cnt]])),fingList,sensList,jointList) 
#    b_multA[cnt] = modC.cy.angToBm_cyl_cy(np.concatenate(([i, i, i, i])),fingList,sensList,jointList) 
    b_multB[cnt] = modC.cy.angToBm_cyl_cy(angles[cnt],fingList,sensList,jointList) 
    
#    b_conA[cnt] = (modC.angToB_cyl(i,phalInd,sInd,jointInd) + 
#                    modC.angToB_cyl(angles[-cnt],phalMid,sInd,jointMid))    
#    b_conB[cnt] = (modC.angToB_cyl(i,phalInd,sMid,jointInd) + 
#                    modC.angToB_cyl(angles[-cnt],phalMid,sMid,jointMid))
                    
    # single way...
    b_ind[cnt] = modC.cy.angToBm_cyl_cy(i,phalInd,sInd,jointInd) 
#    b_mid[cnt] = modC.angToB_cyl(i,phalMid,sInd,jointMid)    
#    b_rin[cnt] = modC.angToB_cyl(i,phalRin,sInd,jointRin)    
#    b_pin[cnt] = modC.angToB_cyl(i,phalPin,sInd,jointPin)    
    cnt += 1
print "time needed simulation: ", time.time()-startT    

''' estimation '''
#startT = time.time()
#a = modC.estimateAng_cyl([0,0], phalMid, sMid, jointMid, b_cyl[-1])
#print "time needed: ", time.time()-startT
#print a.x
#print angles[-1]
   
estAngm = np.zeros((len(angles),len(sensList)*2))   
estAng_Ind = np.zeros((len(angles),2))   
#estAng_Mid = np.zeros((len(angles),2))   
#estAng_Rin = np.zeros((len(angles),2))   
#estAng_Pin = np.zeros((len(angles),2))   
##tolerance = 1.e-06
#cnt = 0
startT = time.time()
for i in range(len(b_ind[1:])):    
    print "estimating step ",i ," of ", len(angles)
    temp = modC.estimateAng_cyl(estAngm[i], fingList, sensList, jointList, b_multB[i+1])
    estAngm[i+1] = temp.x
#    temp = modC.estimateAng_cyl(estAng_Ind[i], np.array(phalInd), sInd, jointInd, b_ind[i+1])
#    estAng_Ind[i+1] = temp.x    
#    temp = modC.estimateAng_cyl(estAng_Mid[i], np.array(phalMid), sMid, jointMid, b_mid[i+1])
#    estAng_Mid[i+1] = temp.x    
#    temp = modC.estimateAng_cyl(estAng_Rin[i], np.array(phalRin), sRin, jointRin, b_rin[i+1])
#    estAng_Rin[i+1] = temp.x    
#    temp = modC.estimateAng_cyl(estAng_Pin[i], np.array(phalPin), sPin, jointPin, b_pin[i+1])
#    estAng_Pin[i+1] = temp.x    
    cnt += 1    
print "time needed estimation: ", time.time()-startT   
   
plt.close('all')
#plo.plotter2d((b_mid,),("index",))
#plo.plotter2d((b_mult,b_ind,b_mid,b_rin,b_pin),("multi","index","middle","ring","pinky"))
#plo.plotter2d((b_multA[:,0:2],b_multB[:,0:2],b_multA[:,2:4],b_multB[:,2:4]),("multiA","cyA","multB","cyB"))
#plo.plotter2d((b_mult[:,0:2],b_conA,b_mult[:,2:4],b_conB),("multiA","cyA","multB","cyB"))
plo.plotter2d((estAngm[:,0:2],estAngm[:,2:4],estAngm[:,4:6],estAngm[:,6:]),("ind","mid","rin","pin"))
#plt.figure()
#plo.plotter2d((estAng_Ind,estAng_Mid,estAng_Rin,estAng_Pin),("angle Ind","angle Mid","angle Rin","angle Pin"))


plt.show()

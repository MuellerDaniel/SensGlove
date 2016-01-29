import modelCyl as modC
#import modelCyl3D as mod3D
import numpy as np
import plotting as plo
import matplotlib.pyplot as plt
import handDim as h
import time

''' moving magnet on paper... '''
#angA = 1*np.pi/2
#a = np.arange(0.05, 0.1, 0.001)
#pos2D = np.zeros((len(a),2))
#pos3D = np.zeros((len(a),3))
#
#cnt = 0
#for i in a:
#    pos3D[cnt] = np.array([i, 0.03, -0.002])
#    pos2D[cnt] = np.array([i, 0.])
#    cnt += 1
#
#b2D = np.zeros((len(a),2))
#calcPos2D = np.zeros((len(a),2))
#cnt = 0
#for i in pos2D:
#    (b2D[cnt], calcPos2D[cnt]) = modC.calcB_cyl(i, angA)
#    cnt += 1
#
#
#b3D = np.zeros((len(a),3))
#calcPos3D = np.zeros((len(a),2))
#cnt = 0
#for i in pos3D:
#    (b3D[cnt], calcPos3D[cnt]) = mod3D.calcB_cyl(i, angA)
#    cnt += 1
#    
#    
#plt.close('all')    
#plo.plotter2d((b2D,b3D),("B2d","B3d"),shareAxis=False) 
#plo.plotter2d((calcPos2D,calcPos3D), ("pos2d","pos3d"))


''' hand '''

fingList = [h.phalInd, h.phalMid, h.phalRin, h.phalPin]
sensList = [h.sInd_carC, h.sMid_carC, h.sRin_carC, h.sPin_carC]
jointList = [h.jointInd_car, h.jointMid_car, h.jointRin_car, h.jointPin_car]

a = np.arange(0.,np.pi/2, 0.01)
angles = np.zeros((len(a),2*len(fingList)))
cnt = 0
for i in a:
    angles[cnt] = np.array([i, 0,    # angle index
                            0.3, i*0.4,    # angle mid
                            i, 0.4,    # angle rin
                            i, i*0.3])   # angle pin    
    cnt += 1
    
fingB2D = np.zeros((len(a),2))    
#cnt = 0
#for i in angles:
#    fingB2D[cnt] = modC.angToB_cyl(i, h.phalMid,np.array([0.03, 0.]), np.array([0., 0.024]))
#    cnt += 1


#angList = [angles, angles]

fingB3D = np.zeros((len(a),3*len(sensList)))
cnt = 0
for i in range(len(angles)):
#    fingB3D[cnt] = mod3D.angToB_cyl(angles[i],fingList,sensList,jointList)
    fingB3D[cnt] = modC.cy.angToB_cyl(angles[i], fingList, sensList, jointList)
    cnt += 1
    



''' estimation... '''
bnds = ((0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2))
print "estimation running..."
estAng = np.zeros((len(fingB3D),2*len(fingList)))
cnt = 0
startT = time.time()
for i in fingB3D[1:]:
    tmp = modC.estimateAng_cyl(estAng[cnt], fingList, sensList, jointList, i, bnds)    
    print tmp.fun
    estAng[cnt+1] = tmp.x
    cnt += 1

print "time needed: ", time.time()-startT

plt.close('all')
plo.plotter2d((fingB3D[:,:3],fingB3D[:,3:6],fingB3D[:,6:9],fingB3D[:,9:]),("ind","mid","ring","pinky"))
plt.figure()
plo.plotter2d((estAng[:,:2],estAng[:,2:4],estAng[:,4:6],estAng[:,6:]),("ANGLEind","mid","ring","pinky"))



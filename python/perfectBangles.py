import numpy as np
import modelCyl as modC
import modelDip as modD
import handDim as h
import plotting as plo
import matplotlib.pyplot as plt
import time

''' simulating and estimating with the models '''

sensList_cyl = [h.sInd_carC, h.sMid_carC, h.sRin_carC, h.sPin_carC]
#sensList_cyl = [h.sPin_rad]
fingList_cyl = [h.phalMid]
#fingList_cyl = [h.phalPin]
jointList_cyl = [h.jointMid_car]
#jointList_cyl = [h.jointPin_rad]


sensList_dip = [h.sInd_car, h.sMid_car, h.sRin_car, h.sPin_car]
fingList_dip = [h.phalMid]
#fingList_dip = [h.phalPin]
jointList_dip = [h.jointMid_car]
#jointList_dip = [h.jointPin_car]


''' simulation '''
t = np.arange(0,np.pi/2,0.01)       # describing the angles
angles_cyl = np.zeros((len(t),2*len(fingList_cyl)))
angles_dip = np.zeros((len(t), 3*len(fingList_dip)))
cnt = 0
for i in t:
#    TODO adjust it on the number of fingers you want to measure
    angles_cyl[cnt] = np.array([i, 0])#,    # angle index
#                              0, i,    # angle mid
#                              i, 0.4,    # angle rin
#                              i, i*0.3])   # angle pin
    
    angles_dip[cnt] = np.array([i, 0, 0])#,
#                                0, i, 0,
#                                i, 0.4, 0,
#                                i, i*0.3, 0])    
    
    cnt += 1
    
b_cyl = np.zeros((len(t), 3*len(sensList_cyl)))
b_dip = np.zeros((len(t), 3*len(sensList_dip)))    

cnt = 0
for i in range(len(t)):
    b_cyl[i] = modC.cy.angToB_cyl(angles_cyl[i],fingList_cyl,sensList_cyl,jointList_cyl)    # simulating cylindrical model
#    b_dip[i] = modD.angToBm(angles_dip[i],fingList_dip,sensList_dip,jointList_dip)              # simulating dipole model
#    b_dip[i] = modD.cy.angToBm_cy(angles_dip[i],fingList_dip,sensList_dip,jointList_dip)
    
plt.close('all')    
#plo.plotter2d((b_cyl,b_dip),("cyl","dip"),shareAxis=False)
#plo.plotter2d((b_dip[:,:3], b_dip[:,3:6], b_dip[:,6:9], b_dip[:,9:]),("a","a","a","a"))
#plo.plotter2d((b_cyl[:,:2], b_cyl[:,2:4], b_cyl[:,4:6], b_cyl[:,6:]),("c","c","c","c"))  
plo.plotter2d((b_cyl,),("mid",))  


''' estimation '''
## cylindrical model
estAng_cyl = np.zeros((len(b_cyl), 2*len(fingList_cyl)))
bnds_cyl = ((0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.))

#startCyl = time.time()
#cnt = 0
#for i in b_cyl[1:]:
#    print "cylindrical estimation step: ", cnt
#    tmp = modC.estimateAng_cyl(estAng_cyl[cnt], fingList_cyl, sensList_cyl, jointList_cyl, i, bnds=bnds_cyl)
#    print "function value: ", tmp.fun
#    estAng_cyl[cnt+1] = tmp.x
#    
#    cnt += 1
#
#timeCyl = time.time()-startCyl    
#plo.plotter2d((estAng_cyl[:,:2], estAng_cyl[:,2:4],estAng_cyl[:,4:6],estAng_cyl[:,6:]),("i","m","r","p"))    
    

## dipole model
estAng_dip = np.zeros((len(b_dip), 3*len(fingList_dip)))    
bnds_dip = ((0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.),
            (0.0,np.pi/2.))

#startDip = time.time()
#cnt = 0
#for i in b_dip[1:]:
#    print "dipole estimation step: ", cnt
##    tmp = modD.estimate_BtoAng(estAng_dip[cnt],fingList_dip,jointList_dip,sensList_dip,i)
#    tmp = modD.estimate_BtoAng(estAng_dip[cnt],fingList_dip,jointList_dip,sensList_dip,i,bnds=bnds_dip)
#    print "function value: ", tmp.fun
#    estAng_dip[cnt+1] = tmp.x
#    
#    cnt += 1
#
#timeDip = time.time()-startDip

#plo.plotter2d((estAng_dip[:,:2], estAng_dip[:,2:4],estAng_dip[:,4:6],estAng_dip[:,6:]),("di","dm","dr","dp"))    
#print "time for cyl: ", timeCyl
#print "time for dip: ", timeDip

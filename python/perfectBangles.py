import numpy as np
import modelCyl as modC
import modelDip as modD
import handDim as h
import plotting as plo
import matplotlib.pyplot as plt
import jacB_oneone as joo
import jacB_onefour as jof
import jacB_fourfour as jff
import time

''' simulating and estimating with the models '''

sensList = [h.sInd,h.sMid,h.sRin,h.sPin]
#sensList = [h.sInd]
fingList = [h.phalInd, h.phalMid, h.phalRin, h.phalPin]
#fingList = [h.phalInd]
jointList = [h.jointInd, h.jointMid, h.jointRin, h.jointPin]
#jointList = [h.jointInd]



''' simulation '''
t = np.arange(0,np.pi/2,0.1)       # describing the angles
angles_cyl = np.zeros((len(t),2*len(fingList)))
cnt = 0
for i in t:
#    TODO adjust it on the number of fingers you want to measure
    angles_cyl[cnt] = np.array([i, 0,    # angle index
                                i, 0.,    # angle mid
                                i, 0.,    # angle rin
                                i, 0])   # angle pin
        
    cnt += 1
    
b_cyl = np.zeros((len(t), 3*len(sensList)))
b_dip = np.zeros((len(t), 3*len(sensList)))    

cnt = 0
for i in range(len(t)):
    b_cyl[i] = modC.cy.angToB_cyl(angles_cyl[i],fingList,sensList,jointList)    # simulating cylindrical model
    b_dip[i] = modD.cy.angToBm_cy(angles_cyl[i],fingList,sensList,jointList)              # simulating dipole model
    
#plt.close('all')    
#plo.plotter2d((b_cyl,b_dip),("cyl","dip"),shareAxis=False)
#plo.plotter2d((b_dip[:,:3], b_dip[:,3:6], b_dip[:,6:9], b_dip[:,9:]),
#              ("dipole index","dipole middle","dipole ring","dipole pinky"))
#plo.plotter2d((b_cyl[:,:3], b_cyl[:,3:6], b_cyl[:,6:9], b_cyl[:,9:]),
#              ("cyl index","cyl middle","cyl ring","cyl pinky"))  
#plo.plotter2d((b_cyl,),("mid",))  


''' estimation '''
## cylindrical model
estAng_cyl = np.zeros((len(b_cyl), 2*len(fingList)))
fun_cyl = np.zeros((len(b_cyl),))
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
#    tmp = modC.estimateAng_cyl(estAng_cyl[cnt], fingList, sensList, jointList, i, bnds=bnds_cyl[:len(fingList)*2], method=2)
##    print "function value: ", tmp.fun
#    estAng_cyl[cnt+1] = tmp.x
#    fun_cyl[cnt+1] = tmp.fun
#    
#    cnt += 1
#
#timeCyl = time.time()-startCyl     
    

## dipole model
estAng_dip = np.zeros((len(b_dip), 2*len(fingList)))    
fun_dip = np.zeros((len(b_dip),))
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
#
#startDip = time.time()
#cnt = 0
#for i in b_dip[1:]:
#    print "dipole estimation step: ", cnt
##    tmp = modD.estimate_BtoAng(estAng_dip[cnt],fingList_dip,jointList_dip,sensList_dip,i)
#    tmp = modD.estimate_BtoAng(estAng_dip[cnt],fingList,sensList,jointList,i,bnds=bnds_dip[:len(fingList)*2],method=2)
##    print "function value: ", tmp.fun
#    estAng_dip[cnt+1] = tmp.x
#    fun_dip[cnt+1] = tmp.fun
#    
#    cnt += 1
#
#timeDip = time.time()-startDip

ang_d = modD.estimateSeries(b_dip,fingList,sensList,jointList,bnds=True,met=1)
ang_c = modC.estimateSeries(b_cyl,fingList,sensList,jointList,bnds=True,met=1)
plo.plotter2d((ang_d[:,:3],ang_c[:,:3]),("dipole","cyl"))
#plo.plotter2d((angles_cyl,estAng_dip,ang_d,estAng_cyl,ang_c),("perfect","dip","dipPacked","cyl","cylPacked"))


#plo.plotter2d((estAng_cyl, estAng_dip),("est cyl", "est dip"), mtitle='estimated angles')
#print "time for cyl: ", timeCyl
#print "max cyl: ", max(fun_cyl)
#print "mean cyl: ", np.mean(fun_cyl)
#
#print "time for dip: ", timeDip
#print "max cyl: ", max(fun_dip)
#print "mean cyl: ", np.mean(fun_dip)

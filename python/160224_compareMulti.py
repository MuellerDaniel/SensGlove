import numpy as np
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt

''' calculating the mean and var... '''

def addDip(d):
    dips = np.zeros((len(d),len(d[0])/2))
    for i in range(0,int(len(d[0])/2)):
        dips[:,i] = (d[:,i*2+1]*(2./3.))

    d = np.append(d,dips[:,-1].reshape((len(d),1)),axis=1)

    cnt = 0
    for i in range(2,int(len(d[0])),3):
        d = np.insert(d,i,dips[:,cnt],1)
        cnt += 1

    return d

def printMeanVar(est, sim):
    namelist = ['unconstr Dip A: ', 'unconstr Cyl A:',  'constr Dip A: ', 'constr Cyl A:', ]
    cnt = 0
    for i in est:
        dif = sim-i
        mean = np.mean(np.linalg.norm(dif, axis=1))
        var = np.var(dif)**2
        print "%s %s +- %s" % (namelist[cnt], mean, var)
        # print "var of "+namelist[cnt], var

        cnt += 1


folderStr = "../simResults/24/160225/"
simValues = datAc.readStateFile(folderStr+"simStates.txt")

simValues_nA = np.delete(simValues, np.s_[3],1)
simValues_nA = np.delete(simValues_nA, np.s_[6],1)
# simValues_nA = np.delete(simValues_nA, np.s_[9],1)
# simValues_nA = np.delete(simValues_nA, np.s_[12],1)

loc = folderStr
print "witout ad-ab:"
uDip_nAt = datAc.readStateFile(loc+"estAng_dip0")
uCyl_nAt = datAc.readStateFile(loc+"estAng_cyl0")
cDip_nAt = datAc.readStateFile(loc+"estAng_dip1")
cCyl_nAt = datAc.readStateFile(loc+"estAng_cyl1")
# add dip...
uDip_nA = addDip(uDip_nAt)
uCyl_nA = addDip(uCyl_nAt)
cDip_nA = addDip(cDip_nAt)
cCyl_nA = addDip(cCyl_nAt)
nAlist = [uDip_nA, uCyl_nA, cDip_nA, cCyl_nA]
printMeanVar(nAlist, simValues_nA)

print "\nwith ad-ab:"
uDip_A = datAc.readStateFile(loc+"estAng_dip_A0")
uCyl_A = datAc.readStateFile(loc+"estAng_cyl_A0")
cDip_A = datAc.readStateFile(loc+"estAng_dip_A1")
cCyl_A = datAc.readStateFile(loc+"estAng_cyl_A1")
Alist = [uDip_A, uCyl_A, cDip_A, cCyl_A]
printMeanVar(Alist, simValues)


''' plotting... '''
# plo.plotter2d((uDip_A[:,:4], uDip_A[:,4:8], uDip_A[:,8:12], uDip_A[:,12:]),
#             ("model: uDip_A","middle","ring","pinky"))
# plo.plotter2d((uCyl_A[:,:4], uCyl_A[:,4:8], uCyl_A[:,8:12], uCyl_A[:,12:]),
#             ("model: uCyl_A","middle","ring","pinky"))
# plo.plotter2d((cDip_A[:,:4], cDip_A[:,4:8], cDip_A[:,8:12], cDip_A[:,12:]),
#             ("model: cDip_A","middle","ring","pinky"))
# plo.plotter2d((cCyl_A[:,:4], cCyl_A[:,4:8], cCyl_A[:,8:12], cCyl_A[:,12:]),
#             ("model: cCyl_A","middle","ring","pinky"))
# plo.plotter2d((simValues[:,:4], simValues[:,4:8], simValues[:,8:12], simValues[:,12:]),
#             ("model: simValues","middle","ring","pinky"))

# plo.plotter2d((uDip_nA[:,:3], uDip_nA[:,3:6], uDip_nA[:,6:9], uDip_nA[:,9:]),
#             ("model: uDip_nA","middle","ring","pinky"))
# plo.plotter2d((uCyl_nA[:,:3], uCyl_nA[:,3:6], uCyl_nA[:,6:9], uCyl_nA[:,9:]),
#             ("model: uCyl_nA","middle","ring","pinky"))
# plo.plotter2d((cDip_nA[:,:3], cDip_nA[:,3:6], cDip_nA[:,6:9], cDip_nA[:,9:]),
#             ("model: cDip_nA","middle","ring","pinky"))
# plo.plotter2d((cCyl_nA[:,:3], cCyl_nA[:,3:6], cCyl_nA[:,6:9], cCyl_nA[:,9:]),
#             ("model: cCyl_nA","middle","ring","pinky"))
# plo.plotter2d((simValues_nA[:,:3], simValues_nA[:,3:6], simValues_nA[:,6:9], simValues_nA[:,9:]),
#             ("model: simValues_nA","middle","ring","pinky"))

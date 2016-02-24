import numpy as np
import modelCyl as modC
import modelDip as modD
import modelCyl_A as modCA
import modelDip_A as modDA
import plotting as plo
import handDim as h
import matplotlib.pyplot as plt
import time
import dataAcquisitionMulti as datAc

def saveSimStates(d,f):
    # add DIP states
    dips = np.zeros((len(d),len(d[0])/3))
    for i in range(0,int(len(d[0])/3)):
        dips[:,i] = (d[:,i*3+1]*(2./3.))
    cnt = 0
    for i in range(2,int(len(d[0])+3),4):
        d = np.insert(d,i,dips[:,cnt],1)
        cnt += 1
    
    datAc.saveStates(f,d)
            

''' comparing different minimization algorithms '''
sInd2 = np.array([-0.02-0.02,  -0.009, 0.030])
sMid2 = np.array([-0.02-0.02,  -0.029, 0.030])
sRin2 = np.array([-0.018-0.02, -0.049, 0.030])
sPin2 = np.array([-0.016-0.02, -0.069, 0.030])

sensList = [h.sInd, h.sMid, h.sRin, h.sPin]
#sensList = [h.sInd, h.sMid, h.sRin, h.sPin,
#            sInd2, sMid2, sRin2, sPin2]
#sensList = [h.sInd, h.sMid]
#sensList = [h.sInd]
#sensList = [h.sPin_car]
#fingList = [h.phalInd, h.phalMid, h.phalRin, h.phalPin]
fingList = [h.phalInd, h.phalMid]
#fingList = [h.phalInd]
#jointList = [h.jointInd, h.jointMid, h.jointRin, h.jointPin]
jointList = [h.jointInd, h.jointMid]
#jointList = [h.jointInd]

folderStr = "../simResults/24/160224/"
fileN = folderStr+"info.txt"
f = open(fileN,'w')

t = np.arange(0.,np.pi/2,0.0085)
a = np.arange(-0.26,0.26,0.0085)

#simValues_A = np.zeros((7*len(t)+2*len(a),3*len(fingList)))
simValues_A = np.zeros((2*len(t),3*len(fingList)))

cnt = 0
#for i in t:
#    simValues_A[cnt] = np.array([i, 0.,0.])     # moving only MCP
##    simValues_A[cnt] = np.array([i, 0.,0.,     # moving only MCP
##                               i, 0. ,0.])#,
##                               i, 0. ,0.,
##                               i, 0. ,0.])
#
#    cnt += 1
#
#for i in t[::-1]:
#    simValues_A[cnt] = np.array([i, 0. ,0.])
##    simValues_A[cnt] = np.array([i, 0. ,0.,     # moving only MCP
##                               i, 0. ,0.])#,
##                               i, 0. ,0.,
##                               i, 0. ,0.])
#    cnt += 1
#
#for i in t:
#    simValues_A[cnt] = np.array([0., i ,0.])
##    simValues_A[cnt] = np.array([0., i ,0.,     # moving only PIP
##                                0., i ,0.])#,
##                                0., i ,0.,
##                                0., i ,0.])
#    cnt += 1
#
#for i in t[::-1]:
#    simValues_A[cnt] = np.array([0., i ,0.])
##    simValues_A[cnt] = np.array([0., i ,0.,     # moving only PIP
##                                0., i ,0.])#,
##                                0., i ,0.,
##                                0., i ,0.])
#    cnt += 1
##
#for i in a:
#    simValues_A[cnt] = np.array([0., abs(i) ,i])
##    simValues_A[cnt] = np.array([0., abs(i) ,i,     # moving only PIP
##                                0., abs(i) ,i])#,
##                                0., abs(i) ,-i,
##                                0., abs(i) ,-i])
#    cnt += 1
#
#for i in a[::-1]:
#    simValues_A[cnt] = np.array([0., abs(i) ,i])
##    simValues_A[cnt] = np.array([0., abs(i) ,i,     # moving only PIP
##                                0., abs(i) ,i])#,
##                                0., abs(i) ,-i,
##                                0., abs(i) ,-i])
#    cnt += 1
#
#for i in t:
#    simValues_A[cnt] = np.array([i, i ,0.])
##    simValues_A[cnt] = np.array([0., 0. ,0.,     # all
##                                i, i ,0.])#,
##                                i, i ,0.,
##                                0., 0. ,0.])
#    cnt += 1
#
#for i in t[::-1]:
#    simValues_A[cnt] = np.array([i, i ,0.])
##    simValues_A[cnt] = np.array([0., 0. ,0.,     # all
##                                i, i ,0.])#,
##                                i, i ,0.,
##                                0., 0. ,0.])
#    cnt += 1
#
#for i in t:
#    simValues_A[cnt] = np.array([i*0.9, i*0.2 ,a[i%11]])
##    simValues_A[cnt] = np.array([i*0.9, i*0.2 ,a[i%11],     # all
##                                i*0.1, i*0.5 ,-a[i%11]])#,
##                                i*0.2, i ,a[i%11],
##                                0., i*0.4 ,-a[i%11]])
#    cnt += 1

for i in t:
#    simValues_A[cnt] = np.array([i*0.5, i,0.])     # moving only MCP
    simValues_A[cnt] = np.array([i*0.5, i, -i*0.1,     # moving only MCP
                               i, i, 0.])#,
#                               i*0.5, i,0.,
#                               i*0.5, i,0.])

    cnt += 1

for i in t[::-1]:
#    simValues_A[cnt] = np.array([i*0.5, i ,0.])
    simValues_A[cnt] = np.array([i*0.5, i, -i*0.1,     # moving only MCP
                               i, i, 0.])#,
#                               i*0.5, i,0.,
#                               i*0.5, i,0.])
    cnt += 1

#plo.plotter2d((simValues_A[:,:3],simValues_A[:,3:6],simValues_A[:,6:9],simValues_A[:,9:]),
#              ("perfect angles index","middle","ring","pinky"))

plo.plotter2d((simValues_A,),("perfect angles",))
plt.savefig(folderStr+"perfectAngles.png")

plt.figure()
simValues = np.delete(simValues_A, np.s_[2],1)
saveSimStates(simValues_A,folderStr+"simStates.txt")

#b_cyl = np.zeros((len(simValues_A),3*len(sensList)))
#b_dip = np.zeros((len(simValues_A),3*len(sensList)))
b_cyl_A = np.zeros((len(simValues_A),3*len(sensList)))
#b_dip_A = np.zeros((len(simValues_A),3*len(sensList)))

#noise = 0.5*np.random.randn(1,12)

for i in range(len(simValues_A)):

#    b_cyl[i] = modC.cy.angToB_cyl(simValues[i],fingList,sensList,jointList) #+ noise
#    b_dip[i] = modD.cy.angToBm_cy(simValues[i],fingList,sensList,jointList) #+ noise

    b_cyl_A[i] = modCA.cy.angToB_cyl(simValues_A[i],fingList,sensList,jointList) #+ noise
#    b_dip_A[i] = modDA.cy.angToBm_cy(simValues_A[i],fingList,sensList,jointList) #+ noise

#plo.plotter2d((b_cyl[:,:3], b_cyl[:,3:6], b_cyl[:,6:9], b_cyl[:,9:]),
#             ("b_cyl_nA index","middle","ring","pinky"))
#plo.plotter2d((b_dip[:,:3], b_dip[:,3:6], b_dip[:,6:9], b_dip[:,9:]),
#             ("b_dip_nA index","middle","ring","pinky"))             
#plo.plotter2d((b_dip_A[:,:3], b_dip_A[:,3:6], b_dip_A[:,6:9], b_dip_A[:,9:]),
#             ("b_dip_A index","middle","ring","pinky"))             
#plo.plotter2d((b_cyl_A[:,:3], b_cyl_A[:,3:6], b_cyl_A[:,6:9], b_cyl_A[:,9:]),
#             ("b_cyl_A index","middle","ring","pinky"))      


#dif = b_dip-b_cyl
#dif_A = b_dip_A-b_cyl_A
#plo.plotter2d((dif[:,:3], dif[:,3:6], dif[:,6:9], dif[:,9:]),
#             ("dif index","middle","ring","pinky"))             
#plo.plotter2d((dif_A[:,:3], dif_A[:,3:6], dif_A[:,6:9], dif_A[:,9:]),
#             ("dif_A index","middle","ring","pinky"))                     




f.write("Start of estimation routine!\n")
for i in range(0,2):
    methString = "METHOD:" + str(i)
    print methString
    f.write(methString + '\n')
    
    ''' dip without ad-ab '''
    startT = time.time()    
    estAng_dip = modD.estimateSeries(b_cyl_A, fingList, sensList, jointList, bnds=True, met=i)
    endT = time.time()-startT
    
    resString = "model: dipole, without adduction-abduction\n"
    resString += "total time[sec] needed: " + str(endT) + "\n"
    resString += "avg time per step[sec]: " + str(endT/len(simValues_A)) + "\n\n"
    # resString += "max fun value: " + str(max(fun_dip)) + "\n\n"
    print resString
    f.write(resString)
    datAc.saveStates(folderStr+"estAng_dip"+str(i), estAng_dip)
    plo.plotter2d((estAng_dip[:,:3], estAng_dip[:,3:6]),
                  ("model: dip without Adduction index","middle"+methString))
#    plo.plotter2d((estAng_dip[:,:3], estAng_dip[:,3:6], estAng_dip[:,6:9], estAng_dip[:,9:]),
#             ("model: dip without Adduction index","middle"+methString,"ring","pinky"))
    plt.savefig(folderStr+str(i)+"dip_nA.png")


    ''' cyl without ad-ab '''
    startT = time.time()
    estAng_cyl = modC.estimateSeries(b_cyl_A, fingList, sensList, jointList, bnds=True, met=i)
    endT = time.time()-startT
    
    resString = "model: cylindrical, without adduction-abduction\n"
    resString += "total time[sec] needed: " + str(endT) + "\n"
    resString += "avg time per step[sec]: " + str(endT/len(simValues_A)) + "\n\n"
    # resString += "max fun value: " + str(max(fun_cyl)) + "\n\n"
    print resString
    f.write(resString)
    datAc.saveStates(folderStr+"estAng_cyl"+str(i), estAng_cyl)
    plo.plotter2d((estAng_cyl[:,:3], estAng_cyl[:,3:6]),
                  ("model: cylindrical without Adduction index","middle"+methString))
#    plo.plotter2d((estAng_cyl[:,:3], estAng_cyl[:,3:6], estAng_cyl[:,6:9], estAng_cyl[:,9:]),
#             ("model: cylindrical without Adduction index","middle"+methString,"ring","pinky"))
    plt.savefig(folderStr+str(i)+"cyl_nA.png")

    ''' dip with ad-ab '''
    startT = time.time()
    estAng_dip_A = modDA.estimateSeries(b_cyl_A, fingList, sensList, jointList, bnds=True, met=i)
    endT = time.time()-startT
    
    resString = "model: dipole, with adduction-abduction\n"
    resString += "total time[sec] needed: " + str(endT) + "\n"
    resString += "avg time per step[sec]: " + str(endT/len(simValues_A)) + "\n\n"
    # resString += "max fun value: " + str(max(fun_dip_A)) + "\n\n"
    print resString
    f.write(resString)
    datAc.saveStates(folderStr+"estAng_dip_A"+str(i), estAng_dip_A)
    plo.plotter2d((estAng_dip_A[:,:4], estAng_dip_A[:,4:8]),
                  ("model: dip with Adduction index","middle"+methString))
#    plo.plotter2d((estAng_dip_A[:,:4], estAng_dip_A[:,4:8], estAng_dip_A[:,8:12], estAng_dip_A[:,12:]),
#             ("model: dip with Adduction index","middle"+methString,"ring","pinky"))
    plt.savefig(folderStr+str(i)+"dip_A.png")
    
    ''' cyl with ad-ab '''
    startT = time.time()
    estAng_cyl_A = modCA.estimateSeries(b_cyl_A, fingList, sensList, jointList, bnds=True, met=i)
    endT = time.time()-startT
    
    resString = "model: cylindrical, with adduction-abduction\n"
    resString += "total time[sec] needed: " + str(endT) + "\n"
    resString += "avg time per step[sec]: " + str(endT/len(simValues_A)) + "\n\n\n"
    # resString += "max fun value: " + str(max(fun_cyl_A)) + "\n\n"
    print resString
    f.write(resString)
    datAc.saveStates(folderStr+"estAng_cyl_A"+str(i), estAng_cyl_A)
    plo.plotter2d((estAng_cyl_A[:,:4], estAng_cyl_A[:,4:8]),
                  ("model: cylindrical with Adduction index","middle"+methString))
#    plo.plotter2d((estAng_cyl_A[:,:4], estAng_cyl_A[:,4:8], estAng_cyl_A[:,8:12], estAng_cyl_A[:,12:]),
#             ("model: cylindrical with Adduction index","middle"+methString,"ring","pinky"))
    plt.savefig(folderStr+str(i)+"cyl_A.png")

    
#    plo.plotter2d((estAng_dip_A, estAng_cyl_A),("dipole_A", "cylindrical_A"), mtitle=methString + "with ad-ab")
#    plt.savefig(folderStr+str(i)+"_A.png")
#    plo.plotter2d((estAng_dip,estAng_cyl), ("dipole","cylindrical"), mtitle=methString + "without ad-ab")
#    plt.savefig(folderStr+str(i)+"_nA.png")

f.close()
plt.show()

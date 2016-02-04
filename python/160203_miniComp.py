import numpy as np
import modelCyl as modC
import modelDip as modD
import modelCyl_A as modCA
import modelDip_A as modDA
import plotting as plo
import handDim as h
import time

''' comparing different minimization algorithms '''

sensList = [h.sInd_car,]
#sensList = [h.sPin_car]
fingList = [h.phalInd]
#fingList = [h.phalInd]
jointList = [h.jointInd_car]

fileN = "comparisonOne.txt"
f = open(fileN,'w')

t = np.arange(0.,np.pi/2,0.1)
a = np.arange(-0.26,0.26,0.05)

simValues_A = np.zeros((7*len(t)+2*len(a),3*len(fingList)))
#simValues_A = np.zeros((2*len(t),3*len(fingList)))

cnt = 0
for i in t:
    simValues_A[cnt] = np.array([i, 0.,0.])#,     # moving only MCP
#                                i, 0. ,0.,
#                                i, 0. ,0.,
#                                i, 0. ,0.])
    cnt += 1

for i in t[::-1]:
    simValues_A[cnt] = np.array([i, 0. ,0.])#,     # moving only MCP
#                                i, 0. ,0.,
#                                i, 0. ,0.,
#                                i, 0. ,0.])
    cnt += 1
    
for i in t:
    simValues_A[cnt] = np.array([0., i ,0.])#,     # moving only PIP
#                                 0., i ,0.,
#                                 0., i ,0.,
#                                 0., i ,0.])
    cnt += 1

for i in t[::-1]:
    simValues_A[cnt] = np.array([0., i ,0.])#,     # moving only PIP
#                                 0., i ,0.,
#                                 0., i ,0.,
#                                 0., i ,0.])
    cnt += 1
    
for i in a:
    simValues_A[cnt] = np.array([0., abs(i) ,i])#,     # moving only PIP
#                                 0., abs(i) ,i,
#                                 0., abs(i) ,-i,
#                                 0., abs(i) ,-i])
    cnt += 1
    
for i in a[::-1]:
    simValues_A[cnt] = np.array([0., abs(i) ,i])#,     # moving only PIP
#                                 0., abs(i) ,i,
#                                 0., abs(i) ,-i,
#                                 0., abs(i) ,-i])
    cnt += 1    
    
for i in t:
    simValues_A[cnt] = np.array([i, i ,0.])#,     # all
#                                 i, i ,0.,
#                                 i, i ,0.,
#                                 i, i ,0.])
    cnt += 1

for i in t[::-1]:
    simValues_A[cnt] = np.array([i, i ,0.])#,     # all
#                                 i, i ,0.,
#                                 i, i ,0.,
#                                 i, i ,0.])
    cnt += 1   
    

for i in t:
    simValues_A[cnt] = np.array([i*0.9, i*0.2 ,a[i%11]])#,     # all
#                                 i*0.1, i*0.5 ,-a[i%11],
#                                 i*0.2, i ,a[i%11],
#                                 0., i*0.4 ,-a[i%11]])
    cnt += 1

#plo.plotter2d((simValues_A[:,:3],simValues_A[:,3:6],simValues_A[:,6:9],simValues_A[:,9:]),
#              ("perfect angles index","middle","ring","pinky"))

#simValues = np.delete(simValues_A,np.s_[2,5,8,11],1)
simValues = np.delete(simValues_A, np.s_[2],1)

b_cyl = np.zeros((len(simValues_A),3*len(sensList)))
b_dip = np.zeros((len(simValues_A),3*len(sensList)))
b_cyl_A = np.zeros((len(simValues_A),3*len(sensList)))
b_dip_A = np.zeros((len(simValues_A),3*len(sensList)))

noise = 0.5*np.random.randn(1,12)

for i in range(len(simValues_A)):
    
    b_cyl[i] = modC.cy.angToB_cyl(simValues[i],fingList,sensList,jointList) #+ noise   
    b_dip[i] = modD.cy.angToBm_cy(simValues[i],fingList,sensList,jointList) #+ noise   
    
    b_cyl_A[i] = modCA.cy.angToB_cyl(simValues_A[i],fingList,sensList,jointList) #+ noise
    b_dip_A[i] = modDA.cy.angToBm_cy(simValues_A[i],fingList,sensList,jointList) #+ noise
    


estAng_dip = np.zeros((len(simValues_A),2*len(sensList)))    
estAng_cyl = np.zeros((len(simValues_A),2*len(sensList)))    
estAng_dip_A = np.zeros((len(simValues_A),3*len(sensList)))    
estAng_cyl_A = np.zeros((len(simValues_A),3*len(sensList)))    

fun_cyl = np.zeros((len(simValues_A),))
fun_dip = np.zeros((len(simValues_A),))
fun_cyl_A = np.zeros((len(simValues_A),))
fun_dip_A = np.zeros((len(simValues_A),))


bnds = ((0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (0.,np.pi/2))
        
bnds_A = ((0.,np.pi/2),
        (0.,np.pi/2),
        (-0.3,0.3),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (-0.3,0.3),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (-0.3,0.3),
        (0.,np.pi/2),
        (0.,np.pi/2),
        (-0.3,0.3))        


f.write("Start of estimation routine!\n")
for i in range(3):
    methString = "METHOD: " + str(i)
    print methString
    f.write(methString + '\n\n')
    startT = time.time()
    for j in range(len(simValues_A[1:])):
        tmp = modD.estimate_BtoAng(estAng_dip[j],fingList, jointList, sensList, b_dip[j+1],bnds[:2],method=i)
        estAng_dip[j+1] = tmp.x        
        fun_dip[j+1] = tmp.fun
    endT = time.time()-startT
    resString = "model: dipole, without adduction-abduction\n"
    resString += "total time[sec] needed: " + str(endT) + "\n"
    resString += "avg time per step[sec]: " + str(endT/len(simValues_A)) + "\n"
    resString += "max fun value: " + str(max(fun_dip)) + "\n\n"
    print resString
    f.write(resString)
    plo.plotter2d((estAng_dip[:,:2], estAng_dip[:,2:4], estAng_dip[:,4:6], estAng_dip[:,6:]),
              ("model: dip without Adduction index","middle"+methString,"ring","pinky"))        
        
    startT = time.time()
    for j in range(len(simValues_A[1:])):
        tmp = modC.estimateAng_cyl(estAng_cyl[j],fingList, jointList, sensList, b_cyl[j+1],bnds[:2],method=i)
        estAng_cyl[j+1] = tmp.x        
        fun_cyl[j+1] = tmp.fun
    endT = time.time()-startT
    resString = "model: cylindrical, without adduction-abduction\n"
    resString += "total time[sec] needed: " + str(endT) + "\n"
    resString += "avg time per step[sec]: " + str(endT/len(simValues_A)) + "\n"
    resString += "max fun value: " + str(max(fun_cyl)) + "\n\n"
    print resString
    f.write(resString)
    plo.plotter2d((estAng_cyl[:,:2], estAng_cyl[:,2:4], estAng_cyl[:,4:6], estAng_cyl[:,6:]),
              ("model: cylindrical without Adduction index","middle"+methString,"ring","pinky"))        

    startT = time.time()
    for j in range(len(simValues_A[1:])):                
        tmp = modDA.estimate_BtoAng(estAng_dip_A[j],fingList, jointList, sensList, b_dip_A[j+1],bnds_A[:3],method=i)
        estAng_dip_A[j+1] = tmp.x        
        fun_dip_A[j+1] = tmp.fun
    endT = time.time()-startT
    resString = "model: dipole, with adduction-abduction\n"
    resString += "total time[sec] needed: " + str(endT) + "\n"
    resString += "avg time per step[sec]: " + str(endT/len(simValues_A)) + "\n"
    resString += "max fun value: " + str(max(fun_dip_A)) + "\n\n"
    print resString
    f.write(resString)
    plo.plotter2d((estAng_dip_A[:,:3], estAng_dip_A[:,3:6], estAng_dip_A[:,6:9], estAng_dip_A[:,9:]),
              ("model: dip with Adduction index","middle"+methString,"ring","pinky"))        
        
    startT = time.time()
    for j in range(len(simValues_A[1:])):        
        tmp = modCA.estimateAng_cyl(estAng_cyl_A[j],fingList, jointList, sensList, b_cyl_A[j+1],bnds_A[:3],method=i)
        estAng_cyl_A[j+1] = tmp.x        
        fun_cyl_A[j+1] = tmp.fun
    endT = time.time()-startT
    resString = "model: cylindrical, with adduction-abduction\n"
    resString += "total time[sec] needed: " + str(endT) + "\n"
    resString += "avg time per step[sec]: " + str(endT/len(simValues_A)) + "\n"
    resString += "max fun value: " + str(max(fun_cyl_A)) + "\n\n"
    print resString    
    f.write(resString)
    plo.plotter2d((estAng_cyl_A[:,:3], estAng_cyl_A[:,3:6], estAng_cyl_A[:,6:9], estAng_cyl_A[:,9:]),
              ("model: cylindrical with Adduction index","middle"+methString,"ring","pinky"))        
        
f.close()        

import dataAcquisitionMulti as datAc
import modelDip as modD
import modelDip_A as modDA
import modelCyl as modC
import modelCyl_A as modCA
import handDim as h
import numpy as np
import plotting as plo
import time

''' for estimating ONE finger with one or multiple sensors, using minimization approach '''

''' simulating data for fitting '''
sensList = [h.sInd,h.sMid,h.sRin,h.sPin]
#sensList = [h.sInd]
#fingList = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
fingList = [h.phalInd]
#jointList = [h.jointInd,h.jointMid,h.jointRin,h.jointRin]
jointList = [h.jointInd]

''' 90deg fitting values '''
t90 = np.arange(0,np.pi/2,0.1)       # describing the angles
#a = np.arange(0,np.pi*(110./180),(np.pi*(110./180))/16)
angles90 = np.zeros((len(t90),3*len(fingList)))
cnt = 0
for i in t90:
    angles90[cnt] = np.array([i, 0., 0.])#,     # moving only MCP
#                            i, 0. ,0.,
#                            i, 0. ,0.,
#                            i, 0. ,0.])
        
    cnt += 1
    
b90 = np.zeros((len(t90), 3*len(sensList)))
b90_A = np.zeros((len(t90), 3*len(sensList)))    

cnt = 0
for i in range(len(t90)):
#    b90[i] = modD.angToBm(angles90[i][:2],fingList,sensList,jointList)    # simulating model without ad-ab
    b90_A[i] = modDA.angToBm(angles90[i],fingList,sensList,jointList)              # simulating model with ad-ab
#    b[i] = modC.angToB_cyl(angles[i][:2],fingList,sensList,jointList)    # simulating model without ad-ab
#    b_A[i] = modCA.angToB_cyl(angles[i],fingList,sensList,jointList)              # simulating model with ad-ab    
    
''' 30deg fitting values '''    
#t30 = np.arange(0,np.pi*(30./180.),0.1)       # describing the angles
#angles30 = np.zeros((len(t30),3*len(fingList)))
#cnt = 0
#for i in t30:
#    angles30[cnt] = np.array([0., 0., -1*i])#,     # moving only MCP
##                            i, 0. ,0.,
##                            i, 0. ,0.,
##                            i, 0. ,0.])
#        
#    cnt += 1    
#    
#b30_A = np.zeros((len(t30), 3*len(sensList)))    
#
#cnt = 0
#for i in range(len(t30)):
#    b30_A[i] = modDA.angToBm(angles30[i],fingList,sensList,jointList)              # simulating model with ad-ab
##    b_A[i] = modCA.angToB_cyl(angles[i],fingList,sensList,jointList)              # simulating model with ad-ab
    
    
    
    
''' fitting measurements '''    
sString = 'set4'
(tim, s1, s2, s3, s4) = datAc.readMag("../datasets/160210/160210_"+sString+"_mag")

print "fitting for 90"
start = 99
end = 185
(scale, off) = datAc.getScaleOff(b90_A[:,:3],s1[start:end]) 
s1_fit = s1*scale+off
plo.plotter2d((b90_A[:,:3], s1_fit[start:end], s1[start:end]),("sim1", "fitted", "meas"),shareAxis=True)

(scale, off) = datAc.getScaleOff(b90_A[:,3:6],s2[start:end]) 
s2_fit = s2*scale+off

(scale, off) = datAc.getScaleOff(b90_A[:,6:9],s3[start:end]) 
s3_fit = s3*scale+off
#plo.plotter2d((b90_A[:,6:9], s3_fit[start:end], s3[start:end]),("sim3", "fitted", "meas"))

(scale, off) = datAc.getScaleOff(b90_A[:,9:],s4[start:end]) 
s4_fit = s4*scale+off
#plo.plotter2d((b90_A[:,9:], s4_fit[start:end], s4[start:end]),("sim4", "fitted", "meas"))

## combining everything again...
s1_fit = np.append(s1_fit,np.append(s2_fit,np.append(s3_fit,s4_fit,1),1),1)
''' fit with prerecorded '''
#(timC, sc1, sc2, sc3, sc4) = datAc.readMag("../datasets/160217/160217_"+'cali3')
#start = 102
#end = 139
#(scale, off) = datAc.getScaleOff(b90_A[:,:3],sc1[start:end]) 
#s1_fit = s1*scale+off
#plo.plotter2d((b90_A[:,:3], s1_fit[start:end], s1[start:end]),("sim1", "fitted", "meas"),shareAxis=False)
#
#(scale, off) = datAc.getScaleOff(b90_A[:,3:6],sc2[start:end]) 
#s2_fit = s2*scale+off
#
#(scale, off) = datAc.getScaleOff(b90_A[:,6:9],sc3[start:end]) 
#s3_fit = s3*scale+off
##plo.plotter2d((b90_A[:,6:9], s3_fit[start:end], s3[start:end]),("sim3", "fitted", "meas"))
#
#(scale, off) = datAc.getScaleOff(b90_A[:,9:],sc4[start:end]) 
#s4_fit = s4*scale+off
##plo.plotter2d((b90_A[:,9:], s4_fit[start:end], s4[start:end]),("sim4", "fitted", "meas"))


''' estimating measurements '''    
startT = time.time()
estAngd_A = modDA.estimateSeries(s1_fit, fingList, sensList, jointList, bnds=True, met=1)
d_A = time.time()-startT
startT = time.time()
estAngd = modD.estimateSeries(s1_fit, fingList, sensList, jointList, bnds=True, met=1)
d = time.time()-startT
startT = time.time()
estAngc_A = modCA.estimateSeries(s1_fit, fingList, sensList, jointList, bnds=True, met=1)    
c_A = time.time()-startT
startT = time.time()       # out, because leads same results as dip and is slower!
estAngc = modC.estimateSeries(s1_fit, fingList, sensList, jointList, bnds=True, met=1)    
c = time.time()-startT
    
print "time d_A: ", d_A    
print "time c_A: ", c_A
#print "time d: ", d
#print "time c: ", c
    
plo.plotLeapVsMag((tim,estAngd_A),(tim,s1,s1_fit[:,:3]),head="estAngd_A vs B-field "+sString)


(timLeap, angInd, angMid, angRin, angPin) = datAc.readLeap("../datasets/160210/160210_"+sString+"_leap")
plo.plotLeapVsMag((timLeap,angInd),(tim,estAngd_A),head="leap state vs estAngd_A "+sString,dif=False)

plo.plotLeapVsMag((tim,estAngd_A),(tim,estAngc_A),head="dip vs cyl ad-ab "+sString,dif=False)
plo.plotLeapVsMag((tim,estAngd),(tim,estAngc),head="dip vs cyl NO ad-ab "+sString,dif=False)

#plo.plotLeapVsMag((tim[257:471],estAngc_A[:,:4],estAngc_A[:,4:8],estAngc_A[:,8:12],estAngc_A[:,12:]),
#                  (tim[257:471],estAngd_A[:,:4],estAngd_A[:,4:8],estAngd_A[:,8:12],estAngd_A[:,12:]),head="cyl vs dip WITH ad-ab "+sString,dif=False)
#plo.plotLeapVsMag((tim[:150],estAngc[:,:4],estAngc[:,4:8],estAngc[:,8:12],estAngc[:,12:]),
#                  (tim[:150],estAngd[:,:4],estAngd[:,4:8],estAngd[:,8:12],estAngd[:,12:]),head="cyl vs dip WITHOUT ad-ab "+sString,dif=False)


#plo.plotLeapVsMag((timLeap,angInd,angMid,angRin,angPin),
#                  (tim,estAng[:,:3],estAng[:,3:6],estAng[:,6:9],estAng[:,9:]),head="leap state vs est "+sString,dif=False)

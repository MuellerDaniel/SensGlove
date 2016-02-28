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
fingList = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
#fingList = [h.phalInd]
jointList = [h.jointInd,h.jointMid,h.jointRin,h.jointRin]
#jointList = [h.jointInd]

''' 90deg fitting values '''
t90 = np.arange(0,np.pi/2,0.1)       # describing the angles
#a = np.arange(0,np.pi*(110./180),(np.pi*(110./180))/16)
angles90 = np.zeros((len(t90),3*len(fingList)))
cnt = 0
for i in t90:
    angles90[cnt] = np.array([i, 0., 0.,     # moving only MCP
                            i, 0. ,0.,
                            i, 0. ,0.,
                            i, 0. ,0.])
        
    cnt += 1
    
b90 = np.zeros((len(t90), 3*len(sensList)))
b90_A = np.zeros((len(t90), 3*len(sensList)))    

cnt = 0
for i in range(len(t90)):
    b90_A[i] = modCA.angToB_cyl(angles90[i],fingList,sensList,jointList)              # simulating model with ad-ab    
    
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
sstring = 'set5'
dayString='160210'

(tim, s1, s2, s3, s4) = datAc.readMag("../datasets/160210/"+dayString+'_'+sstring+"_mag")

print "fitting for 90"
start = 27
end = 57
(scale, off) = datAc.getScaleOff(b90_A[:,:3],s1[start:end]) 
s1_fit = s1*scale+off
#plo.plotter2d((b90_A[:,:3], s1_fit[start:end], s1[start:end]),("sim1", "fitted", "meas"),shareAxis=True)

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
#''' 11 '''
#startT = time.time()
#estAngd_A = modDA.estimateSeries(s1_fit[:,:3], fingList, [sensList[0]], jointList, bnds=True, met=1)
#d_A = time.time()-startT
#print "time d_A11: ", d_A 
#datAc.saveStates("../datasets/niceOnes/"+dayString+'_'+sstring+"dipA11.txt", estAngd_A)
#
#startT = time.time()
#estAngc_A = modCA.estimateSeries(s1_fit[:,:3], fingList, [sensList[0]], jointList, bnds=True, met=1)    
#c_A = time.time()-startT
#datAc.saveStates("../datasets/niceOnes/"+dayString+'_'+sstring+"cylA11.txt", estAngc_A)
#print "time c_A11: ", c_A

#''' 12 '''
#startT = time.time()
#estAngd_A = modDA.estimateSeries(s1_fit[:,:6], fingList, sensList[:2], jointList, bnds=True, met=1)
#d_A = time.time()-startT
#print "time d_A12: ", d_A 
#datAc.saveStates("../datasets/niceOnes/"+dayString+'_'+sstring+"dipA12.txt", estAngd_A)
#
#startT = time.time()
#estAngc_A = modCA.estimateSeries(s1_fit[:,:6], fingList, sensList[:2], jointList, bnds=True, met=1)    
#c_A = time.time()-startT
#datAc.saveStates("../datasets/niceOnes/"+dayString+'_'+sstring+"cylA12.txt", estAngc_A)
#print "time c_A12: ", c_A
#
''' 14 '''
startT = time.time()
estAngd_A = modDA.estimateSeries(s1_fit, fingList, sensList, jointList, bnds=True, met=1)
d_A = time.time()-startT
print "time d_A14: ", d_A 
datAc.saveStates("../datasets/44/"+dayString+'_'+sstring+"dipA44.txt", estAngd_A)

startT = time.time()
estAngc_A = modCA.estimateSeries(s1_fit, fingList, sensList, jointList, bnds=True, met=1)    
c_A = time.time()-startT
datAc.saveStates("../datasets/44/"+dayString+'_'+sstring+"cylA44.txt", estAngc_A)
print "time c_A14: ", c_A

    
plo.plotLeapVsMag((tim,estAngd_A),(tim,s1,s1_fit[:,:3]),head="estAngd_A vs B-field "+sstring)


(timLeap, angInd, angMid, angRin, angPin) = datAc.readLeap("../datasets/160210/"+dayString+'_'+sstring+"_leap" )
#plo.plotLeapVsMag((timLeap,angInd),(tim,estAngd_A),head="leap state vs estAngd_A "+sstring,dif=False)

#plo.plotLeapVsMag((tim,estAngd_A),(tim,estAngc_A),head="dip vs cyl ad-ab "+sstring,dif=False)
#plo.plotLeapVsMag((tim,estAngd),(tim,estAngc),head="dip vs cyl NO ad-ab "+sstring,dif=False)

plo.plotLeapVsMag((timLeap,angInd,angMid,angRin,angPin),
                  (tim,estAngd_A[:,:4],estAngd_A[:,4:8],estAngd_A[:,8:12],estAngd_A[:,12:]),head="estAngd")

plo.plotLeapVsMag((timLeap,angInd,angMid,angRin,angPin),
                  (tim,estAngc_A[:,:4],estAngc_A[:,4:8],estAngc_A[:,8:12],estAngc_A[:,12:]),head="estAngc")
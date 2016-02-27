import dataAcquisitionMulti as datAc
import modelDip as modD
import modelDip_A as modDA
import modelCyl as modC
import modelCyl_A as modCA
import handDim as h
import numpy as np
import plotting as plo
import time
import matplotlib.pyplot as plt
import setFcn as sf

''' for estimating ONE finger with one or multiple sensors, using minimization approach '''

''' simulating data for fitting '''
sensList = [h.sInd,h.sMid,h.sRin,h.sPin]
#sensList = [h.sInd]
#fingList = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
fingList = [h.phalInd]
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
    
b90_A = np.zeros((len(t90), 3*len(sensList)))    

cnt = 0
for i in range(len(t90)):
    b90_A[i] = modCA.angToB_cyl(angles90[i],fingList,sensList,jointList)              # simulating model with ad-ab    


#fi = open("../datasets/evalSets/estResults/160217_real/results.csv","a")
# all the start and end states for the corresponding datasets...
startL = [480,728,99 ,50,   180,40,120,120,120,120,140,130,220,140,110]
endL =   [529,799,185,90,   280,80,180,160,180,160,180,175,300,180,160]

for i in range(4,5,1):      
    sstring = 'set'+str(i)
    
    (tim, s1, s2, s3, s4) = datAc.readMag("../datasets/evalSets/"+sstring+"_mag")
    (tLeap, lInd, lMid, lRin, lPin) = datAc.readLeap("../datasets/evalSets/"+sstring+"_leap")
    lInd_re = sf.resampleLeap((tLeap,lInd),tim)[0]
    
    ''' fitting measurements ''' 
#    print "fitting for 90"
    start = startL[i-1]
    end = endL[i-1]
    (scale, off) = datAc.getScaleOff(b90_A[:,:3],s1[start:end]) 
    s1_fit = s1*scale+off
    
    (scale, off) = datAc.getScaleOff(b90_A[:,3:6],s2[start:end]) 
    s2_fit = s2*scale+off
    
    (scale, off) = datAc.getScaleOff(b90_A[:,6:9],s3[start:end]) 
    s3_fit = s3*scale+off
    
    (scale, off) = datAc.getScaleOff(b90_A[:,9:],s4[start:end]) 
    s4_fit = s4*scale+off
    
    ## combining everything again...
    s1_fit = np.append(s1_fit,np.append(s2_fit,np.append(s3_fit,s4_fit,1),1),1)       
    
    
    ''' estimating measurements '''    
    print "estimating ", sstring
    ''' 11 '''
    print "11"
#    fi.write(sstring+',')
    startT = time.time()
    estAngd_A = modDA.estimateSeries(s1_fit[:,:3], fingList, [sensList[0]], jointList, bnds=True, met=1)
    d_A = time.time()-startT
    d_A /= len(s1_fit)
#    print "time d_A11: ", d_A 
#    fi.write(str(d_A)+',')
    datAc.saveStates("../datasets/evalSets/estResults/160217_real/"+sstring+"_dipA11.txt", estAngd_A)
    (mean_A, var_A) = sf.getMeanVar(lInd_re,estAngd_A)
#    fi.write(str(mean_A)+','+str(var_A)+',')
    print "cyl mean_A %s  var_A %s" % (mean_A, var_A)
    # neglecting ad-ab    
#    (mean, var) = sf.getMeanVar(lInd_re[:,:3], estAngd_A[:,:3])
#    fi.write(str(mean)+','+str(var)+',')
#    print "cyl mean %s  var %s" % (mean, var) 
    
    
    startT = time.time()
    estAngc_A = modCA.estimateSeries(s1_fit[:,:3], fingList, [sensList[0]], jointList, bnds=True, met=1)    
    c_A = time.time()-startT
    c_A /= len(s1_fit)
#    print "time c_A11: ", c_A
#    fi.write(str(c_A)+',') 
    datAc.saveStates("../datasets/evalSets/estResults/160217_real/"+sstring+"_cylA11.txt", estAngc_A)
    (mean_A, var_A) = sf.getMeanVar(lInd_re,estAngc_A)
#    fi.write(str(mean_A)+','+str(var_A)+',')
    print "cyl mean_A %s  var_A %s" % (mean_A, var_A)
#     neglecting ad-ab    
#    (mean, var) = sf.getMeanVar(lInd_re[:,:3], estAngc_A[:,:3])
#    fi.write(str(mean)+','+str(var)+',')  
#    print "dip mean %s  var %s" % (mean, var) 
    
    # plot and save it 
    sf.plotDif(lInd_re,estAngd_A,tim,"dip A11")
    plt.savefig("../datasets/evalSets/difPlots/160217_real/"+sstring+"dipA11.png")
    sf.plotDif(lInd_re,estAngc_A,tim,"cyl A11")
    plt.savefig("../datasets/evalSets/difPlots/160217_real/"+sstring+"dipA11.png")
    
    
    ''' 12 '''
    print "12"
    startT = time.time()
    estAngd_A = modDA.estimateSeries(s1_fit[:,:6], fingList, sensList[:2], jointList, bnds=True, met=1)
    d_A = time.time()-startT
    d_A /= len(s1_fit)
#    print "time d_A12: ", d_A 
#    fi.write(str(d_A)+',')
    datAc.saveStates("../datasets/evalSets/estResults/160217_real/"+sstring+"_dipA12.txt", estAngd_A)
    (mean_A, var_A) = sf.getMeanVar(lInd_re,estAngd_A)
#    fi.write(str(mean_A)+','+str(var_A)+',')
    print "dip mean_A %s  var_A %s" % (mean_A, var_A)  
    # neglecting ad-ab movement
#    (mean, var) = sf.getMeanVar(lInd_re[:,:3], estAngd_A[:,:3])
#    fi.write(str(mean)+','+str(var)+',')
#    print "dip mean %s  var %s" % (mean, var)       
    
    startT = time.time()
    estAngc_A = modCA.estimateSeries(s1_fit[:,:6], fingList, sensList[:2], jointList, bnds=True, met=1)    
    c_A = time.time()-startT
    c_A /= len(s1_fit)
#    print "time c_A12: ", c_A
#    fi.write(str(c_A)+',')
    datAc.saveStates("../datasets/evalSets/estResults/160217_real/"+sstring+"_cylA12.txt", estAngc_A)
    (mean_A, var_A) = sf.getMeanVar(lInd_re,estAngc_A)
#    fi.write(str(mean_A)+','+str(var_A)+',')
    print "cyl mean_A %s  var_A %s" % (mean_A, var_A)        
    # neglecting ad-ab movement
#    (mean, var) = sf.getMeanVar(lInd_re[:,:3], estAngc_A[:,:3])
#    fi.write(str(mean)+','+str(var)+',')    
#    print "cyl mean %s  var %s" % (mean, var)    

    # plot and save it    
    sf.plotDif(lInd_re,estAngd_A,tim,"dip A12")
    plt.savefig("../datasets/evalSets/difPlots/160217_real/"+sstring+"dipA12.png")
    sf.plotDif(lInd_re,estAngc_A,tim,"cyl A12")
    plt.savefig("../datasets/evalSets/difPlots/160217_real/"+sstring+"cylA12.png")
    
    
    ''' 14 '''
    print "14"
    startT = time.time()
    estAngd_A = modDA.estimateSeries(s1_fit, fingList, sensList, jointList, bnds=True, met=1)
    d_A = time.time()-startT
    d_A /= len(s1_fit)
#    print "time d_A14: ", d_A 
#    fi.write(str(d_A)+',')
    datAc.saveStates("../datasets/evalSets/estResults/160217_real/"+sstring+"_dipA14.txt", estAngd_A)
    (mean_A, var_A) = sf.getMeanVar(lInd_re,estAngd_A)
#    fi.write(str(mean_A)+','+str(var_A)+',')
    print "dip mean_A %s  var_A %s" % (mean_A, var_A)    
    # neglecting ad-ab movement
#    (mean, var) = sf.getMeanVar(lInd_re[:,:3], estAngd_A[:,:3])
#    fi.write(str(mean)+','+str(var)+',')
#    print "dip mean %s  var %s" % (mean, var) 
    
    startT = time.time()
    estAngc_A = modCA.estimateSeries(s1_fit, fingList, sensList, jointList, bnds=True, met=1)    
    c_A = time.time()-startT
    c_A /= len(s1_fit)
#    print "time c_A14: ", c_A
#    fi.write(str(c_A)+',')
    datAc.saveStates("../datasets/evalSets/estResults/160217_real/"+sstring+"_cylA14.txt", estAngc_A)
    (mean_A, var_A) = sf.getMeanVar(lInd_re,estAngc_A)
#    fi.write(str(mean_A)+','+str(var_A)+'\n')
    print "cyl mean_A %s  var_A %s" % (mean_A, var_A)    
    # neglecting ad-ab movement    
#    (mean, var) = sf.getMeanVar(lInd_re[:,:3], estAngc_A[:,:3])
#    fi.write(str(mean)+','+str(var)+'\n')  
#    print "cyl mean %s  var %s" % (mean, var) 
    
    # plot and save it    
    sf.plotDif(lInd_re,estAngd_A,tim,"dip A14")
    plt.savefig("../datasets/evalSets/difPlots/160217_real/"+sstring+"dipA14.png")
    sf.plotDif(lInd_re,estAngc_A,tim,"cyl A14")
    plt.savefig("../datasets/evalSets/difPlots/160217_real/"+sstring+"cylA14.png")
    
    plt.close('all')
    
fi.close()    
 
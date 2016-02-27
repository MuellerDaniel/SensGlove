import matplotlib.pyplot as plt
import dataAcquisitionMulti as datAc
import plotting as plo
import numpy as np
import matplotlib.lines as mlines

''' CALCULATING THE MEAN DIFFERENCE AND VAR BETWEEN ESTIMATED AND LEAP
    ALSO PLOTTING IT '''

def resampleLeap_mean(leapData, tMag):
    ''' take the mean of the Leap state values from tMag[i-1] till tMag[i] '''
    tLeap = leapData[0]
    statesLeap = leapData[1:]
    newLeap = ()    # tuple, containing the resampled Leap states    
    
    indexOld = 0   
    for l  in statesLeap:   
        print type(l)
        newLeapStates = np.zeros((len(tMag),4))
        cnt = 0
        
        for i in tMag:    # iterate over all finger state vectors                    
            cond = (tLeap<=i)==1
            indexNew = len(np.extract(cond, tLeap))
            if indexNew == indexOld:
                newLeapStates[cnt] = newLeapStates[cnt-1]
            else:
                for a in range(0,4):            
                    newLeapStates[cnt][a] = np.mean(l[:,a][indexOld:indexNew])            
            indexOld = indexNew
            cnt += 1
            
        newLeap += (newLeapStates,)
    
    return newLeap        
        
        
def resampleLeap_point(leapData, tMag):
    ''' taking the leap state at the time where you are the nearest to the time of the mag data '''
    
    tLeap = leapData[0]
    statesLeap = leapData[1:]
    newLeap = ()    # tuple, containing the resampled Leap states    
    
#    indexOld = 0   
    for l  in statesLeap:   
        print type(l)
        newLeapStates = np.zeros((len(tMag),4))
        cnt = 0
        
        for i in tMag:    # iterate over all finger state vectors                    
            cond = (tLeap<=i)==1
            indexNew = len(np.extract(cond, tLeap))
            newLeapStates[cnt] = l[indexNew]    
#            indexOld = indexNew
            cnt += 1
            
        newLeap += (newLeapStates,)
    
    return newLeap        



def printDif(leap,est, setName):
    
    if len(est[0]) == 3:
        leap = leap[:,:-1]
    
    dif = leap-est
    normedDif = np.linalg.norm(dif, axis=1)    
    print "\n",setName
    print "mean of nomed differences: ", np.mean(normedDif)
    print "standard deviation: ", np.var(normedDif)**2


def plotDif(leap, est, tMag, setName):    
    styleL = ['solid', 'dashed', 'dotted', 'dashdot']
    if len(est[0]) == 3:
        leap = leap[:,:-1]    
    
    plt.figure()    
    
    statesP = plt.subplot(211)
    
    for i in range(0,len(est[0]),1):
        statesP.plot(tMag,leap[:,i],c='r',ls=styleL[i])
        statesP.plot(tMag, est[:,i],c='g', ls=styleL[i])
            
#    statesP.legend()
    statesP.set_ylabel('Angle [rad]')
    statesP.set_title('Difference '+setName)

    
    difP = plt.subplot(212)
    dif = leap-est
    normedDif = np.linalg.norm(dif, axis=1) 
    
    difP.plot(tMag, normedDif, c='g', ls='-')
    
    difP.set_ylabel('Normed Difference [rad]')    
    difP.set_xlabel('Time [sec]')
    

    linePerf = mlines.Line2D([], [], color='r',
                      markersize=15, label='Leap')
    lineEst = mlines.Line2D([], [], color='g',
                      markersize=15, label='Estimated')
    plt.figlegend((linePerf,lineEst),
                  ('Leap','Estimated'), loc='upper right')
                  
               
def plotDif_ind(leap, est, tMag, setName):    
    styleL = ['solid', 'dashed', 'dotted', 'dashdot']
    if len(est[0]) == 3:
        leap = leap[:,:-1]    
    
    plt.figure()    
    
    fMCP = plt.subplot(411)    
    fMCP.plot(tMag,leap[:,0],c='r',ls=styleL[0])
    fMCP.plot(tMag, est[:,0],c='g', ls=styleL[0])
    
    fPIP = plt.subplot(412)
    fPIP.plot(tMag,leap[:,1],c='r',ls=styleL[1])
    fPIP.plot(tMag, est[:,1],c='g', ls=styleL[1])
    fPIP.plot(tMag,leap[:,2],c='r',ls=styleL[2])
    fPIP.plot(tMag, est[:,2],c='g', ls=styleL[2])    
    
    aMCP = plt.subplot(413)
    aMCP.plot(tMag,leap[:,3],c='r', ls=styleL[3])
    aMCP.plot(tMag,est[:,3],c='g', ls=styleL[3])
        
#    statesP.legend()
#    statesP.set_ylabel('Angle [rad]')
#    statesP.set_title('Difference '+setName)

    
    difP = plt.subplot(414)
    dif = leap-est
    normedDif = np.linalg.norm(dif, axis=1) 
    
    difP.plot(tMag, normedDif, c='g', ls='-')
    
    difP.set_ylabel('Normed Difference [rad]')    
    difP.set_xlabel('Time [sec]')
    

    linePerf = mlines.Line2D([], [], color='r',
                      markersize=15, label='Leap')
    lineEst = mlines.Line2D([], [], color='g',
                      markersize=15, label='Estimated')
    plt.figlegend((linePerf,lineEst),
                  ('Leap','Estimated'), loc='upper right')               
    
    
    

#dayString = '160210'
#folderString = "../datasets/niceOnes/"+dayString
sstring = "set4"
#estDA = datAc.readStateFile(folderString+'_'+sstring+"dipA14.txt")
#estCA = datAc.readStateFile(folderString+'_'+sstring+"cylA14.txt")
#(tLeap,lInd,lMid,lRin,lPin) = datAc.readLeap(folderString+'_'+sstring+"_leap")
#(tMag,s1,s2,s3,s4) = datAc.readMag(folderString+'_'+sstring+"_mag")

estCA = datAc.readStateFile("../datasets/evalSets/estResults/160217_real/"+sstring+"_cylA12.txt")
(tLeap,lInd,lMid,lRin,lPin) = datAc.readLeap("../datasets/evalSets/"+sstring+"_leap")
(tMag,s1,s2,s3,s4) = datAc.readMag("../datasets/evalSets/"+sstring+"_mag")

#plo.plotLeapVsMag((tLeap,lInd),(tMag[:-1],estDA[:,:4]),head="states")

#a = resampleLeap_mean((tLeap,lInd), tMag)[0]
#plo.plotLeapVsMag((tLeap,lInd),(tMag,a), head="a")

b = resampleLeap_point((tLeap,lInd), tMag)[0]
#plo.plotLeapVsMag((tLeap,lInd),(tMag,b), head="b")

#diff = b - estDA
plt.close('all')

b = b[:-1]
tMag = tMag[:-1]
# disregarding the ad-ab states...
#estDA = estDA[:,:-1]
#estCA = estCA[:,:-1]

#plotDif(b,estDA, tMag, 'estDA')
#plt.savefig("../datasets/niceOnes/dipA14_plot.png")
#printDif(b, estDA, 'estDA')

plotDif_ind(b,estCA, tMag, 'estCA')
#plt.savefig("../datasets/niceOnes/cylA14_plot.png")
#printDif(b, estCA, 'estCA')







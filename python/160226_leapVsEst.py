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
    
#    for i in range(0,len(est[0]),1):
    for i in range(0,1,4):
        statesP.plot(tMag,leap[:,i],c='r',ls=styleL[i])
        statesP.plot(tMag, est[:,i],c='g', ls=styleL[i])
            
#    statesP.legend()
    statesP.set_ylabel('Angle [rad]')
    statesP.set_title('Difference '+setName)

    
    difP = plt.subplot(212)
    dif = leap-est[:,:4]
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
    
    dif = leap-est
    normed = np.linalg.norm(dif,axis=1)
    mean = np.mean(normed)
    std = np.var(normed)**2
#    mean = np.mean(dif,axis=0)    
#    std = np.var(dif, axis=0)**2
    
    print "mean: %s +- %s" % (mean,std)
    
    
    
#    ##Direct input
#    plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
#    #Options
#    params = {'text.usetex' : True,
#             'font.size' : 11,
#             'font.family' : 'lmodern',
#             'text.latex.unicode': True
##             'figure.autolayout': True
#             }
#    plt.rcParams.update(params)
#    
#    figHeight = 5
#    figWidth = 6
#    
#    plt.figure(figsize=(figWidth,figHeight),dpi=300)   
    plt.figure()
    
    
    styleL = ['solid', 'dashed', 'dotted', 'dashdot']
    if len(est[0]) == 3:
        leap = leap[:,:-1]    
    
    fMCP = plt.subplot(411)    
    fMCP.plot(tMag,leap[:,0],c='r',ls=styleL[0])
    fMCP.plot(tMag, est[:,0],c='g', ls=styleL[0])
    fMCP.set_ylabel(r'$\theta_{MCP}$ [rad]')
    plt.setp(fMCP.get_xticklabels(), visible=False)    
    
    fPIP = plt.subplot(412, sharey=fMCP, sharex=fMCP)
    fPIP.plot(tMag,leap[:,1],c='r',ls=styleL[0])
    fPIP.plot(tMag, est[:,1],c='g', ls=styleL[0])
    fPIP.plot(tMag,leap[:,2],c='r',ls=styleL[1])
    fPIP.plot(tMag, est[:,2],c='g', ls=styleL[1])   
    fPIP.set_ylabel(r'$\theta_{PIP}$\\ \, $\theta_{DIP}$ [rad]')
    plt.setp(fPIP.get_xticklabels(), visible=False)    
    
    aMCP = plt.subplot(413, sharey=fMCP, sharex=fMCP)
    aMCP.plot(tMag,leap[:,3],c='r', ls=styleL[0])
    aMCP.plot(tMag,est[:,3],c='g', ls=styleL[0])
    aMCP.set_ylabel(r'$\phi_{MCP}$ [rad]')
    plt.setp(aMCP.get_xticklabels(), visible=False)    
        
    fMCP.set_title('Difference '+setName)

    
    difP = plt.subplot(414, sharey=fMCP, sharex=fMCP)
    dif = leap-est
    normedDif = np.linalg.norm(dif, axis=1) 
    
    difP.plot(tMag, normedDif, c='k', ls='-')
    
    difP.set_ylabel('Normed\nDifference [rad]')    
    difP.set_xlabel('Time [sec]')
    difP.set
    
    plt.xlim([0,tMag[-1]+1])
    plt.xticks(np.arange(0,tMag[-1],5))

    linePerf = mlines.Line2D([], [], color='r',
                      markersize=15, label='Leap')
    lineEst = mlines.Line2D([], [], color='g',
                      markersize=15, label='Estimated')
    plt.figlegend((linePerf,lineEst),
                  ('Leap','Estimated'), loc='upper center')
#    plt.figlegend((linePerf,lineEst),
#                  ('Leap','Estimated'), loc='upper center', bbox_to_anchor=(0.5,1.04), ncol=2)    
    
                  
#    plt.savefig("../thesis/pictures/plots/bestEst.png", dpi=300, bbox_inches='tight')                  
    
 
 
def plotMulti(leap,mag,time):
    ''' plot only flex-ext of MCP '''
    
    colorL = ['red', 'green', 'blue','yellow']
    a = plt.subplot(211)
    state = 0
    for i in range(0,len(leap),1):
        a.plot(time,leap[i][:,state],c=colorL[i],ls='-')
        a.plot(time,mag[:,i*4+state],c=colorL[i],ls='--')
        
    dif = plt.subplot(212)
    state = 1
    for i in range(0,len(leap),1):
        dif.plot(time,leap[i][:,state],c=colorL[i],ls='-')
        dif.plot(time,mag[:,i*4+state],c=colorL[i],ls='--')        
        
        
    lineInd = mlines.Line2D([], [], color='r',
                      markersize=15, label='Index')
    lineMid = mlines.Line2D([], [], color='g',
                      markersize=15, label='Middle')

    lineLeap = mlines.Line2D([], [], color='k', linestyle='-',
                      markersize=15, label='Leap')
    lineEst = mlines.Line2D([], [], color='k', linestyle='--',
                      markersize=15, label='Estimated')                      
    
    plt.figlegend((lineInd,lineMid, lineLeap, lineEst),
                  ('Index','Middle', 'Leap', 'Estimated'), loc='upper center', ncol=2)        
        
        

def plotNormed(leap,mag,time):
    
        ##Direct input
    plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
    #Options
    params = {'text.usetex' : True,
             'font.size' : 11,
             'font.family' : 'lmodern',
             'text.latex.unicode': True
#             'figure.autolayout': True
             }
    plt.rcParams.update(params)
    
    figHeight = 3.5
    figWidth = 3.5
    
    plt.figure(figsize=(figWidth,figHeight),dpi=300)   
    
    colorL = ['red', 'green', 'blue','yellow']
    ind = plt.subplot(211)
    mid = plt.subplot(212,sharex=ind, sharey=ind)
    
    ind.plot(time, leap[0],c=colorL[0],ls='-')    
    ind.plot(time, mag[0],c=colorL[1],ls='-')    
    ind.set_ylabel('Normed states\nindex [rad]')   
    plt.setp(ind.get_xticklabels(), visible=False)  
    
    mid.plot(time, leap[1],c=colorL[0],ls='-')    
    mid.plot(time, mag[1],c=colorL[1],ls='-')
    mid.set_ylabel('Normed states\nmiddle [rad]')    
    mid.set_xlabel('Time [sec]')    
    
    ind.set_xticks(np.arange(0,time[-1],5))
    
    plt.subplots_adjust(hspace=0.1)
    
    plt.xlim([0,tMag[642]])
    
    ''' shade regions of interest '''
#    # MCP movement  set6_cut 6s
#    a = 3.1
#    b = 9.1
#    ind.axvspan(a,b,color='y', alpha=0.4, lw=0)
#    mid.axvspan(a,b,color='y', alpha=0.4, lw=0)
#    
#    # Fist set6_cut 6s
#    a = 11
#    b = 17
#    ind.axvspan(a,b,color='y', alpha=0.4, lw=0)
#    mid.axvspan(a,b,color='y', alpha=0.4, lw=0)
#    
#    # Index set6_cut 6s
#    a = 19
#    b = 22.2
#    ind.axvspan(a,b,color='y', alpha=0.4, lw=0)
#    mid.axvspan(a,b,color='y', alpha=0.4, lw=0)
#    
#    # Middle set6_cut 6s
#    a = 23.5
#    b = 25.5
#    ind.axvspan(a,b,color='y', alpha=0.4, lw=0)
#    mid.axvspan(a,b,color='y', alpha=0.4, lw=0)
    


    lineLeap = mlines.Line2D([], [], color='r', linestyle='-',
                      markersize=15, label='Leap')
    lineEst = mlines.Line2D([], [], color='g', linestyle='-',
                      markersize=15, label='Estimated')                      
    
    plt.figlegend((lineLeap, lineEst),
                  ('Leap', 'Estimated'), loc='upper center', ncol=2)       
                  
    plt.savefig("../thesis/pictures/plots/est44.png", dpi=300, bbox_to_anchor=(0.5,0.9), bbox_inches='tight')               
                  
 
def verifyDIPPIP(d):
    q = np.zeros((len(d),))
    
    for i in range(0,len(d)):
        q[i] = d[i][1]/d[i][2]
        
    return q        
    

plt.close('all')

''' for plotting best result '''
#sstring = "set4"
#estCA = datAc.readStateFile("../datasets/evalSets/estResults/160217_real/"+sstring+"_cylA12.txt")
#(tLeap,lInd,lMid,lRin,lPin) = datAc.readLeap("../datasets/evalSets/"+sstring+"_leap")
#(tMag,s1,s2,s3,s4) = datAc.readMag("../datasets/evalSets/"+sstring+"_mag")
#b = resampleLeap_point((tLeap,lInd), tMag)[0]
#b = b[:-1]
#tMag = tMag[:-1]
#plotDif_ind(b,estCA, tMag, 'estCA 14')

''' for plotting least best result '''
#sstring = "set5"
#estCA = datAc.readStateFile("../datasets/evalSets/estResults/160226_real/"+sstring+"_cylA14.txt")
#(tLeap,lInd,lMid,lRin,lPin) = datAc.readLeap("../datasets/evalSets/"+sstring+"_leap")
#(tMag,s1,s2,s3,s4) = datAc.readMag("../datasets/evalSets/"+sstring+"_mag")
#b = resampleLeap_point((tLeap,lInd), tMag)[0]
#b = b[:-1]
#tMag = tMag[:-1]
#plotDif_ind(b,estCA, tMag, 'estCA')
#plotDif(b,estCA, tMag, 'estCA')

''' for plotting 44 estimation... '''
sstring = "set6"
estCA = datAc.readStateFile("../datasets/44/160210_"+sstring+"cylA44.txt")
(tLeap,lInd,lMid,lRin,lPin) = datAc.readLeap("../datasets/160210/160210_"+sstring+"_leap")
(tMag,s1,s2,s3,s4) = datAc.readMag("../datasets/160210/160210_"+sstring+"_mag")
(indRe, midRe, rinRe, pinRe) = resampleLeap_point((tLeap, lInd, lMid, lRin, lPin), tMag)

tMag = tMag[:-1]
#plotDif_ind(indRe[:-1],estCA[:,:4], tMag, 'estCA Index')
#plotDif_ind(rinRe[:-1],estCA[:,4:8], tMag, 'estCA Middle')
#plotDif_ind(midRe[:-1],estCA[:,8:12], tMag, 'estCA Ring')
#plotDif_ind(pinRe[:-1],estCA[:,12:], tMag, 'estCA Pinky')
#plotMulti([indRe[:-1],midRe[:-1]],estCA,tMag)

lIndN = np.linalg.norm(indRe,axis=1)
lMidN = np.linalg.norm(midRe,axis=1)
lRinN = np.linalg.norm(rinRe,axis=1)
lPinN = np.linalg.norm(pinRe,axis=1)

mIndN = np.linalg.norm(estCA[:,:4],axis=1)
mMidN = np.linalg.norm(estCA[:,4:8],axis=1)
mRinN = np.linalg.norm(estCA[:,8:12],axis=1)
mPinN = np.linalg.norm(estCA[:,12:],axis=1)

plotNormed((lIndN[:-1],lMidN[:-1],lRinN[:-1],lPinN[:-1]),(mIndN,mMidN,mRinN,mPinN),tMag)






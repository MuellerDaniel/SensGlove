import matplotlib.pyplot as plt
import dataAcquisitionMulti as datAc
import plotting as plo
import numpy as np
import matplotlib.lines as mlines
from matplotlib.image import BboxImage,imread
from matplotlib.transforms import Bbox


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







def plotDif_ind(leap, est, tMag, setName):    
    
    dif = leap-est
    normed = np.linalg.norm(dif,axis=1)
    mean = np.mean(normed)
    std = np.var(normed)**2
#    mean = np.mean(dif,axis=0)    
#    std = np.var(dif, axis=0)**2
    
    print "mean: %s +- %s" % (mean,std)
    
    
    
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
#    
    figHeight = 5
    figWidth = 6
#    
    fig = plt.figure(figsize=(figWidth,figHeight),dpi=300)   
#    plt.figure()
    
    ax = fig.add_axes([0,0,figWidth,figHeight],frameon=False)
#    ax = fig.set_axis_off()    
    
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
    plt.setp(aMCP.get_xticklabels(), visible=True)    
        
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
    
    ''' adding the pictures... '''
    TICKYPOS = -.75
    difP.get_xaxis().set_ticklabels([])
    
#    lowerCorner = difP.transData.transform((.8,TICKYPOS-.2))
#    upperCorner = difP.transData.transform((1.2,TICKYPOS+.2))
    lowPos = [-1.6,TICKYPOS-1.2]
    upPos = [lowPos[0]+6,lowPos[1]+1.5]
    print lowPos
    print upPos
    lowerCorner = difP.transData.transform((lowPos[0],lowPos[1]))
    upperCorner = difP.transData.transform((upPos[0],upPos[1]))
    
    # first
    bbox_image0 = BboxImage(Bbox([[lowerCorner[0], lowerCorner[1]],
                                 [upperCorner[0], upperCorner[1]]]),
                       norm = None,
                       origin=None,
                       clip_on=False,
                       )   
    bbox_image0.set_data(imread('../thesis/pictures/statePics/bestLeap/out-0.jpg'))
    difP.add_artist(bbox_image0)                       
    # second
    lowC1 = difP.transData.transform((lowPos[0]+6.5,lowPos[1]))
    upC1 = difP.transData.transform((upPos[0]+6.5,upPos[1]))
    bbox_image1 = BboxImage(Bbox([[lowC1[0], lowC1[1]],
                                 [upC1[0], upC1[1]]]),
                       norm = None,
                       origin=None,
                       clip_on=False,
                       )   
    bbox_image1.set_data(imread('../thesis/pictures/statePics/bestLeap/out-5.jpg'))
    difP.add_artist(bbox_image1)
    
    
                  
    plt.savefig("../thesis/pictures/plots/bestEstTEST.png", dpi=300, bbox_inches='tight')                  
  



plt.close('all')

''' for plotting best result '''
sstring = "set4"
estCA = datAc.readStateFile("../datasets/evalSets/estResults/160217_real/"+sstring+"_cylA12.txt")
(tLeap,lInd,lMid,lRin,lPin) = datAc.readLeap("../datasets/evalSets/"+sstring+"_leap")
(tMag,s1,s2,s3,s4) = datAc.readMag("../datasets/evalSets/"+sstring+"_mag")
b = resampleLeap_point((tLeap,lInd), tMag)[0]
b = b[:-1]
tMag = tMag[:-1]
plotDif_ind(b,estCA, tMag, 'estCA 14')
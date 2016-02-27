import numpy as np
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import matplotlib.lines as mlines



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

def plotDif_sub(inL):
    ''' inL : list
            [perfectStates, estimated1, estimated2, ...] '''

    colorL = ['r','g','b','y']
    styleL = ['solid','dashed','dotted','dashdot']
    titleL = ['Index', 'Middle', 'Ring', 'Pinky']
#    labelL = ['Defined states', 'Estimated states0', 'Estimated states1', 'Estimated states2']
    
    xTime = np.arange(0,4.95,0.05)
    
#    strA = 'a) Comparison of the estimated with\nthe perfect states and the normed\ndifferences for each time step. The underlying estimation is done\nfor N=1, K=1, using the cylindrical model with constraints and phiMCP'    
#    strB = 'b) Comparison of the estimated with\nthe perfect states\nand the normed difference for each time step.\nThe underlying estimation is done for N=2, K=1, using the cylindrical model with constraints and phiMCP'    
    
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

    figHeight = 5
    figWidth = 6.2
#
#    fig = plt.figure(figsize=(figWidth,figHeight),dpi=300)
#    tt = plt.subplot(211)
    fig, ax = plt.subplots(2,4, sharex='col', sharey='row',
                           figsize=(figWidth,figHeight), dpi=300)
#    fig, ax = plt.subplots(2,4, sharex='col', sharey='row')
    
    ''' plot of first set '''
    
#    plt.setp(a.get_xticklabels(), visible=False)

    lineMCP, = ax[0][0].plot(np.arange(0,6e-5,16e-1),'k-',label=r'\theta_{MCP}')
    linePIP, = ax[0][0].plot(np.arange(0,6e-5,16e-1),'k--',label=r'\theta_{PIP}')
    lineDIP, = ax[0][0].plot(np.arange(0,6e-5,16e-1),'k:',label=r'\theta_{DIP}')
    linePHI, = ax[0][0].plot(np.arange(0,6e-5,16e-1),'k-.',label=r'\phi_{MCP}')
            
    
    print "inL[0]: ", inL[0].shape
    print "inL[1]: ", inL[1].shape
    ''' plot the perfect states '''    
    for i in range(0,4,1):
        styleCnt = 0                
        print "next"
        for j in range(i*4,i*4+4,1):
            print j            
            ax[0][i].plot(xTime,inL[0][:,j],color=colorL[0],linestyle=styleL[styleCnt])
            ax[0][i].plot(xTime,inL[1][:,j],color=colorL[1],linestyle=styleL[styleCnt])        
            styleCnt += 1

        ax[0][i].set_title(titleL[i])
#        if i > 0:        
#            ax[0][i]
        
    ax[0][0].set_ylabel('System states [rad]')      
    
    ''' plot the difference '''
    cnt = 0
    for i in range(0,16,4):
        simS = inL[0][:,i:i+4]
        estS = inL[1][:,i:i+4]
        difS_n = np.linalg.norm(simS-estS,axis=1)
        
        ax[1][cnt].plot(xTime,difS_n,color=colorL[1],linestyle=styleL[0])
        ax[1][cnt].set_xlabel('Time [sec]')
        cnt += 1
        
    ax[1][0].set_ylabel('Difference, normed [rad]')
        

    linePerf = mlines.Line2D([], [], color=colorL[0],
                      markersize=15, label='Perfect States')
    lineEst = mlines.Line2D([], [], color=colorL[1],
                      markersize=15, label='Estimated States')

    

    plt.figlegend((lineMCP,linePIP,lineDIP,linePHI,linePerf,lineEst),
                    (r'$\theta_{MCP}$',r'$\theta_{PIP}$',r'$\theta_{DIP}$',r'$\phi_{MCP}$', 'Perfect States', 'Estimated States'),
                    loc='center right',bbox_to_anchor=(0.9,1.05), ncol=3)

#    plt.subplots_adjust(top=0.8)    
    
    plt.savefig("../thesis/pictures/plots/difMult.png", dpi=300, bbox_inches='tight')
    return fig



folderStr = "../simResults/44/160224/"
simValues = datAc.readStateFile(folderStr+"simStates.txt")
simValues_nA = np.delete(simValues, np.s_[3],1)
simValues_nA = np.delete(simValues_nA, np.s_[6],1)
simValues_nA = np.delete(simValues_nA, np.s_[9],1)
simValues_nA = np.delete(simValues_nA, np.s_[12],1)

cCyl_A44 = datAc.readStateFile(folderStr+"estAng_cyl_A0")
#cCyl_A44 = addDip(cCyl_A44t)

#cCyl_nA12 = datAc.readStateFile("../simResults/12/160224/"+"estAng_cyl1")

plt.close('all')
pl = plotDif_sub([simValues, cCyl_A44])

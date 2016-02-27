import numpy as np
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt

plt.close('all')

folderStr = "../simResults/44/160224/"
simValues = datAc.readStateFile(folderStr+"simStates.txt")
xTime = np.arange(0,4.95,0.05)
#simValues_nA = np.delete(simValues, np.s_[-1],1)
# plo.plotter2d((simValues,),("perfect",))
# plt.close('all')

##Direct input
plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
#Options
params = {'text.usetex' : True,
         'font.size' : 11,
         'font.family' : 'lmodern',
         'text.latex.unicode': True
#         'figure.autolayout': True
         }
plt.rcParams.update(params)

figHeight = 5
figWidth = 6.2

colorL = ['r','g','b','y']
styleL = ['solid','dashed','dotted','dash-dot']
cnt = 0
fig,ax = plt.subplots(3,4, sharex='col', sharey='row',
                        figsize=(figWidth,figHeight),dpi=300)
for i in range(0,4,1):
    ax[0][i].plot(xTime, simValues[:,i*4],color=colorL[cnt], linestyle='-')
    if i == 0:
        ax[0][i].set_ylabel(r'$\theta_{MCP}$ [rad]')
    # plt.setp(a.get_xticklabels(), visible=False)
    # a.legend(loc='upper right', bbox_to_anchor=(legX,legY))

    ax[1][i].plot(xTime, simValues[:,i*4+1],color=colorL[i],linestyle='--')
    ax[1][i].plot(xTime, simValues[:,i*4+2],color=colorL[i],linestyle=':')
    if i == 0:
        ax[1][i].set_ylabel(r'$\theta_{PIP},\, \theta_{DIP}$ [rad]')
    # plt.setp(b.get_xticklabels(), visible=False)
    # b.legend(loc='upper right', bbox_to_anchor=(legX,legY))

    ax[2][i].plot(xTime, simValues[:,i*4+3],color=colorL[i],linestyle='-.')
    if i == 0:
        ax[2][i].set_ylabel(r'$\phi_{MCP}$ [rad]')
    ax[2][i].set_xlabel('Time [sec]')
    # c.legend(loc='upper right', bbox_to_anchor=(legX,legY))

    cnt += 1

lineInd, = ax[1][0].plot(np.arange(0,6e-5,16e-1),'r-',label='Index')
lineMid, = ax[1][1].plot(np.arange(0,6e-5,16e-1),'g-',label='Middle')
lineRin, = ax[1][2].plot(np.arange(0,6e-5,16e-1),'b-',label='Ring')
linePin, = ax[1][3].plot(np.arange(0,6e-5,16e-1),'y-',label='Pinky')

fig.legend([lineInd, lineMid, lineRin, linePin],
            ['Index', 'Middle', 'Ring', 'Pinky'],  ncol=4, loc='center right', bbox_to_anchor=(0.95,1))
            
#plt.subplots_adjust(top=0.8)      
#plt.tight_layout(pad=3)

plt.savefig("../thesis/pictures/plots/multiStates.png", dpi=300, bbox_inches='tight')

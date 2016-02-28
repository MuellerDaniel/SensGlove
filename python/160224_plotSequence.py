import numpy as np
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt

folderStr = "../simResults/11/160224/"
simValues = datAc.readStateFile(folderStr+"simStates.txt")
xTime = np.arange(0,70.9,0.05)
#simValues_nA = np.delete(simValues, np.s_[-1],1)
#plo.plotter2d((simValues,),("perfect",))
plt.close('all')

##Direct input
plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
#Options
params = {'text.usetex' : True,
         'font.size' : 11,
         'font.family' : 'lmodern',
         'text.latex.unicode': True,
         'figure.autolayout': True
         }
plt.rcParams.update(params)

figHeight = 4
figWidth = 5
legX = 1.3
legY = 1
fig = plt.figure(figsize=(figWidth,figHeight),dpi=300)
# fig = plt.figure(dpi=100)

a = plt.subplot(311)
plt.axis((xTime[0],xTime[-1], min(simValues[:,3]), 1.6))
a.plot(xTime, simValues[:,0],'r-',label=r'$\theta_{MCP}$')
a.set_ylabel(r'$\theta_{MCP}$ [rad]')
#a.set_ylabel('Angle [rad]')
# a.set_xlabel('Data point')
plt.setp(a.get_xticklabels(), visible=False)
#a.legend(loc='upper right', bbox_to_anchor=(legX,legY))

b = plt.subplot(312, sharex=a, sharey=a)
b.plot(xTime, simValues[:,1],'r-',label=r'$\theta_{PIP}$')
b.plot(xTime, simValues[:,2],'r--',label=r'$\theta_{DIP}$')
b.set_ylabel(r'$\theta_{PIP},\, \theta_{DIP}$ [rad]')
#b.set_ylabel('Angle [rad]')
# b.set_xlabel('Data point')
plt.setp(b.get_xticklabels(), visible=False)
#b.legend(loc='upper right', bbox_to_anchor=(legX,legY))

c = plt.subplot(313, sharex=a, sharey=a)
c.plot(xTime, simValues[:,3],'r-',label=r'$\phi_{MCP}$')
c.set_ylabel(r'$\phi_{MCP}$ [rad]')
#c.set_ylabel('Angle [rad]')
c.set_xlabel('Time [sec]')
#c.legend(loc='upper right', bbox_to_anchor=(legX,legY))
# plt.show()
plt.savefig("../thesis/pictures/plots/indexStates.png", dpi=300, bbox_inches='tight')

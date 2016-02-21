import numpy as np
import modelDip as modD
import modelCyl as modC
import plotting as plo
import matplotlib.pyplot as plt
import dataAcquisitionMulti as datAc



dP = datAc.textAcquisition("160215_clipPos")[0]*1e-4
dN = datAc.textAcquisition("160215_clipNeg")[0]*1e-4



#dP -= np.mean(dP[:,0][:20])
#dN -= np.mean(dN[:,0][:15])

dP = dP[20:] *[1.,0.,0.]
dN = dN[15:] *[1.,0.,0.]   

start = 7.1
stopP = 2.0625
rPos = np.arange(stopP,start,((start-stopP)/len(dP)))[::-1]
stopN = 1.4528
rNeg = np.arange(stopN,start,((start-stopN)/len(dN)))[::-1]
tP = rPos
tN = rNeg
#tP = np.arange(0.03,0.07,(0.03/95))[::-1]
#tN = np.arange(0.04,0.07,(0.03/70))[::-1]
bP = np.zeros((len(tP),3))
bN = np.zeros((len(tN),3))

cnt = 0
for i in tP:
    bP[cnt] = modC.calcB_cyl(np.array([abs(i)*1e-2+(0.015/2),0.,0.]), 0.)
    cnt += 1
    
cnt = 0    
for i in tN:
    bN[cnt] = modC.calcB_cyl(np.array([abs(i)*1e-2+(0.015/2),0.,0.]), np.pi)
    cnt += 1    

dP += bP[0][0]-dP[0][0]  #0.0001602
dN += bN[0][0]-dN[0][0] #0.0001145

''' plotting only measured '''

plt.close('all')

#Direct input 
plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
#Options

params = {'text.usetex' : True,
          'font.size' : 11,
          'font.family' : 'lmodern',
          'text.latex.unicode': True,
          'figure.autolayout': True
          }
plt.rcParams.update(params) 

## WORKS!
figHeight = 2
figWidth = 3
fig = plt.figure(figsize=(figWidth,figHeight),dpi=500)
#plt.figure()
plt.xlim(rPos[0],rPos[-1])
#plt.plot(rPos,bP[:,0]*1e+3,'r--',label='model data')
plt.plot(rPos,dP[:,0],'b-',label='measurement data')
plt.axis([7,rPos[-1],-0.8,0.6])
plt.grid(True)
plt.xlabel(r'$\Delta d$ [cm]')
plt.ylabel('B-field [mT]')
#plt.title('positive clipping')
#plt.legend()
plt.savefig("../thesis/pictures/plots/posClipping.png", dpi=500 ,format='png')

fig = plt.figure(figsize=(figWidth,figHeight),dpi=500)
plt.xlim(rNeg[0],rNeg[-1])
#plt.plot(rNeg,bN[:,0]*1e+3, 'r--', label='model data')
plt.plot(rNeg,dN[:,0], 'b-', label='measurement data')
plt.axis([7, rNeg[-1], -0.6, 0.6])
plt.grid(True)
plt.xlabel(r'$\Delta d$ [cm]')
plt.ylabel('B-field [mT]')
#plt.title('negative clipping')
plt.savefig("../thesis/pictures/plots/negClipping.png", dpi=500)



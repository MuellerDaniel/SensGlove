import subprocess
import dataAcquisitionMulti as datAc
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import plotting as plo

''' data acquistion '''
#bleCmd = "gatttool -t random -b E7:00:30:16:CD:18 --char-write-req --handle=0x000f --value=0100 --listen"
#
#proc = subprocess.Popen(bleCmd.split(), stdout=subprocess.PIPE, close_fds=True)
#
#m = np.zeros((4,4))
#
#
##t = np.zeros((1,))
#cnt = 0
#try:
##    startT = time.time()
##    while time.time()-startT < 10:
##    while True:
#    for i in range(500):
#        print "nr of meas: ",cnt
##        print time.time()-startT
##        startT = time.time()
#        m = np.append(m,datAc.readMagPacket(proc),0)        
##        t = np.append(t,time.time()-startT)
#        cnt += 1
#
#except KeyboardInterrupt:
#    pass
#
#proc.kill()
#datAc.saveToFile(m,"160217_MPU_mag")
#d = datAc.sortData(m)

''' take the datapoints for 160217_MPU2 from [300:-1] (for sensor 0 or 1) and display them reversed '''

d = datAc.textAcquisition("160217_MPU2")
oneC = d[0][300:][::-1]
twoC = d[1][300:][::-1]
oneR = d[2][300:][::-1]
twoR = d[3][300:][::-1]
''' plot everything... '''

plt.close('all')

#plt.figure()
#plt.plot(oneC[:,0],'r-',label='cancel1')
#plt.plot(oneC[:,1],'r--')
#plt.plot(oneC[:,2],'r:')
#plt.plot(oneR[:,0],'b-',label='raw1')
#plt.plot(oneR[:,1],'b--')
#plt.plot(oneR[:,2],'b:')
#plt.legend()
#plt.title('unit 1')

con = 1e-4

#plt.figure()
#normR = np.linalg.norm(twoR*con,axis=1)
#normC = np.linalg.norm(twoC*con, axis=1)
#plt.plot(normR,color='y')
#plt.plot(normC,color='g')

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

figHeight = 4
figWidth = 4
fig = plt.figure(figsize=(figWidth,figHeight),dpi=300)
#fig = plt.figure()
ax = plt.subplot(212)

sX, = ax.plot(np.arange(0,6e-5,16e-1),'k-',label='x')
sY, = ax.plot(np.arange(0,6e-5,16e-1),'k--',label='y')
sZ, = ax.plot(np.arange(0,6e-5,16e-1),'k:',label='z')

ax.plot(twoC[:,0]*con,'r-',label='With cancellation')
ax.plot(twoC[:,1]*con,'r--')
ax.plot(twoC[:,2]*con,'r:')
ax.plot(twoR[:,0]*con,'g-',label='Raw')
ax.plot(twoR[:,1]*con,'g--')
ax.plot(twoR[:,2]*con,'g:')
ax.set_xlabel('Measurement number')
ax.set_ylabel('B-field [mT]')

# 20 143
ax.axvline(x=20)
ax.axvline(x=143)

textY = 0.064
ax.annotate('initial\norientation', xy=(10, 0.02), xytext=(170, textY),
                arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"))
ax.annotate("",xy=(170, 0.02), xytext=(170,textY),
                arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"))     
                            
ax.annotate('rotated\norientation', xy=(40, 0.04), xytext=(25, textY),
                arrowprops=dict(arrowstyle="->",
                            connectionstyle="arc3"))                            


#plt.title('unit 2')
ax.legend(loc='upper center',ncol=2,bbox_to_anchor=(0.5,1.85))
plt.savefig("../thesis/pictures/plots/earthCanc.png", dpi=300, bbox_inches='tight')


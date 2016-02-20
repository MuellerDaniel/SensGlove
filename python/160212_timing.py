import subprocess
import dataAcquisitionMulti as datAc
import time
import numpy as np
import matplotlib.pyplot as plt
import plotting as plo

''' acquiring the data live! '''
#bleCmd = "gatttool -t random -b E7:00:30:16:CD:18 --char-write-req --handle=0x000f --value=0100 --listen"
#bleCmd = "gatttool -t random -b D7:54:04:52:37:2A --char-write-req --handle=0x000f --value=0100 --listen"
#proc = subprocess.Popen(bleCmd.split(), stdout=subprocess.PIPE, close_fds=True)
#t = np.zeros((1,))
#doubleSend = 0
#wrongSend = 0
##m = np.zeros((1,4*3+1))
#m = np.zeros((4,4))
#try:
##    while True:
#    for i in range(0,200):
#        startT = time.time()
#        m = datAc.readMagPacket(proc)
#        t = np.append(t,[time.time()-startT])
#        print "received!"
#
#        
#except KeyboardInterrupt:
#    pass
#proc.kill()        
#
#t = t[1:]

# save to file
#f = open("timeF25.dat",'w')
#for i in t:
#    f.write(str(i) + ' ')

''' plotting stuff '''
f = open("timeF50.dat",'r')
t50 = f.readline().split()
t50 = np.asarray(t50).astype('float')
m50 = np.mean(t50)
var50 = np.var(t50)

f = open("timeF25.dat",'r')
t25 = f.readline().split()
t25 = np.asarray(t25).astype('float')
m25 = np.mean(t25)
var25 = np.var(t25)

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
figWidth = 5
fig = plt.figure(figsize=(figWidth,figHeight),dpi=500)

#bins = ([min(t), 0.05, 0.065, 0.075, 0.1, 0.15, max(t)])
#bins = 10

plt.hist([t50, t25], histtype='bar',rwidth=0.8, label=[r'$f_{Sensor}=50$Hz',r'$f_{Sensor}=25$Hz'])
plt.legend()
plt.text(0.2, 100, r'$\mu_{25Hz}$=0.08s', color='green')
plt.text(0.2, 90, r'$\sigma_{25Hz}$=0.0012', color='green')
plt.text(0.2, 70, r'$\mu_{50Hz}$=0.05s', color='blue')
plt.text(0.2, 60, r'$\sigma_{50Hz}$=0.0014', color='blue')
#plt.xticks(np.arange(0,0.25,0.035))
plt.ylabel(r'Nr of measurements')
plt.xlabel(r'Time for acquisition [s]')
plt.savefig("../thesis/pictures/plots/timingRFd_v2.png", dpi=500)
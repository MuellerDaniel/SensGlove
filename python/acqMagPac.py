import dataAcquisitionMulti as datAc
import matplotlib.pyplot as plt
import plotting as plo
import time,subprocess
import numpy as np

''' simply reads FULL magnetic packages via BLE 
    A full package means, that it starts '''
    
    
bleCmd = "gatttool -t random -b E7:00:30:16:CD:18 --char-write-req --handle=0x000f --value=0100 --listen"    
proc = subprocess.Popen(bleCmd.split(), stdout=subprocess.PIPE, close_fds=True)

m = np.zeros((4,4))    
#t = np.zeros((1,))
cnt = 0
try:
    startT = time.time()
    while time.time()-startT < 10:
#    while True:
#    for i in range(500):
#        print "nr of meas: ",cnt
        print time.time()-startT
#        startT = time.time()
        m = np.append(m,datAc.readMagPacket(proc),0)
#        t = np.append(t,time.time()-startT)
        cnt += 1
        
except KeyboardInterrupt:
    pass
    
proc.kill()    
datAc.saveToFile(m,"160205_magData") 

d = datAc.sortData(m)
plo.plotter2d((d[0],d[1],d[2],d[3]),("1","2","3","4"))
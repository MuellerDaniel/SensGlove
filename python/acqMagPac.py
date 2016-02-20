import dataAcquisitionMulti as datAc
import matplotlib.pyplot as plt
import plotting as plo
import time,subprocess
import numpy as np
import sys,signal, select


def saveToFile(data,f):
    fil = open(f,'w')
    for i in data:
        for j in i:
            fil.write(str(j) + '\t')
        fil.write('\n')

''' routine for recognizing the sigint '''
def cleanup(signum, frame):
    print "acqMagPac end..."
    proc.kill()
#    m = m[8:]
#    for i in frame.f_globals:
#        print i
#    print type(frame)
#    datAc.saveToFile(m[8:],"160209_mag")
    saveToFile(m[1:],"160217_mag")
    sys.exit()



''' simply reads FULL magnetic packages via BLE
    A full package means, that it starts '''


bleCmd = "gatttool -t random -b E7:00:30:16:CD:18 --char-write-req --handle=0x000f --value=0100 --listen"
proc = subprocess.Popen(bleCmd.split(), stdout=subprocess.PIPE, close_fds=True)

m = np.zeros((1,4*3+1))

signal.signal(signal.SIGINT, cleanup)
timOut = 1
t = np.zeros((1,))
cnt = 0
try:
    
#    startT = time.time()
#    while time.time()-startT < 10:
    while True:
#    for i in range(500):
#        print "nr of meas: ",cnt
#        print time.time()-startT
#        startT = time.time()
#        print datAc.readMagPacket(proc,sensStamp=False)
        
        m = np.append(m,[np.concatenate(([time.time()],datAc.readMagPacket(proc,sensStamp=False).flatten()*1e-7))],0)
        print "MAG\t\tup!"
        cnt += 1
        

except KeyboardInterrupt:
    pass


#m = m[8:]
#proc.kill()
# datAc.saveToFile(m,"160205_magData")

#d = datAc.sortData(m)
#plo.plotter2d((d[0],d[1],d[2],d[3]),("1","2","3","4"))

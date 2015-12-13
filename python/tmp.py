import dataAcquisitionMulti as datAc
import numpy as np
import matplotlib.pyplot as plt

cmd = "gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen"
d = datAc.pipeAcquisition(cmd,1,measNr=200)
#d = datAc.textAcquisition("151210_y5_7_10.txt")

#data = datAc.moving_average3d(d[0],10)
valX = d[0][:,0]*0.00429428
valY = d[0][:,1]*0.00447199
valZ = d[0][:,2]*0

earthX = np.mean(valX)
earthY = np.mean(valY)
earthZ = np.mean(valZ)

print earthX
print earthY
print earthZ

plt.figure()
plt.plot(valX,'r')
plt.plot(valY,'g')
plt.plot(valZ,'b')
plt.title("raw scaled")
plt.figure()
plt.plot(valX-earthX,'r')
plt.plot(valY-earthY,'g')
plt.plot(valZ,'b')
plt.title("scaled and offset")
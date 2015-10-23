import dataAcquisitionMulti as datAc
import numpy as np
import plotting as plo

a = datAc.pipeAcquisition("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen",
                          measNr=4*100)

#plo.plotter2d((a[0:1],a[1:2],a[2:3],a[3:4]),("s0","s1","s2","s3",))   
plo.visMagData(a)
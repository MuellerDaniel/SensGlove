'''
    script for checking the calibrated output of your sensor
    just wave the sensors around
'''

import dataAcquisitionMulti as datAc
import plotting as plo

#data = datAc.pipeAcquisition("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen",
#                             measNr=100)
data = datAc.collectForTime("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen",
                            20)

plo.visMagData(data)                

''' checking the calibration values '''

cnt = 0
for i in data:    
    # check hard iron 
    maxX = max(i[:,0])            
    minX = min(i[:,0])
    offX = (maxX+minX)/2
    maxY = max(i[:,1])            
    minY = min(i[:,1])
    offY = (maxY+minY)/2    
    maxZ = max(i[:,2])            
    minZ = min(i[:,2])
    offZ = (maxZ+minZ)/2
    print "\nhard iron offset sensor " + str(cnt)
    print [offX, offY, offZ]
    
    # check soft iron
    tmpX = (maxX + abs(minX))/2
    tmpY = (maxY + abs(minY))/2
    tmpZ = (maxZ + abs(minZ))/2
    rad = (tmpX+tmpY+tmpZ)/3
    print "soft iron offset sensor " + str(cnt) 
    print [rad/tmpX, rad/tmpY, rad/tmpZ]
    
    cnt += 1
    print "\n"
 
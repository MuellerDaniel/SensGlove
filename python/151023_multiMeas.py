''' script for experimenting with the measured and the modeled B-field '''

import dataAcquisitionMulti as datAc
import numpy as np
import subprocess,time, os
import modelEqMultiCython as modE
import plotting as plo
import matplotlib.pyplot as plt
import perfectBangles as b

cmd = "gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen"
calcB = datAc.textAcquisition("151102_perfectB")

#(d_index,d_middle,d_ring,d_pinky) = datAc.collectForTime(cmd, 10, 0.01, avgFil=False, avgN=10, fileName="151101_rawMeas_move2")
#(d_index,d_middle,d_ring,d_pinky) = datAc.collectForTime(cmd, 20, 0.01, fileName="151102_rawMeas_ovMove")
data = datAc.textAcquisition("151102_rawMeas_move")
(d_index,d_middle,d_ring,d_pinky) = (data[0],data[1],data[2],data[3])

# absolute positions of wooden-joints
#jointInd = [0.09138, 0.02957, -0.01087]         # to wooden-joint(index)
#jointMid = [0.09138, 0.00920, -0.01087]          # to wooden-joint(middle)
#jointRin = [0.09138, -0.01117, -0.01087]         # to wooden-joint(ring)
#jointPin = [0.09138, -0.03154, -0.01087]         # to wooden-joint(pinky)
jointInd = b.jointInd
jointMid = b.jointMid
jointRin = b.jointRin
jointPin = b.jointPin

## position of sensor
#s1 = [0.06755, 0.02957, 0.]     # sensor beneath index
#s2 = [0.04755, 0.00920, 0.]     # sensor beneath middle
#s3 = [0.06755, -0.01117, 0.]    # sensor beneath ring
#s4 = [0.04755, -0.03012, 0.]    # sensor beneath pinky
s1 = b.s1
s2 = b.s2
s3 = b.s3
s4 = b.s4
## lengths of phalanges
#phalInd = [0.03038, 0.02728, 0.02234]
#phalMid = [0.03640, 0.03075, 0.02114]
#phalRin = [0.03344, 0.02782, 0.01853]
#phalPin = [0.02896, 0.02541, 0.01778]
phalInd = b.phalInd
phalRin = b.phalRin
phalMid = b.phalMid
phalPin = b.phalPin


''' data fitting '''
#fitIndex = modE.fitMeasurements(calcB[0],d_index,(0,200))
#fitMiddle = modE.fitMeasurements(calcB[1],d_middle,(0,200))
#fitRing = modE.fitMeasurements(calcB[2],d_ring,(0,200))
#fitPinky = modE.fitMeasurements(calcB[3],d_pinky,(0,200))
#
## neglect the resting data
#fitIndex = fitIndex[200:700]
#fitMiddle = fitMiddle[200:700]
#fitRing = fitRing[200:700]
#fitPinky = fitPinky[200:700]

avgIndex = datAc.moving_average3d(d_index,50)
avgMiddle = datAc.moving_average3d(d_middle,50)
avgRing = datAc.moving_average3d(d_ring,50)
avgPinky = datAc.moving_average3d(d_pinky,50)

''' estimating the angles '''
#estAngInd = np.zeros((len(fitIndex[:,0]),3))
#estAngMid = np.zeros((len(fitIndex[:,0]),3))
#estAngRin = np.zeros((len(fitIndex[:,0]),3))
#estAngPin = np.zeros((len(fitIndex[:,0]),3))
#
#bnds = ((0.0,np.pi/2),    # index
#        (0.0,np.pi/2),
#        (0.0,np.pi/2),
#        (0.0,np.pi/2),    # middle
#        (0.0,np.pi/2),
#        (0.0,np.pi/2),
#        (0.0,np.pi/2),    # ring
#        (0.0,np.pi/2),
#        (0.0,np.pi/2),
#        (0.0,np.pi/2),    # pinky
#        (0.0,np.pi/2),
#        (0.0,np.pi/2))
# 
## piping action...
##mPath = 'estimatedAngles'
##if not os.path.exists(mPath):
##    os.mkfifo(mPath)
##procId = os.getpid()   
##print "starting visualization..."
##vis = subprocess.Popen(('./../visualization/finger_angles/application.linux64/finger_angles '+mPath).split(),shell=False)
##pipeout = file(mPath,"w")
#      
#for i in range(len(estAngInd[1:])):
#    res = modE.estimate_BtoAng(np.concatenate((estAngInd[i], estAngMid[i], estAngRin[i], estAngPin[i])),
#                               [phalInd,phalMid,phalRin,phalPin],
#                                [jointInd,jointMid,jointRin,jointPin],
#                                [s1,s2,s3,s4],
#                                np.concatenate((fitIndex[i+1],fitMiddle[i+1],fitRing[i+1],fitPinky[i+1])),
#                                bnds)
#    
#    print res
#                         
#    estAngInd[i+1] = res.x[0:3]    
#    estAngMid[i+1] = res.x[3:6]    
#    estAngRin[i+1] = res.x[6:9]    
#    estAngPin[i+1] = res.x[9:12]    

#    pipeStr = ''
#    for i in res.x:
#        pipeStr = pipeStr + " {0:.4f}".format(abs(i))
#    # put the angles on the pipe...
#    try:                   #thumb      #index       #middle      #ring        #pinky
#        pipeout.write("0.0000 0.0000 0.0000" + pipeStr)
#        pipeout.flush()
#    except OSError,e:
#        print "error! listener disconnected"
#        os.unlink(mPath)
#        break                            

#plt.close('all')
#plo.plotter2d((d_index,calcB[0],d_middle,calcB[1],d_ring,calcB[2],d_pinky,calcB[3]),
#              ("ind", "calcInd", "mid", "calcMid","rin", "calcRin", "pin", "calcPin"))
plo.plotter2d((calcB[0],calcB[1],calcB[2],calcB[3]),("calc index","calc middle","calc ring","calc pinky"))
plo.plotter2d((d_index,d_middle,d_ring,d_pinky),("meas index","meas middle","meas ring","meas pinky"))
plo.plotter2d((avgIndex,avgMiddle,avgRing,avgPinky),("avg index","avg middle","avg ring","avg pinky"))
#plo.plotter2d((fitIndex,calcB[0]),("measIndex","calcIndex"),shareAxis=True)
#plo.plotter2d((fitMiddle,calcB[1]),("measMiddle","calcMiddle"),shareAxis=True)
#plo.plotter2d((fitRing,calcB[2]),("measRing","calcRing"),shareAxis=True)
#plo.plotter2d((fitPinky,calcB[3]),("measPinky","calcPinky"),shareAxis=True)
#plo.plotter2d((d_index,avgIndex,calcB[0]),("measIndex","avg","calcIndex"),shareAxis=False)
#plo.plotter2d((d_middle,avgMiddle,calcB[1]),("measMiddle","avg","calcMiddle"),shareAxis=False)
#plo.plotter2d((d_ring,avgRing,calcB[2]),("measRing","avg","calcRing"),shareAxis=False)
#plo.plotter2d((d_pinky,avgPinky,calcB[3]),("measPinky","avg","calcPinky"),shareAxis=False)
#plo.plotter2d((estAngInd,estAngMid,estAngRin,estAngPin),("ind", "mid", "rin", "pin"))
import dataAcquisitionMulti as datAc
import numpy as np
import subprocess,time
import modelEqMultiCython as modE
import plotting as plo
import matplotlib.pyplot as plt

cmd = "gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen"
calcB = datAc.textAcquisition("perfectB")

(d_index,d_middle,d_ring,d_pinky) = datAc.collectForTime(cmd, 10, 0.01,avgFil=True,avgN=10)

# calculate the offset, caused by the earth field
#earthOff = np.array([[np.mean(d_index[:,0]), np.mean(d_index[:,1]), np.mean(d_index[:,2])],
#                    [np.mean(d_middle[:,0]), np.mean(d_middle[:,1]), np.mean(d_middle[:,2])],
#                    [np.mean(d_ring[:,0]), np.mean(d_ring[:,1]), np.mean(d_ring[:,2])],
#                    [np.mean(d_pinky[:,0]), np.mean(d_pinky[:,1]), np.mean(d_pinky[:,2])]])
# 151028 the calculated offset
#earthOff = np.array([[-393.19476678, -115.37610922,  117.84605233],
#                   [-405.61448237, -114.97810011,  130.61178612],
#                   [-420.73119454, -109.46814562,  177.76047782],
#                   [-398.89919226,  -96.66159272,  123.86134243]])
#d_index -= earthOff[0]
#d_middle -= earthOff[1]
#d_ring -= earthOff[2]
#d_pinky -= earthOff[3]

# calculate and apply the offset, s.t. you fit the measurements to the calculated B-field
#magOff = np.array([[calcB[0][0][0]-np.mean(d_index[:,0]), calcB[0][0][1]-np.mean(d_index[:,1]), calcB[0][0][2]-np.mean(d_index[:,2])],
#                    [calcB[1][0][0]-np.mean(d_middle[:,0]), calcB[1][0][1]-np.mean(d_middle[:,1]), calcB[1][0][2]-np.mean(d_middle[:,2])],
#                    [calcB[2][0][0]-np.mean(d_ring[:,0]), calcB[2][0][1]-np.mean(d_ring[:,1]), calcB[2][0][2]-np.mean(d_ring[:,2])],
#                    [calcB[3][0][0]-np.mean(d_pinky[:,0]), calcB[3][0][1]-np.mean(d_pinky[:,1]), calcB[3][0][2]-np.mean(d_pinky[:,2])]])
# 151028 the calculated offset
magOff = np.array([[ 1292.83328085,  -220.89194193,  -289.02723504],
                   [ 1036.17817964,    46.28124575,  -213.60249662],
                   [ 1586.63743434,   285.00956206,  -355.03524989],
                   [  955.54294006,   367.8931559 ,  -220.09212326]])

d_index += magOff[0]
d_middle += magOff[1]
d_ring += magOff[2]
d_pinky += magOff[3]

# applying the average filter
#(avg_index,avg_middle,avg_ring,avg_pinky) = datAc.collectForTime(cmd, 5, 0.1,avgFil=True,avgN=5)

plo.plotter2d((d_index,calcB[0],d_middle,calcB[1],d_ring,calcB[2],d_pinky,calcB[3]),("ind", "mid", "rin", "pin","ind", "mid", "rin", "pin"))
#plo.plotter2d((calcB[0],calcB[1],calcB[2],calcB[3]),("ind", "mid", "rin", "pin"))
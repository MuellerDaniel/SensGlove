import numpy as np
import handDim as h
import modelDip as modD
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt


sensList_dip = [h.sInd_car,h.sMid_car,h.sRin_car,h.sPin_car]
fingList_dip = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
#fingList_dip = [h.phalInd,h.phalMid,h.phalRin]
jointList_dip = [h.jointInd_car,h.jointMid_car, h.jointRin_car, h.jointPin_car]
#jointList_dip = [h.jointInd_car,h.jointMid_car,h.jointRin_car]


''' simulation '''
t = np.arange(0,np.pi/2,0.01)       # describing the angles
angles1 = np.zeros((len(t),2*len(fingList_dip)))
angles2 = np.zeros((len(t),2*len(fingList_dip)))
cnt = 0
for i in t:
#    TODO adjust it on the number of fingers you want to measure
    angles1[cnt] = np.array([0., 0.,    # angle index
                             i,  0.,    # angle mid
                             0., 0.,    # angle rin
                             0., 0])   # angle pin

    angles2[cnt] = np.array([0., 0.,    # angle index
                             0.,  0.,    # angle mid
                             i, 0.,    # angle rin
                             0., 0])   # angle pin                             
    
    cnt += 1
    
    
bMid = np.zeros((len(t), 3*len(sensList_dip)))    
bRin = np.zeros((len(t), 3*len(sensList_dip)))    
cnt = 0
for i in range(len(t)):
#    b_cyl[i] = modC.cy.angToB_cyl(angles_cyl[i],fingList_cyl,sensList_cyl,jointList_cyl)    # simulating cylindrical model
    bMid[i] = modD.cy.angToBm_cy(angles1[i],fingList_dip,sensList_dip,jointList_dip)              # simulating dipole model
    bRin[i] = modD.cy.angToBm_cy(angles2[i],fingList_dip,sensList_dip,jointList_dip)              # simulating dipole model
    
    
b_meas = datAc.textAcquisition("160131_allMid2")    
b_meas *= 0.01
print "-----------middle----------"
print "INDEX"    
(scale1, off1) = datAc.getScaleOff(bMid[:,0:3],b_meas[0])    
b_ind = b_meas[0]*scale1+off1
print "MIDDLE"
#(scale2, off2) = datAc.getScaleOff(bMid[:,3:6],b_meas[1])    
#b_mid = b_meas[0]*scale2+off2
print "RING"
(scale3, off3) = datAc.getScaleOff(bMid[:,6:9],b_meas[2])    
b_rin = b_meas[2]*scale3+off3
print "PINKY"
(scale4, off4) = datAc.getScaleOff(bMid[:,9:],b_meas[3])    
b_pin = b_meas[3]*scale4+off4

#plo.plotter2d((bMid[:,0:3],b_ind,b_meas[0]),("sim index","index fit","raw"))
#plo.plotter2d((bMid[:,3:6],b_mid,b_meas[1]),("sim middle","middle fit","raw"))
#plo.plotter2d((bMid[:,6:9],b_rin,b_meas[2]),("sim ring","ring fit","raw"))
#plo.plotter2d((bMid[:,9:], b_pin,b_meas[3]),("sim pinky","pinky fit","raw"))


b_meas = datAc.textAcquisition("160131_allRin2")    
b_meas *= 0.01
print "-----------ring----------"
print "INDEX"    
#(scale1, off1) = datAc.getScaleOff(bRin[:,0:3],b_meas[0])    
b_ind = b_meas[0]*scale1+off1
print "MIDDLE"
(scale2, off2) = datAc.getScaleOff(bRin[:,3:6],b_meas[1])    
b_mid = b_meas[0]*scale2+off2
print "RING"
#(scale3, off3) = datAc.getScaleOff(bRin[:,6:9],b_meas[2])    
b_rin = b_meas[2]*scale3+off3
print "PINKY"
#(scale4, off4) = datAc.getScaleOff(bRin[:,9:],b_meas[3])    
b_pin = b_meas[3]*scale4+off4

plo.plotter2d((bRin[:,0:3],b_ind,b_meas[0]),("sim index","index fit","raw"))
plo.plotter2d((bRin[:,3:6],b_mid,b_meas[1]),("sim middle","middle fit","raw"))
plo.plotter2d((bRin[:,6:9],b_rin,b_meas[2]),("sim ring","ring fit","raw"))
plo.plotter2d((bRin[:,9:], b_pin,b_meas[3]),("sim pinky","pinky fit","raw"))
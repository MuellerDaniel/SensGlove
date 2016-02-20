import dataAcquisitionMulti as datAc
import plotting as plo
import modelCyl as modC
import modelDip as modD
import handDim as h
import numpy as np

bleCmd = "gatttool -t random -b E7:00:30:16:CD:18 --char-write-req --handle=0x000f --value=0300 --listen"



#calData = datAc.pipeAcquisition(bleCmd,4,measNr=100)

calData = datAc.collectForTime(bleCmd, 30)



#calData = datAc.textAcquisition("160202_hand2")
meas = np.array([calData[0][:,0],calData[0][:,1],calData[0][:,2],
                 calData[1][:,0],calData[1][:,1],calData[1][:,2],
                 calData[2][:,0],calData[2][:,1],calData[2][:,2],
                 calData[3][:,0],calData[3][:,1],calData[3][:,2],]).T

# calculating the B-field
fingerList = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
jointList = [h.jointInd_car,h.jointMid_car,h.jointRin_car,h.jointPin_car]
sensList = [h.sInd_car,h.sMid_car,h.sRin_car,h.sPin_car]

t = np.arange(0,1/2.*np.pi,0.01)
angles = np.zeros((len(t),2*len(sensList)))
cnt = 0
for i in t:
    angles[cnt] = np.array([i, 0.,
                            i, 0.,
                            i, 0.,
                            i, 0.])
    cnt += 1



b_dip = np.zeros((len(t),3*len(sensList)))
b_cyl = np.zeros((len(t),3*len(sensList)))
cnt = 0
for i in angles:
    b_dip[cnt] = modD.cy.angToBm_cy(i,fingerList,sensList,jointList)    
    b_cyl[cnt] = modC.angToB_cyl(i,fingerList,sensList,jointList)    
    cnt += 1

#    caliPos = calcBInd_m[0]

(scale, off) = datAc.getScaleOff(b_dip, meas)

meas_fit = meas * scale + off

plo.plotter2d((b_dip[:,:3], b_dip[:,3:6], b_dip[:,6:9], b_dip[:,9:]),
              ("dipole index","dipole middle","dipole ring","dipole pinky"))
plo.plotter2d((meas_fit[:,:3], meas_fit[:,3:6], meas_fit[:,6:9], meas_fit[:,9:]),
              ("meas_fit index","meas_fit middle","meas_fit ring","meas_fit pinky"))  
plo.plotter2d((meas[:,:3], meas[:,3:6], meas[:,6:9], meas[:,9:]),
              ("meas_raw index","meas_raw middle","meas_raw ring","meas_raw pinky"))                
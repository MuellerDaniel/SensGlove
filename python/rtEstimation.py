import dataAcquisitionMulti as datAc
import matplotlib.pyplot as plt
import modelDip as modD
import modelCyl as modC
import numpy as np
from scipy.optimize import *
import plotting as plo
import time,subprocess
import EKF as k
import jacB as j
import handDim as h

fingerList = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
jointList = [h.jointInd_car,h.jointMid_car,h.jointRin_car,h.jointPin_car]
sensList = [h.sInd_car,h.sMid_car,h.sRin_car,h.sPin_car]

def inStretchPos(ref,meas):
       # number of measurements to take into account
    mMeas = np.zeros((len(meas[0],)))
    for i in range(len(meas[0])):
        mMeas[i] = np.mean(meas[:,i])
    print "summed dif: ",sum((mMeas-ref))
    if abs(sum((mMeas-ref))) < 80:
        return True
    else:
        return False


# simulate the 90 deg movement of all fingers
# perform this movement with your own hand
# return the fitting values
def calibrateData(procCmd):
    print "cali"


    fingerList = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
    jointList = [h.jointInd_car,h.jointMid_car,h.jointRin_car,h.jointPin_car]
    sensList = [h.sInd_car,h.sMid_car,h.sRin_car,h.sPin_car]


#    calData = datAc.pipeAcquisition(procCmd,4,measNr=150)
    calData = datAc.collectForTime(procCmd,20)

    t = np.arange(0,1/2.*np.pi,0.01)
    angles = np.zeros((len(t),2*len(sensList)))
    cnt = 0
    for i in t:
        angles[cnt] = np.array([i, 0.,
                                i, 0.,
                                i, 0.,
                                i, 0.])
        cnt += 1

    # calculating the B-field
    fingerList = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
    jointList = [h.jointInd_car,h.jointMid_car,h.jointRin_car,h.jointPin_car]
    sensList = [h.sInd_car,h.sMid_car,h.sRin_car,h.sPin_car]

    calcB_dip = np.zeros((len(t),3*len(sensList)))
    calcB_cyl = np.zeros((len(t),3*len(sensList)))
    cnt = 0
    for i in angles:
        calcB_dip[cnt] = modD.cy.angToBm_cy(i,fingerList,sensList,jointList)
        calcB_cyl[cnt] = modC.cy.angToB_cyl(i,fingerList,sensList,jointList)
        cnt += 1

    # fitting to dipole model
    (scaleInd,offInd) = datAc.getScaleOff(calcB_dip[:,0:3] , calData[0])
    (scaleMid,offMid) = datAc.getScaleOff(calcB_dip[:,3:6] , calData[1])
    (scaleRin,offRin) = datAc.getScaleOff(calcB_dip[:,6:9] , calData[2])
    (scalePin,offPin) = datAc.getScaleOff(calcB_dip[:,9:12], calData[3])

    # fitting to cylindrical model
    # (scaleInd,offInd) = datAc.getScaleOff(calcB_cyl[:,0:3] , calData[0])
    # (scaleMid,offMid) = datAc.getScaleOff(calcB_cyl[:,3:6] , calData[1])
    # (scaleRin,offRin) = datAc.getScaleOff(calcB_cyl[:,6:9] , calData[2])
    # (scalePin,offPin) = datAc.getScaleOff(calcB_cyl[:,9:12], calData[3])

    scaleArr = np.array([scaleInd, scaleMid, scaleRin, scalePin])
    offArr = np.array([offInd, offMid, offRin, offPin])

    return (scaleArr, offArr)








#def main():
bleCmd = "gatttool -t random -b E7:00:30:16:CD:18 --char-write-req --handle=0x000f --value=0300 --listen"

''' calibration process '''
(scaleValues, offValues) = calibrateData(bleCmd)

print scaleValues
print offValues

print "Press Enter to go ahed..."
try:
    sys.stdin.readline()
except KeyboardInterrupt:
    pass



''' RT estimation '''
procBle = subprocess.Popen(bleCmd.split(),
                           stdout=subprocess.PIPE, close_fds=True)

#    bnds = ((0.0,np.pi/2),      # MCP
#            (0.0,np.pi/(180/110)),      # PIP
#            #(0.0,np.pi/2),
#            (0.0,np.pi/2),      # MCP
#            (0.0,np.pi/(180/110)),      # PIP
#            #(0.0,np.pi/2))      # DIP
#            (0.0,np.pi/2),      # MCP
#            (0.0,np.pi/(180/110)),      # PIP
#            #(0.0,np.pi/2))      # DIP
#            (0.0,np.pi/2),      # MCP
#            (0.0,np.pi/(180/110)))      # PIP
#            #(0.0,np.pi/2))      # DIP


# error covariance matrix (8x8), gets updated each step, so the initial one is not so important...
P = np.eye(8)

# process noise covariance matrix (8x8)
#Q = np.diag([1e+2, 1e-2, 1e-2, 1e+2, 1e+2, 1e-2, 1e+2, 1e-2,])
Q = np.eye(8) * 1e+2

# measurement noise covariance matrix (12x12)
#R = np.diag([1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1, 1e-1])
R = np.eye(12) * 1e-1


x_EKF = np.zeros((1, 2*len(fingerList)))
#x_EKF[0] = angles[0]


estAngMeas = np.zeros((1,2*len(fingerList)))
measB = np.zeros((3*len(fingerList),))
fval = np.array([0.])
cnt = 0
errCnt = 0

sensI = np.array([[0.,0.,0.]])
sensM = np.array([[0.,0.,0.]])
sensR = np.array([[0.,0.,0.]])
sensP = np.array([[0.,0.,0.]])



try:
#    time.sleep(0.5)
    while True:
        print "cnt: ",cnt
        cnt += 1

        data = datAc.RTdata_blocking(procBle)
#            print data

        sensI = np.append(sensI, [data[0][1:]*scaleValues[0]+offValues[0]],axis=0)
        sensM = np.append(sensM, [data[1][1:]*scaleValues[1]+offValues[1]],axis=0)
        sensR = np.append(sensR, [data[2][1:]*scaleValues[2]+offValues[2]],axis=0)
        sensP = np.append(sensP, [data[3][1:]*scaleValues[3]+offValues[3]],axis=0)

#        print "index: ",sensI[-1]
#        print "middle: ",sensM[-1]
#        print "ring: ", sensR[-1]
#        print "pinky: ", sensP[-1]

#        measB = np.concatenate((sensI[-1],sensM[-1],sensR[-1],sensP[-1]))

##       TODO here goes the estimation stuff...
#        normal estimation

#        res = modD.estimate_BtoAng(estAngMeas[-1], fingerList, jointList, sensList, measB)

#        estAngMeas = np.append(estAngMeas,[res.x],axis=0)
#        fval = np.append(fval,res.fun)

#       EKF estimation
        (x_p, P_p) = k.EKF_predict_hand(x_EKF[cnt-1], P, Q)

        (x_EKF_new, P) = k.EKF_update_hand(j.jacMulti, measB, x_p, P_p, R)
        print x_EKF_new
        x_EKF = np.append(x_EKF,[x_EKF_new],axis=0)


except KeyboardInterrupt:
    print "ended, cnt: ", cnt
    print "errorCnt: ", errCnt

procBle.kill()

plo.plotter2d((sensI,sensM,sensR,sensP),("index","middle","ring","pinky"))

#    print scaleInd,offInd
#    print scaleMid,offMid
#    print scaleRin,offRin
#    print scalePin,offPin

#if __name__ == "__main__":
#    main()

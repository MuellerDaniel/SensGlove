import dataAcquisitionMulti as datAc
import matplotlib.pyplot as plt
import modelDip_A as modD
import modelCyl_A as modC
import numpy as np
from scipy.optimize import *
import plotting as plo
import time,subprocess
#import EKF as k
#import jacB as j
import handDim as h
import sys



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

#    calData = datAc.pipeAcquisition(procCmd,4,measNr=150)
    calData = datAc.collectForTime(procCmd,5)

    # convert to Tesla
#    print "type calData", type(calData)
#    print "type calData[0]",type(calData[0])
    nInd = calData[0]*1e-7
    nMid = calData[1]*1e-7
    nRin = calData[2]*1e-7
    nPin = calData[3]*1e-7
    # reassign the tuple...
    calData = None
    calData = (nInd, nMid, nRin, nPin)


    # calculating the B-field
    fingerList = [h.phalInd]
    jointList = [h.jointInd]
    sensList = [h.sInd,h.sMid,h.sRin,h.sPin]

    t = np.arange(0,1/2.*np.pi,0.01)
    angles = np.zeros((len(t),3))
    cnt = 0
    for i in t:
        angles[cnt] = np.array([i, 0., 0.])
        cnt += 1


#    calcB_dip = np.zeros((len(t),3*len(sensList)))
    calcB_cyl = np.zeros((len(t),3*len(sensList)))
    cnt = 0
    for i in angles:
#        calcB_dip[cnt] = modD.cy.angToBm_cy(i,fingerList,sensList,jointList)
        calcB_cyl[cnt] = modC.cy.angToB_cyl(i,fingerList,sensList,jointList)
        cnt += 1

    # fitting to dipole model
    (scaleInd,offInd) = datAc.getScaleOff(calcB_cyl[:,0:3] , calData[0])
    (scaleMid,offMid) = datAc.getScaleOff(calcB_cyl[:,3:6] , calData[1])
    (scaleRin,offRin) = datAc.getScaleOff(calcB_cyl[:,6:9] , calData[2])
    (scalePin,offPin) = datAc.getScaleOff(calcB_cyl[:,9:12], calData[3])

    scaleArr = np.array([scaleInd, scaleMid, scaleRin, scalePin])
    offArr = np.array([offInd, offMid, offRin, offPin])

    cInd = calData[0]*scaleInd+offInd
    cMid = calData[1]*scaleMid+offMid
    cRin = calData[2]*scaleRin+offRin
    cPin = calData[3]*scalePin+offPin

    # plo.plotter2d((cInd,cMid,cRin,cPin),("calIndex","calMid","calRin","calPin"))
    # plt.figure()
    # plo.plotter2d((calcB_cyl[:,0:3],calcB_cyl[:,3:6],calcB_cyl[:,6:9],calcB_cyl[:,9:]),
                #   ("simIndex","simMid","simRin","simPin"))

    return (scaleArr, offArr)







bleCmd = "gatttool -t random -b E7:00:30:16:CD:18 --char-write-req --handle=0x000f --value=0100 --listen"

''' calibration process '''
(scaleValues, offValues) = calibrateData(bleCmd)

print scaleValues
print offValues

print "Stretch finger and press Enter to go ahed..."

try:
    sys.stdin.readline()
except KeyboardInterrupt:
    pass



''' RT estimation '''
fingerList = [h.phalInd]
jointList = [h.jointInd]
sensList = [h.sInd,h.sMid,h.sRin,h.sPin]

procBle = subprocess.Popen(bleCmd.split(), stdout=subprocess.PIPE, close_fds=True)

a_bnds = ((0.0,np.pi/2),      # MCP
        (0.0,np.pi/(180/110)),      # PIP
        (-(30./180)*np.pi,(30./180)*np.pi))


estAng = np.zeros((1,3*len(fingerList)))
cnt = 0
errCnt = 0

sensI = np.array([[0.,0.,0.]])
sensM = np.array([[0.,0.,0.]])
sensR = np.array([[0.,0.,0.]])
sensP = np.array([[0.,0.,0.]])

# Blender stuff
fileName = "fingStates.txt"
f = open(fileName,'w')
toSend = ("mag " + "0.0000 0.0000 0.0000 " +
                    "0.0000 0.0000 0.0000 " +
                    "0.0000 0.0000 0.0000 " +
                    "0.0000 0.0000 0.0000")
f.write(toSend+'\n')
f.close()

blendCmd = "./../visualization/riggedAni/HandGame.blend " + fileName
subPro = subprocess.Popen(blendCmd.split())

data = np.zeros((4,4))

try:
#    time.sleep(0.5)
    while True:
        print "cnt: ",cnt

        # "blocking"
#        data = datAc.readMagPacket(procBle)
        # "non-blocking"
        data = datAc.RTdata(data,procBle)

        # convert to Tesla
        data *= 1e-7
#            print data

        sensI = np.append(sensI, [data[0][1:]*scaleValues[0]+offValues[0]],axis=0)
        sensM = np.append(sensM, [data[1][1:]*scaleValues[1]+offValues[1]],axis=0)
        sensR = np.append(sensR, [data[2][1:]*scaleValues[2]+offValues[2]],axis=0)
        sensP = np.append(sensP, [data[3][1:]*scaleValues[3]+offValues[3]],axis=0)

#        print "index: ",sensI[-1]
#        print "middle: ",sensM[-1]
#        print "ring: ", sensR[-1]
#        print "pinky: ", sensP[-1]

        measB = np.concatenate((sensI[-1],sensM[-1],sensR[-1],sensP[-1]))
#        print "measB.shape ", measB.shape

#        normal estimation
        res = modC.estimateAng_cyl(estAng[cnt], fingerList, sensList, jointList, measB, bnds=a_bnds, method=1)
#        print "estimation result: " ,res.x

        estAng = np.append(estAng,[res.x],axis=0)
#        print "estAng.shape ", estAng.shape

        # Blender stuff
        outstr = ("mag " + "{0:.4f} ".format(estAng[-1][0])+"{0:.4f} ".format(estAng[-1][1])+"{0:.4f} ".format(1*estAng[-1][2]) +
                            "0.0000 0.0000 0.0000 " +
                            "0.0000 0.0000 0.0000 " +
                            "0.0000 0.0000 0.0000")
        f = open(fileName,'w')
        f.write(outstr + '\n')
        f.close()
        print "sended: ", outstr


        cnt += 1




except KeyboardInterrupt:
    print "ended, cnt: ", cnt
    print "errorCnt: ", errCnt

procBle.kill()

# plt.figure()
# plot angles...
# plo.plotter2d((estAng,),("angles",))

# plot B
# plo.plotter2d((sensI, sensM, sensR, sensP),
#               ("B ind", "B mid", "B rin", "B pin"))

#plt.show()

#    print scaleInd,offInd
#    print scaleMid,offMid
#    print scaleRin,offRin
#    print scalePin,offPin

#if __name__ == "__main__":
#    main()

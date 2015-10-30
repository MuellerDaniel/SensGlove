import numpy as np
import matplotlib.pyplot as plt
import modelEqMultiCython as modE
import plotting as plo

""" the artificial data... """
angInd = [0.09138, 0.02957, -0.01087]         # to wooden-angle(index)
angMid = [0.09138, 0.00920, -0.01087]          # to wooden-angle(middle)
angRin = [0.09138, -0.01117, -0.01087]         # to wooden-angle(ring)
angPin = [0.09138, -0.03154, -0.01087]         # to wooden-angle(pinky)

# position of sensor
s1 = [0.06755, 0.02957, 0.]     # sensor beneath index
#s1 = [0.08755, 0.02957, 0.]
#s2 = [0.06755, 0.00920, 0.]    
s2 = [0.04755, 0.00920, 0.]     # sensor beneath middle
s3 = [0.06755, -0.01117, 0.]    # sensor beneath ring
#s3 = [0.08755, -0.01117, 0.]
#s4 = [0.06755, -0.03012, 0.]     
s4 = [0.04755, -0.03012, 0.]    # sensor beneath pinky

rInd = 0.08     # length of index finger (from angle)
rMid = 0.08829  # length of middle finger (from angle)
rRin = 0.07979  # length of ring finger (from angle)
rPin = 0.07215  # length of pinky finger (from angle)
# values for the half circle
t = np.arange(0, 1/2.*np.pi, 0.01)
pos1 = [[0.,0.,0.]]
pos2 = [[0.,0.,0.]]
pos3 = [[0.,0.,0.]]
pos4 = [[0.,0.,0.]]

orien = [[0.,0.,0.]]

cnt=1
for i in t:
    # position of the index finger
    pos1 = np.append(pos1, [[angInd[0]+rInd*np.cos(i),
                            angInd[1],
                            angInd[2]-rInd*np.sin(i)]],
                            axis=0)

    # positions of the middle finger
    pos2 = np.append(pos2, [[angMid[0]+rMid*np.cos(i),
                            angMid[1],
                            angMid[2]-rMid*np.sin(i)]],
                            axis=0)

      # position of the ring finger
    pos3 = np.append(pos3, [[angRin[0]+rRin*np.cos(i),
                            angRin[1],
                            angRin[2]-rRin*np.sin(i)]],
                            axis=0)

    # positions of the pinky finger
    pos4 = np.append(pos4, [[angPin[0]+rPin*np.cos(i),
                            angPin[1],
                            angPin[2]-rPin*np.sin(i)]],
                            axis=0)
                            
    orien = np.append(orien, [[-1*np.cos(i),
                               0,
                               1*np.sin(i)]],axis=0)                            

    cnt+=1

pos = np.zeros(shape=(4,len(pos1)-1,3))
pos[0] = pos1[1:]
pos[1] = pos2[1:]
pos[2] = pos3[1:]
pos[3] = pos4[1:]
orien = orien[1:]

calcBInd = [[[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]]]
calcBMid = [[[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]]]      # The cumulative field measured with sensor at s0
calcBMid_dot = [[[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]]]
calcBRin = [[[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]]]
calcBPin = [[[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]],
            [[0.,0.,0.]]]

cnt=0
# calculate the magnetic fields for each sensor and each magnet
for i in range(pos.shape[1]):
    calcBInd[0] = np.append(calcBInd[0],
                      modE.evalfuncMagDotH(pos[0][i],orien[i],s1), axis=0)
    calcBInd[1] = np.append(calcBInd[1],
                      modE.evalfuncMagDotH(pos[1][i],orien[i],s1), axis=0)
    calcBInd[2] = np.append(calcBInd[2],
                      modE.evalfuncMagDotH(pos[2][i],orien[i],s1), axis=0)
    calcBInd[3] = np.append(calcBInd[3],
                      modE.evalfuncMagDotH(pos[3][i],orien[i],s1), axis=0)

    calcBMid[0] = np.append(calcBMid[0],
                      modE.evalfuncMagDotH(pos[0][i],orien[i],s2), axis=0)
    calcBMid[1] = np.append(calcBMid[1],
                      modE.evalfuncMagDotH(pos[1][i],orien[i],s2), axis=0)
    calcBMid[2] = np.append(calcBMid[2],
                      modE.evalfuncMagDotH(pos[2][i],orien[i],s2), axis=0)
    calcBMid[3] = np.append(calcBMid[3],
                      modE.evalfuncMagDotH(pos[3][i],orien[i],s2), axis=0)

    calcBRin[0] = np.append(calcBRin[0],
                      modE.evalfuncMagDotH(pos[0][i],orien[i],s3), axis=0)
    calcBRin[1] = np.append(calcBRin[1],
                      modE.evalfuncMagDotH(pos[1][i],orien[i],s3), axis=0)
    calcBRin[2] = np.append(calcBRin[2],
                      modE.evalfuncMagDotH(pos[2][i],orien[i],s3), axis=0)
    calcBRin[3] = np.append(calcBRin[3],
                      modE.evalfuncMagDotH(pos[3][i],orien[i],s3), axis=0)

    calcBPin[0] = np.append(calcBPin[0],
                      modE.evalfuncMagDotH(pos[0][i],orien[i],s4), axis=0)
    calcBPin[1] = np.append(calcBPin[1],
                      modE.evalfuncMagDotH(pos[1][i],orien[i],s4), axis=0)
    calcBPin[2] = np.append(calcBPin[2],
                      modE.evalfuncMagDotH(pos[2][i],orien[i],s4), axis=0)
    calcBPin[3] = np.append(calcBPin[3],
                      modE.evalfuncMagDotH(pos[3][i],orien[i],s4), axis=0)

calcBInd = np.delete(calcBInd,0,1)
calcBMid = np.delete(calcBMid,0,1)
calcBMid_dot = np.delete(calcBMid_dot,0,1)
calcBRin = np.delete(calcBRin,0,1)
calcBPin = np.delete(calcBPin,0,1)

# REMEMBER: only add the fields, that you realy need!
summedInd=np.zeros(shape=(len(calcBInd[0]),3))
summedInd+=(calcBInd[0]+calcBInd[1]+calcBInd[2]+calcBInd[3])
#summedInd+=(calcBInd[0])
summedMid=np.zeros(shape=(len(calcBMid[0]),3))
summedMid+=(calcBMid[0]+calcBMid[1]+calcBMid[2]+calcBMid[3])
summedRin=np.zeros(shape=(len(calcBRin[0]),3))
summedRin+=(calcBRin[0]+calcBRin[1]+calcBRin[2]+calcBRin[3])
summedPin=np.zeros(shape=(len(calcBPin[0]),3))
summedPin+=(calcBPin[0]+calcBPin[1]+calcBPin[2]+calcBPin[3])

''' save it to a file in the desired format '''
fi = open("151030_perfectB_H",'w')
for i in range(len(summedInd)):
    fi.write(str(0) + "\t" + str(summedInd[i][0]) + "\t" + 
                            str(summedInd[i][1]) + "\t" + 
                            str(summedInd[i][2]) + "\n")
    fi.write(str(1) + "\t" + str(summedMid[i][0]) + "\t" + 
                            str(summedMid[i][1]) + "\t" + 
                            str(summedMid[i][2]) + "\n")
    fi.write(str(2) + "\t" + str(summedRin[i][0]) + "\t" + 
                            str(summedRin[i][1]) + "\t" + 
                            str(summedRin[i][2]) + "\n")
    fi.write(str(3) + "\t" + str(summedPin[i][0]) + "\t" + 
                            str(summedPin[i][1]) + "\t" + 
                            str(summedPin[i][2]) + "\n")
fi.close()                            

plo.plotter2d((summedInd, summedMid, summedRin, summedPin),("ind","mid","rin","pin"))

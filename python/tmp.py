import numpy as np
import matplotlib.pyplot as plt


""" the artificial data... """
#angInd = [0.02957, 0.09138, 0.01087]         # to wooden-angle(index)
#angMid = [0.00920, 0.09138, 0.01087]          # to wooden-angle(middle)
#angRin = [-0.01117, 0.09138, 0.01087]         # to wooden-angle(ring)
#angPin = [-0.03154, 0.09138, 0.01087]         # to wooden-angle(pinky)
angInd = [0.02957, 0.09138, 0.]         # to wooden-angle(index)
angMid = [0.00920, 0.09138, 0.]          # to wooden-angle(middle)
angRin = [-0.01117, 0.09138, 0.]         # to wooden-angle(ring)
angPin = [-0.03154, 0.09138, 0.]         # to wooden-angle(pinky)

# position of sensor
s1 = [0.02957, 0.06755, 0.]     # sensor beneath index
#s1 = [0.02886, 0.06755, 0.]
s2 = [0.00920 , 0.06755, 0.]    # sensor beneath middle
#s2 = [0.00920 , 0.02755, 0.]
s3 = [-0.01117, 0.06755, 0.]     # sensor beneath ring
#s3 = [-0.01046, 0.06755, 0.]
s4 = [-0.03154, 0.06755, 0.]     # sensor beneath pinky
#s4 = [-0.03012, 0.02755, 0.]

rInd = 0.08                     # length of index finger (from angle)
rMid = 0.08829                  # length of middle finger (from angle)
rRin = 0.07979                  # length of ring finger (from angle)
rPin = 0.07215                  # length of pinky finger (from angle)
# values for the half circle
t = np.arange(0, 1/2.*np.pi, 0.01)
pos1 = [[0.,0.,0.]]
pos2 = [[0.,0.,0.]]
pos3 = [[0.,0.,0.]]
pos4 = [[0.,0.,0.]]
cnt=1
for i in t:
    # position of the index finger
    pos1 = np.append(pos1, [[angInd[0],
                            angInd[1]+rInd*np.cos(i),
                            angInd[2]+rInd*np.sin(i)]],
                            axis=0)

    # positions of the middle finger
    pos2 = np.append(pos2, [[angMid[0],
                            angMid[1]+rMid*np.cos(i),
                            angMid[2]+rMid*np.sin(i)]],
                            axis=0)
#    pos2 = np.append(pos2, [[angMid[0],
#                            angMid[1]+rMid*np.cos(i/2),
#                            angMid[2]+rMid*np.sin(i/2)]],
#                            axis=0)

      # position of the ring finger
    pos3 = np.append(pos3, [[angRin[0],
                            angRin[1]+rRin*np.cos(i),
                            angRin[2]+rRin*np.sin(i)]],
                            axis=0)

    # positions of the pinky finger
    pos4 = np.append(pos4, [[angPin[0],
                            angPin[1]+rPin*np.cos(i),
                            angPin[2]+rPin*np.sin(i)]],
                            axis=0)
#    pos4 = np.append(pos4, [[angPin[0],
#                            angPin[1],
#                            angPin[2]]],
#                            axis=0)

    cnt+=1

pos = np.zeros(shape=(4,len(pos1)-1,3))
pos[0] = pos1[1:]
pos[1] = pos2[1:]
pos[2] = pos3[1:]
pos[3] = pos4[1:]

S = [s1,s2,s3,s4]
R = np.zeros(shape=(4,len(pos1)-1,3))       # R = S-P
H = np.zeros(shape=(4,len(pos1)-1,3))       # H = P-S

for j in range(4):
    for i in range(len(t)):
        R[j][i] = S[j]-pos[j][i]
        H[j][i] = pos[j][i]-S[j]
        
        
plt.figure('R')
plt.clf()
plt.plot(R[0][:,0],'r',(R[0][:,1]),'g',(R[0][:,2]),'b')
#plt.plot(R[0][:,2],R[0][:,1])
plt.figure('H')
plt.clf()
plt.plot(H[0][:,0],'r',(H[0][:,1]),'g',(H[0][:,2]),'b')
#plt.plot(H[0][:,2],H[0][:,1])

plt.show()



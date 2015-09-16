import modelEqMultiTWO as modE
import numpy as np
import matplotlib.pyplot as plt


angInd = [0.02957, 0.09138, 0.01087]         # to wooden-angle(index) 
angMid = [0.00920, 0.09138, 0.01087]          # to wooden-angle(middle) 
angRin = [-0.01117, 0.09138, 0.01087]         # to wooden-angle(ring) 
angPin = [-0.03154, 0.09138, 0.01087]         # to wooden-angle(pinky) 

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
        
    cnt+=1
    
pos = np.zeros(shape=(4,len(pos1)-1,3))
pos[0] = pos1[1:]
pos[1] = pos2[1:]
pos[2] = pos3[1:]
pos[3] = pos4[1:]

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
                      modE.evalfuncMagDot(pos[0][i],s1), axis=0)
    calcBInd[1] = np.append(calcBInd[1],
                      modE.evalfuncMagDot(pos[1][i],s1), axis=0)
    calcBInd[2] = np.append(calcBInd[2],
                      modE.evalfuncMagDot(pos[2][i],s1), axis=0)  
    calcBInd[3] = np.append(calcBInd[3],
                      modE.evalfuncMagDot(pos[3][i],s1), axis=0)
                      
    calcBMid[0] = np.append(calcBMid[0],
                      modE.evalfuncMagDot(pos[0][i],s2), axis=0)
    calcBMid[1] = np.append(calcBMid[1],
                      modE.evalfuncMagDot(pos[1][i],s2), axis=0)
    calcBMid[2] = np.append(calcBMid[2],
                      modE.evalfuncMagDot(pos[2][i],s2), axis=0)                      
    calcBMid[3] = np.append(calcBMid[3],
                      modE.evalfuncMagDot(pos[3][i],s2), axis=0)

    calcBRin[0] = np.append(calcBRin[0],
                      modE.evalfuncMagDot(pos[0][i],s3), axis=0)
    calcBRin[1] = np.append(calcBRin[1],
                      modE.evalfuncMagDot(pos[1][i],s3), axis=0)
    calcBRin[2] = np.append(calcBRin[2],
                      modE.evalfuncMagDot(pos[2][i],s3), axis=0)                            
    calcBRin[3] = np.append(calcBRin[3],
                      modE.evalfuncMagDot(pos[3][i],s3), axis=0) 

    calcBPin[0] = np.append(calcBPin[0],
                      modE.evalfuncMagDot(pos[0][i],s4), axis=0)
    calcBPin[1] = np.append(calcBPin[1],
                      modE.evalfuncMagDot(pos[1][i],s4), axis=0)
    calcBPin[2] = np.append(calcBPin[2],
                      modE.evalfuncMagDot(pos[2][i],s4), axis=0)
    calcBPin[3] = np.append(calcBPin[3],
                      modE.evalfuncMagDot(pos[3][i],s4), axis=0)

calcBInd = np.delete(calcBInd,0,1)    
calcBMid = np.delete(calcBMid,0,1)
calcBMid_dot = np.delete(calcBMid_dot,0,1)        
calcBRin = np.delete(calcBRin,0,1)
calcBPin = np.delete(calcBPin,0,1)      

# REMEMBER: only add the fields, that you realy need!
summedInd=np.zeros(shape=(1,len(calcBInd[0]),3))
summedInd+=(calcBInd[0]+calcBInd[1]+calcBInd[2]+calcBInd[3])
summedMid=np.zeros(shape=(1,len(calcBMid[0]),3))
summedMid+=(calcBMid[0]+calcBMid[1]+calcBMid[2]+calcBMid[3])              
summedRin=np.zeros(shape=(1,len(calcBRin[0]),3))
summedRin+=(calcBRin[0]+calcBRin[1]+calcBRin[2]+calcBRin[3])
summedPin=np.zeros(shape=(1,len(calcBPin[0]),3))
summedPin+=(calcBPin[0]+calcBPin[1]+calcBPin[2]+calcBPin[3])

""" estimating the position from the measurments """
estPos = np.zeros(shape=(4,len(summedMid[0]),3))
#estPos2 = np.zeros(shape=(2,len(summedMid[0]),3))
#estPos[0][0] = [angMid[0]+s0[0], angMid[1]+s0[1]+rMid, s0[2]+angMid[2]]
#estPos[1][0] = [angPin[0]+s0[0], angPin[1]+s0[1]+rPin, s0[2]+angPin[2]]
estPos[0][0] = pos[0][0]
estPos[1][0] = pos[1][0]  
estPos[2][0] = pos[2][0]
estPos[3][0] = pos[3][0]
                
# fixed bnds                  
bnds=((angInd[0]-0.003,angInd[0]+0.003),    # index finger
      (angInd[1],angInd[1]+rInd),
      (angInd[2],angInd[2]+rInd),

      (angMid[0]-0.003,angMid[0]+0.003),    # middle finger
      (angMid[1],angMid[1]+rMid),
      (angMid[2],angMid[2]+rMid),
      
      (angRin[0]-0.003,angRin[0]+0.003),    # ring finger
      (angRin[1],angRin[1]+rRin),
      (angRin[2],angRin[2]+rRin),
      
      (angPin[0]-0.003,angPin[0]+0.003),    # pinky finger
      (angPin[1],angPin[1]+rPin),
      (angPin[2],angPin[2]+rPin))                   
      
S=np.append(s1,s2,axis=0)        
S=np.append(S,s3,axis=0)
S=np.append(S,s4,axis=0)
B=np.zeros((4,3))

i=0
B[0] = summedInd[0][i+1]
B[1] = summedMid[0][i+1]
B[2] = summedRin[0][i+1]
B[3] = summedPin[0][i+1]

P = np.concatenate((estPos[0][i],estPos[1][i],estPos[2][i],estPos[3][i]))

plo.plotter2d((summedInd,summedMid,summedRin,summedPin),("index","Mid","Rin","Pin"))                        


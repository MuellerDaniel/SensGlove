'''
    script for checking the calibrated output of your sensor
    just wave the sensors around
'''
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np


''' calibration according to AN4246 from Freescale '''
def calcFreescale(data):
    
    Y = np.zeros((len(data),))
    X = np.zeros((len(data),4))
    
    cnt = 0
    for i in data:
        for a in i:
            Y[cnt] += a**2
        X[cnt] = np.append(i,[1])
        cnt += 1
    
    beta = np.dot(np.dot(np.linalg.inv(np.dot(X.T,X)),X.T),Y)
    return beta
            

''' checking the calibration values '''
# in the way, the easy (internet) approach does it
def calcHardSoft(data):
    cnt = 0
    
    tmp = np.zeros((1,len(data),3))    
    tmp[0] = data
    data = tmp
    
    for i in data:     # for a shape of (sensors,datapoints,3)
    #for i in a:  
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
     
    cnt = 0 
    for i in data:  
        print "sensor ",cnt
        for j in range(3):
            print "min in "+str(j)+" "+str(min(i[:,j]))
            print "max in "+str(j)+" "+str(max(i[:,j])) 
        cnt += 1  
    
    hard = np.array([offX, offY, offZ])
    soft = np.array([rad/tmpX, rad/tmpY, rad/tmpZ])
    return (hard,soft)
    
   
def deviation(values):    
    ''' find the procentual deviation from the mean of n measurements for x, y, z components ''' 
    rangeX = max(values[:,0]) - min(values[:,0])
    rangeY = max(values[:,1]) - min(values[:,1])
    rangeZ = max(values[:,2]) - min(values[:,2])
    
    meanX = np.mean(values[:,0])
    meanY = np.mean(values[:,1])
    meanZ = np.mean(values[:,2])
    meanArr = np.array([meanX,meanY,meanZ])
    
    # procentual deviation from the mean
    devX = rangeX/meanX
    devY = rangeY/meanY
    devZ = rangeZ/meanZ    
    devArr = np.array([devX,devY,devZ])
    
    return (meanArr,devArr)
    
    
        
    
    
    
''' data acquisition '''
#data = datAc.pipeAcquisition("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen",
#                             4,measNr=500)

#data = datAc.pipeAcquisition('stty -F /dev/ttyACM0 time 50; cat /dev/ttyACM0',nrSens=1,fileName=None,measNr=1000)
#data = datAc.textAcquisition("160111_calData0")

#plo.visMagData(data)           
#plt.figure()
#plo.plotter2d((data[0],),("meas",))
#plt.plot(data[0][:,0])
#plt.figure()
#plt.plot(data[0][:,1])
#plt.figure()
#plt.plot(data[0][:,2])

''' calculate and the hard/soft bias values '''
#(oldHard,oldSoft) = calcHardSoft(data)
#avg = datAc.moving_average3d(data[0],10)
#a = np.zeros((1,len(avg),3))
#a[0] = avg
#print "averaged: "
#calcHardSoft(data[0])
#b = calibrate(data[0])
#v_x = b[0]/2
#v_y = b[1]/2
#v_z = b[2]/2
#B = np.sqrt(b[3]+v_x**2+v_y**2+v_z**2)
#print "\nv_x", v_x
#print "v_y", v_y
#print "v_z", v_z
#print "B", B

#caliData_old = (data[0]-oldHard)*oldSoft
#tmp = np.zeros((1,len(data[0]),3))
#tmp[0] = caliData_old
#caliData_old = tmp
#caliData_new = data[0]-np.array([v_x,v_y,v_z])
#tmp = np.zeros((1,len(data[0]),3))
#tmp[0] = caliData_new
#caliData_new = tmp

''' determine the deviation of the collected min and max values '''
# values from 160111
minValuesA = np.array([[-383.265899, -424.644134, -484.022399],
                      [-397.618103, -439.450225, -488.259124],
                      [-375.511627, -439.803649, -481.366638]])
maxValuesA = np.array([[438.796539, 389.688110, 340.282287],
                      [420.101837, 397.117309, 337.497558],
                      [455.424255, 405.229278, 338.208709]])

# values from 160115
minValues = np.array([[-387.834869, -414.776000, -481.082092],
                      [-407.850067, -439.614166, -464.585784],
                      [-404.837249, -447.333312, -476.074279]])
maxValues = np.array([[417.674530, 366.546234, 318.354431],
                      [438.817718, 370.277496, 343.030700],
                      [432.838745, 386.539398, 339.903320]])                      

minValues = np.concatenate((minValuesA,minValues))
maxValues = np.concatenate((maxValuesA,maxValues))

(mMin,dMin) = deviation(minValues)
(mMax,dMax) = deviation(maxValues)

print "mean Min\n", mMin
print "mean Max\n", mMax
print "deviation Min [%]\n", dMin*100
print "deviation Max [%]\n", dMax*100

print "hard, soft values"
(hard,soft) = calcHardSoft(np.concatenate(([mMin],[mMax])))
print hard
print soft
print "Freescale hard values"
frees = calcFreescale(np.concatenate(([mMin],[mMax])))
print frees


      
        
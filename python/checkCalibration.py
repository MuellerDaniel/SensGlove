'''
    script for checking the calibrated output of your sensor
    just wave the sensors around
'''
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np



''' calibration according to http://bazaar.launchpad.net/~fabio-varesano/freeimu/trunk/view/head:/FreeIMU_GUI/FreeIMU_GUI/cal_lib.py '''
def calibrate(data):
    x = data[:,0]
    y = data[:,1]
    z = data[:,2]
 
    H = np.array([x, y, z, -y**2, -z**2, np.ones([len(x), 1])])
    H = np.transpose(H)
    w = x**2
  
    (X, residues, rank, shape) = np.linalg.lstsq(H, w)
  
    OSx = X[0] / 2
    OSy = X[1] / (2 * X[3])
    OSz = X[2] / (2 * X[4])
  
    A = X[5] + OSx**2 + X[3] * OSy**2 + X[4] * OSz**2
    B = A / X[3]
    C = A / X[4]
  
    SCx = np.sqrt(A)
    SCy = np.sqrt(B)
    SCz = np.sqrt(C)
  
    # type conversion from numpy.float64 to standard python floats
    offsets = [OSx, OSy, OSz]
    scale = [SCx, SCy, SCz]
  
    offsets = map(np.asscalar, offsets)
    scale = map(np.asscalar, scale)
  
    return (offsets, scale)


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
#    return beta
    off = [0.5*beta[0], 0.5*beta[1], 0.5*beta[2]]
    mag = np.sqrt(beta[3]+off[0]**2+off[1]**2+off[2]**2)
    
    calibrated = data - off    
    
    return (off,mag,calibrated)
            

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
    
    calibrated = data*soft-hard    
    
    return (hard,soft, calibrated)
    
   
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
    
 
def meanCalc(values):
    mean = np.zeros((values.shape[0],3))    
    
    cnt = 0
    for i in values:        
        mean[cnt] = np.array([np.mean(i[:,0]), np.mean(i[:,1]), np.mean(i[:,2])])
        
        cnt += 1
        
    return mean        
    
   
def calcDif(data, ref):
    res = np.zeros((len(data),))
    
    cnt = 0
    for i in data:
        res[cnt] = (np.sqrt(i[0]**2+i[1]**2+i[2]**2) - ref) / ref 
        cnt += 1
    res *= 100
    return res
    
   
''' data acquisition '''

#d = datAc.pipeAcquisition("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen",
#    d = datAc.pipeAcquisition("gatttool -t random -b E7:00:30:16:CD:18 --char-write-req --handle=0x000f --value=0300 --listen",                          
#                                 4,measNr=500, fileName="160127_noRot")
d = datAc.textAcquisition("160208_calDat")
#    d = datAc.textAcquisition("160212_calDat")


''' calculate and the hard/soft bias values '''
#(hard_old, soft_old) = calcHardSoft(d[0])
#print "hard_old: ", hard_old
#print "soft_old: ", soft_old

''' Freescale '''
#free0 = calcFreescale(d0[0])
#free1 = calcFreescale(d1[0])
#free2 = calcFreescale(d2[0])
#
#off0 = [0.5*free0[0], 0.5*free0[1], 0.5*free0[2]]
#mag0 = np.sqrt(free0[3]+off0[0]**2+off0[1]**2+off0[2]**2)
#
#off1 = [0.5*free1[0], 0.5*free1[1], 0.5*free1[2]]
#mag1 = np.sqrt(free1[3]+off1[0]**2+off1[1]**2+off1[2]**2)
#
#off2 = [0.5*free2[0], 0.5*free2[1], 0.5*free2[2]]
#mag2 = np.sqrt(free2[3]+off2[0]**2+off2[1]**2+off2[2]**2)
#
#print "off0 ", off0
#print "mag0 ", mag0
#print "off1 ", off1
#print "mag1 ", mag1
#print "off2 ", off2
#print "mag2 ", mag2

#free = calcFreescale(d[0])
#off = [0.5*free[0], 0.5*free[1], 0.5*free[2]]
#mag = np.sqrt(free[3]+off[0]**2+off[1]**2+off[2]**2)
#
#print "off0 ", off
#print "mag0 ", mag

d[0] *= 1e-4    # convert to mT
d[1] *= 1e-4
d[2] *= 1e-4
d[3] *= 1e-4

(off0, b0, free0) = calcFreescale(d[0])
(off1, b1, free1) = calcFreescale(d[1])
(off2, b2, free2) = calcFreescale(d[2])
(off3, b3, free3) = calcFreescale(d[3])

(h0,s0,hs0) =calcHardSoft(d[0])
(h1,s1,hs1) =calcHardSoft(d[1])
(h2,s2,hs2) =calcHardSoft(d[2])
(h3,s3,hs3) =calcHardSoft(d[3])


print "\noff0: ", off0
print "off1: ", off1
print "off2: ", off2
print "off3: ", off3
print "\nb0: ", b0
print "b1: ", b1
print "b2: ", b2
print "b3: ", b3

meanB = (b0+b1+b2+b3)/4
scale0 = meanB/b0
scale1 = meanB/b1
scale2 = meanB/b2
scale3 = meanB/b3

print "scale0 ", scale0
print "scale1 ", scale1
print "scale2 ", scale2
print "scale3 ", scale3


diffFree = calcDif(free0,b0)
diffHs = calcDif(hs0[0],b0)


''' plotting for .tex '''
plt.close('all')

dFree = free0
bFree = b0
dHs = hs0[0]
raw = d[0]
#
#Direct input 
plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
#Options

params = {'text.usetex' : True,
          'font.size' : 11,
          'font.family' : 'lmodern',
          'text.latex.unicode': True,
          'figure.autolayout': True
          }
plt.rcParams.update(params) 

figHeight = 3
figWidth = 3
rad = 2
sh = 0.5
fig = plt.figure(figsize=(figWidth,figHeight),dpi=300)
#fig = plt.figure()
plt.axis('equal')
plt.grid(True)
plt.scatter(dFree[:,0],dFree[:,1],color='green', s=rad, alpha=sh)
plt.scatter(dHs[:,0], dHs[:,1],color='cyan', s=rad, alpha=sh)
plt.scatter(raw[:,0], raw[:,1],color='red', s=rad, alpha=sh)
circ = plt.Circle((0.,0.),bFree, fill=False, color='blue')
plt.axhline(0,0,1,c='k',ls='--')
plt.axvline(0,0,1,c='k',ls='--')
plt.gcf().gca().add_artist(circ)
plt.axis([ -0.06, 0.06, -0.07, 0.07])
plt.xlabel('measurements x-axis [mT]')
plt.ylabel('measurements y-axis [mT]')
plt.savefig("../thesis/pictures/plots/cali_xy.png", dpi=300)
#
fig = plt.figure(figsize=(figWidth,figHeight),dpi=300)
#fig = plt.figure()
plt.axis('equal')
plt.grid(True)
plt.scatter(dFree[:,1],dFree[:,2],color='green', s=rad, alpha=sh)
plt.scatter(dHs[:,1], dHs[:,2],color='cyan', s=rad, alpha=sh)
plt.scatter(raw[:,1], raw[:,2],color='red', s=rad, alpha=sh)
circ = plt.Circle((0.,0.),bFree, fill=False, color='blue')
plt.axhline(0,0,1,c='k',ls='--')
plt.axvline(0,0,1,c='k',ls='--')
plt.gcf().gca().add_artist(circ)
plt.axis([ -0.06, 0.06, -0.07, 0.07])
plt.xlabel('measurements y-axis [mT]')
plt.ylabel('measurements z-axis [mT]')
#plt.savefig("../thesis/pictures/plots/cali_yz.png", dpi=500)
#
#
#
fig = plt.figure(figsize=(6,3),dpi=300)
ax = plt.subplot(121)
ax.grid(True)
ax.axis('equal')
ax.scatter(dFree[:,0],dFree[:,2],color='green', s=rad, alpha=sh, label='Freescale')
ax.scatter(dHs[:,0], dHs[:,2],color='cyan', s=rad, alpha=sh, label='Naive appr.')
ax.scatter(raw[:,0], raw[:,2],color='red', s=rad, alpha=sh, label='Raw')
circ = plt.Circle((0.,0.),bFree, fill=False, color='blue')
ax.axhline(0,0,1,c='k',ls='--')
ax.axvline(0,0,1,c='k',ls='--')
ax.add_artist(circ)
ax.set_xlabel('measurements x-axis [mT]')
ax.set_ylabel('measurements z-axis [mT]')
ax.legend(loc='upper center', bbox_to_anchor=(1.5,1))
plt.savefig("../thesis/pictures/plots/cali_xz.png", dpi=300)




fig = plt.figure(figsize=(4,3), dpi=300)
plt.hist([diffFree, diffHs], color=['green', 'cyan'], histtype='bar', label=['Freescale','Naive appr.'])
plt.xlabel(r'Deviation [$\%$]')
plt.legend(loc='left')
plt.text(-9, 150, r'$\mu_{Free}$=-0.02 \%', color='green')
plt.text(-9, 135, r'$\sigma_{Free}$=4.75', color='green')
plt.text(-9, 115, r'$\mu_{Naive}$=-0.8 \%', color='blue')
plt.text(-9, 100, r'$\sigma_{Naive}$=5.76', color='blue')
plt.savefig("../thesis/pictures/plots/cali_devi.png", dpi=300)







''' inet approach... '''
#(offset, scale) = calibrate(d[0])
#print "offset: ", offset
#print "scale: ",scale

''' determine the deviation of the collected min and max values '''
# values from 160111
#minValuesA = np.array([[-383.265899, -424.644134, -484.022399],
#                      [-397.618103, -439.450225, -488.259124],
#                      [-375.511627, -439.803649, -481.366638]])
#maxValuesA = np.array([[438.796539, 389.688110, 340.282287],
#                      [420.101837, 397.117309, 337.497558],
#                      [455.424255, 405.229278, 338.208709]])
#
## values from 160115
#minValues = np.array([[-387.834869, -414.776000, -481.082092],
#                      [-407.850067, -439.614166, -464.585784],
#                      [-404.837249, -447.333312, -476.074279],
#                      [-399.311187, -436.794494, -499.781158]])
#maxValues = np.array([[417.674530, 366.546234, 318.354431],
#                      [438.817718, 370.277496, 343.030700],
#                      [432.838745, 386.539398, 339.903320],
#                      [441.337890, 374.317962, 319.793182]])                      
#
#minValues = np.concatenate((minValuesA,minValues))
#maxValues = np.concatenate((maxValuesA,maxValues))
#
#(mMin,dMin) = deviation(minValues)
#(mMax,dMax) = deviation(maxValues)
#
#print "mean Min\n", mMin
#print "mean Max\n", mMax
#print "deviation Min [%]\n", dMin*100
#print "deviation Max [%]\n", dMax*100
#
#(hard,soft) = calcHardSoft(np.concatenate(([mMin],[mMax])))
#print "hard of mean ", hard
#print "soft of mean ",soft
#
#frees = calcFreescale(np.concatenate(([mMin],[mMax])))
#print "Freescale hard values of mean ",frees



        
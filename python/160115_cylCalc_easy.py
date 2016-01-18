import modelCyl as modC
import modelEqMultiCython as modE
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np
import time

l_mag = 0.015
r_mag = 0.0025

''' FLAT CASE 
    (angle stays constant, only movement in lateral or radial) '''

#a = modC.calcB_cyl(np.array([0.04, 0.06]), -(np.pi/2))
#print [round(a[0],5), round(a[1],5)]

''' verify that everything works as it should... '''
r = np.arange(0.05,0.1,0.0005)
#r = np.arange(-0.02, 0.02, 0.001)
rr = r[::-1]
a = np.arange(0, 2*np.pi, 0.1)
#a = np.arange(-np.pi/2., 0, 0.01)
#a = a[::-1]
b_cylA = np.zeros((len(a),2))
b_cyl1 = np.zeros((len(r),2))
pos1 = np.zeros((len(r),2))
b_cyl2 = np.zeros((len(r),2))
pos2 = np.zeros((len(r),2))
#b_bar = np.zeros((len(r),))
b_dip = np.zeros((len(r),3))
cnt = 0

pPos = np.zeros((len(r),2))

for i in r:
#    b_bar[cnt] = modE.barMagnet(i)
#     b_cyl1[cnt] = modC.calcB_cyl(np.array([0.06+l_mag/2, i]), np.pi*(0./2.))
#     b_cyl2[cnt] = modC.calcB_cyl(np.array([0.06, i]), np.pi*(-1./2.))
     b_cyl1[cnt] = modC.calcB_cyl(np.array([i, 0]), 0)*[1, -1]
     b_cyl2[cnt] = modC.calcB_cyl(np.array([0, i]), np.pi/2)*[1, -1]
#    b_cyl[cnt] = modC.calcBHand()
#    b_dip[cnt] = modE.calcB(np.array([-rr[cnt], 0, 0]), np.array([1, 0, 0]))  
#    pPos[cnt] = np.array([0, i])
     cnt += 1
  
print "b_cyl1[0]\n", b_cyl1[0]
print "b_cyl2[0]\n", b_cyl2[0]
    
cnt = 0
for i in a:
    b_cylA[cnt] = modC.calcB_cyl(np.array([r[0], 0]), i)        
    cnt += 1
    
#a = modC.calcB_cyl(np.array([r[0], 0]), np.pi/2)
    
#plt.close('all')    
#plt.figure()
#plt.plot(r,b_bar,'r')    
#plt.title('bar Magnet')
#plt.figure()
#plt.plot(a,b_cyl[:,0],'r',a,b_cyl[:,1],'g')    
#plt.scatter(r,b_cyl1[:,0])
plo.plotter2d((b_cyl1,b_cylA,b_cyl2),("B one","B angle","B two"), shareAxis=True)
#plt.figure()
#plo.plotter2d((pos1,pos2),("POS 1", "POS 2"))
#plt.plot(a,b_cyl[:,0],'r',a,b_cyl[:,1],'g')    
#plt.title('cyl formula')
#plt.figure()
#plt.plot(r,b_dip[:,0],'r',r,b_dip[:,1],'g',r,b_dip[:,2],'b')    
#plt.title('dip formula')

''' estimation things '''
#a = modC.estimatePos_cyl(np.array([0.04, 0]), 0, b_cyl[1])      # perfect pos for b_cyl[1]: [r[1],0]
#a = modC.estimatePos_cyl(np.array([0, 0]), 0, b_cyl1[1])
#print "RESULT:\n", a

estPos = np.zeros((len(r),2))

cnt = 0
errCnt = 0
startT = time.time()
for i in b_cyl2[1:]:
    print "estimating ", cnt    
    tmp = modC.estimatePos_cyl(estPos[cnt], np.pi/2, i)    
    estPos[cnt+1] = tmp[0]
    
#    if not tmp.success:
#        print "error in step ", cnt
#        print tmp.fun
#        errCnt += 1
    
    cnt += 1
print "time needed: ", time.time()-startT  
##        
plt.figure()
plt.plot(r, estPos[:,0],'r', r, estPos[:,1],'g')  
plt.title('estimated positions')
#plt.figure()
#plt.plot(r, pPos[:,0],'r', r, pPos[:,1],'g')  
#plt.title('perfect positions')

plt.show()
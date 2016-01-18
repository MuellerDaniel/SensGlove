import modelCyl as modC
import modelEqMultiCython as modE
import plotting as plo
import matplotlib.pyplot as plt
import numpy as np
import time

#a = modC.calcB_cyl(np.array([0.04, 0.06]), -(np.pi/2))
#print [round(a[0],5), round(a[1],5)]

''' verify that everything works as it should... '''
r = np.arange(0.05,0.1,0.0005)
a = np.arange(0, np.pi/2, 0.01)
b_cyl = np.zeros((len(a),2))
#b_bar = np.zeros((len(r),))
b_dip = np.zeros((len(r),3))
cnt = 0
startT = time.time()
for i in r:
#    b_bar[cnt] = modE.barMagnet(i)
#    b_cyl[cnt] = modC.calcB_cyl(np.array([i, 0]), np.pi/2)
    b_dip[cnt] = modE.calcB(np.array([i, 0, 0]), np.array([1, 0, 0]))    
    cnt += 1
print "time needed: ", time.time()-startT    
    
cnt = 0
for i in a:
    print "here! ", cnt
    b_cyl[cnt] = modC.calcB_cyl(np.array([r[0], 0]), i)        
    cnt += 1
    
#a = modC.calcB_cyl(np.array([r[0], 0]), np.pi/2)
    
plt.close('all')    
#plt.figure()
#plt.plot(r,b_bar,'r')    
#plt.title('bar Magnet')
plt.figure()
#plt.plot(r,b_cyl[:,0],'r',r,b_cyl[:,1],'g')    
plt.plot(a,b_cyl[:,0],'r',a,b_cyl[:,1],'g')    
plt.title('cyl formula')
plt.figure()
plt.plot(r,b_dip[:,0],'r',r,b_dip[:,1],'g',r,b_dip[:,2],'b')    
plt.title('dip formula')
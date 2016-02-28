import dataAcquisitionMulti as datAc
import numpy as np
import matplotlib.pyplot as plt
import plotting as plo
import modelDip_A as modD
import modelCyl_A as modC
import handDim as h
from scipy.optimize import *

''' estimate x position again '''
def b1d(x):
    Br = 1260
    r_mag = 0.0025
    l_mag = 0.015
    b_mag = l_mag/2

    return (Br/2)*((x+b_mag)/np.sqrt(r_mag**2+(x+b_mag)**2) - (x-b_mag)/np.sqrt(r_mag**2+(x-b_mag)**2));

def objFun(xGuess,b):
    dif = (b-b1d(xGuess))
    dif = np.linalg.norm(dif)
    return dif

def estB(x0, b):
    res = minimize(objFun, x0, args=(b,), tol=1e-14, method='slsqp',bounds=((0.0,0.2),))
#    res = minimize(objFun, x0, args=(b,))
#    print res    
    return res


''' for x-movement '''
t = np.arange(0.06,0.11,(0.05/62))

b_cyl = np.zeros((len(t),3))
b_dip = np.zeros((len(t),3))

cnt = 0
for i in t:
    b_cyl[cnt] = modC.calcB_cyl(np.array([i, 0.,0.]),np.array([0., 0.]))*1e+3
    b_dip[cnt] = modD.calcB(np.array([i,0.,0.]),np.array([1, 0, 0]))*1e+3
    
    cnt += 1
    

d = datAc.textAcquisition("151216_xMove")[0]*1e-4  
meas = d[9:71]

''' meas fitting '''
range_m = max(meas[:,0]) - min(meas[:,0])
range_s = max(b_cyl[:,0]) - min(b_cyl[:,0])
scaleMeas = range_s/range_m
meas = meas[:,0]*scaleMeas
offsetMeas = b_cyl[0][0] - meas[0]
meas = meas + offsetMeas

meas *= 1

''' re-estimation '''
estCyl = np.zeros((len(b_cyl[1:]),1))
estCyl[0] = t[0]
for i in range(1,len(b_cyl[1:]),1):
    r = estB(estCyl[i-1], b_cyl[i][0])    
    estCyl[i] = r.x

estDip = np.zeros((len(b_dip[1:]),1))
estDip[0] = t[0]
for i in range(1,len(b_dip[1:]),1):
    r = estB(estDip[i-1], b_dip[i][0])    
    estDip[i] = r.x
    
estMeas = np.zeros((len(meas[1:]),1))
estMeas[0] = t[0]
for i in range(1,len(meas[1:]),1):
    r = estB(estMeas[i-1], meas[i])    
    estMeas[i] = r.x


''' deviation calculation '''    
diff_dip = b_cyl[:,0]-b_dip[:,0]
diff_meas = b_cyl[:,0] - meas

''' plotting '''
plt.close('all')

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

figHeight = 6
figWidth = 5
fig = plt.figure(figsize=(figWidth,figHeight),dpi=500)
#fig = plt.figure()
xTime = np.arange(0,3.1,0.05)
t = xTime

# magnetic field
a = plt.subplot(311)
a.plot(t,b_cyl[:,0],'r',label="Cylindrical model")
a.plot(t,b_dip[:,0],'g',label="Dipole model")
a.plot(t,meas,'b',label="Measurements")
plt.setp(a.get_xticklabels(), visible=False) # make x-ticks invisible
plt.legend(loc="lower right", bbox_to_anchor=(1.1,1), ncol=2)
a.set_ylabel('B-field [mT]')

# deviation from cylindrical
b = plt.subplot(312, sharex=a)
#b.stem(t,diff_dip*con,'color','g')
b.plot(t,diff_dip,'g',label='Dipole model')
b.plot(t,diff_meas,'b', label='Measurements')
#plt.legend(loc="lower right",bbox_to_anchor=(1.1,0.4))
b.set_ylabel('Deviation\nfrom cylindrical [mT]')

# re-estimated states
c = plt.subplot(313, sharex=a)
c.plot(t[:-1],estCyl*100,'r', label="Cylindrical")
c.plot(t[:-1],estDip*100,'g', label=" Dipole")
c.plot(t[:-1],estMeas*100,'b', label="Measurements")
#plt.legend(loc='lower right',bbox_to_anchor=(1.1,-0.01))
c.set_xlabel('Time [sec]')
c.set_ylabel('Corresponding\nPosition [cm]')

plt.subplots_adjust(hspace=0.3)

plt.savefig("../thesis/pictures/plots/compX.png", dpi=300, bbox_inches='tight')

''' DO IT FOR A 90 MCP MOVEMENT AS WELL! '''
##sensList = [h.sInd,h.sMid,h.sRin,h.sPin]
#sensList = [h.sInd]
#fingList = [h.phalInd]
#jointList = [h.jointInd]
#
#''' 90deg fitting values '''
#t90 = np.arange(0,np.pi/2,((np.pi/2)/82))       # describing the angles
##a = np.arange(0,np.pi*(110./180),(np.pi*(110./180))/16)
#angles90 = np.zeros((len(t90),3*len(fingList)))
#cnt = 0
#for i in t90:
#    angles90[cnt] = np.array([i, 0., 0.])#,     # moving only MCP
##                            i, 0. ,0.,
##                            i, 0. ,0.,
##                            i, 0. ,0.])
#        
#    cnt += 1
#    
#b90_c = np.zeros((len(t90), 3*len(sensList)))
#b90_d = np.zeros((len(t90), 3*len(sensList)))    
#
#cnt = 0
#for i in range(len(t90)):
#    b90_c[i] = modC.angToB_cyl(angles90[i],fingList,sensList,jointList)*1e+3    # simulating model without ad-ab
#    b90_d[i] = modD.angToBm(angles90[i],fingList,sensList,jointList)*1e+3              # simulating model with ad-ab
#
#
#sString = 'set4'
#(tim, s1, s2, s3, s4) = datAc.readMag("../datasets/160210/160210_"+sString+"_mag")
#s1 *= 1e+3
#print "fitting for 90"
#start = 93
#end = 175
#(scale, off) = datAc.getScaleOff(b90_c[:,:3],s1[start:end]) 
#s1_fit = s1*scale+off
##plo.plotter2d((b90_c[:,:3], s1_fit[start:end], s1[start:end]),("sim1", "fitted", "meas"),shareAxis=True)
#
#''' deviation '''
#diff_dipH = b90_c-b90_d
#diff_measH = b90_c-s1_fit[start:end]
#
#''' plotting '''
#figHeight = 5
#figWidth = 6
#fig = plt.figure(figsize=(figWidth,figHeight),dpi=500)
#
#a = plt.subplot(211)
#
#sX, = a.plot(np.arange(0,6e-5,16e-1),'k-',label='x')
#sY, = a.plot(np.arange(0,6e-5,16e-1),'k--',label='y')
#sZ, = a.plot(np.arange(0,6e-5,16e-1),'k:',label='z')
#
#a.plot(t90,b90_c[:,0],'r-',label='Cylindrical model')
#a.plot(t90,b90_c[:,1],'r--')
#a.plot(t90,b90_c[:,2],'r:')
#
#a.plot(t90,b90_d[:,0],'g-', label='Dipole model')
#a.plot(t90,b90_d[:,1],'g--')
#a.plot(t90,b90_d[:,2],'g:')
#
#a.plot(t90,s1_fit[start:end][:,0],'b-', label='Measurements')
#a.plot(t90,s1_fit[start:end][:,1],'b--')
#a.plot(t90,s1_fit[start:end][:,2],'b:')
#a.set_ylabel('B-field [mT]')
#plt.legend(loc='upper center',ncol=2, bbox_to_anchor=(0.7,1.4))#,bbox_to_anchor=(0.5,0.7))
#
#b = plt.subplot(212, sharex=a)
#b.plot(t90,diff_dipH[:,0],'g-', label='Deviation of dipole model')
#b.plot(t90,diff_dipH[:,1],'g--')
#b.plot(t90,diff_dipH[:,2],'g:')
#
#b.plot(t90,diff_measH[:,0],'b-', label='Deviation of measurements')
#b.plot(t90,diff_measH[:,1],'b--')
#b.plot(t90,diff_measH[:,2],'b:')
#b.set_ylabel('B-field [mT]')
#b.set_xlabel(r'$\theta_{MCP}$ [rad]')
#plt.legend(loc="lower right")
#plt.savefig("../thesis/pictures/plots/compFing.png", dpi=500,bbox_inches='tight')


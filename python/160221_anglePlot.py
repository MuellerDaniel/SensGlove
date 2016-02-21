import numpy as np
import modelCyl_A as modC
import modelDip_A as modD
import handDim as h
import plotting as plo
import matplotlib.pyplot as plt
import jacB_fourfourA as jffA
import jacB_onefourA as jofA
import jacB_oneoneA as jooA
import time
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

''' simulating and estimating with the models '''

sensList0 = [h.sInd,h.sPin]
fingList0 = [h.phalInd]
jointList0 = [h.jointInd]

sensList1 = [h.sMid,h.sPin]
fingList1 = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
jointList1 = [h.jointInd,h.jointMid,h.jointRin,h.jointPin]

sensList2 = [h.sInd]
fingList2 = [h.phalInd]
jointList2 = [h.jointInd]

sensList3 = [h.sMid, h.sPin]
fingList3 = [h.phalInd,h.phalMid,h.phalRin,h.phalPin]
jointList3 = [h.jointInd,h.jointMid,h.jointRin,h.jointPin]

''' simulation '''
#t = np.arange(0,np.pi*(110./180),0.1)       # describing the angles
t = np.arange(0,np.pi*(1./2.), 0.1)
ad = np.arange((-30/180.)*np.pi,(30/180.)*np.pi,((30/180.)*np.pi*2./16.))

angles0 = np.zeros((len(t),3*len(fingList0)))
angles1 = np.zeros((len(t),3*len(fingList1)))
angles2 = np.zeros((len(t),3*len(fingList2)))
angles3 = np.zeros((len(t),3*len(fingList3)))

cnt = 0
for i in t:
    angles0[cnt] = np.array([i, 0. ,0.])#,     # moving only MCP

    angles1[cnt] = np.array([i, i ,0.,     # moving only MCP
                            i, i ,0.,
                            i, i ,0.,
                            i, i ,0.])  
                            
    angles2[cnt] = np.array([0.,0.,ad[cnt]])     

    angles3[cnt] = np.array([0, 0 ,0.,     # moving only MCP
                            i, i ,0.,
                            i, i ,0.,
                            i, i ,0.])
                       
    cnt += 1
    
b0 = np.zeros((len(t), 3*len(sensList0)))
b1 = np.zeros((len(t), 3*len(sensList1)))
b2 = np.zeros((len(t), 3*len(sensList2)))
b3 = np.zeros((len(t), 3*len(sensList3)))

cnt = 0
for i in range(len(t)):
    b0[i] = modC.angToB_cyl(angles0[i],fingList0,sensList0,jointList0)*1e+3    # simulating cylindrical model
    b1[i] = modC.angToB_cyl(angles1[i],fingList1,sensList1,jointList1)*1e+3
    b2[i] = modC.angToB_cyl(angles2[i],fingList2,sensList2,jointList2)*1e+3
    b3[i] = modC.angToB_cyl(angles3[i],fingList3,sensList3,jointList3)*1e+3

''' b_cyl_Pin/b0: values for mInd and sInd/sPin for comparing the influence of an offset in y-direction '''
plt.close('all')

#Direct input 
plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
#Options
params = {'text.usetex' : True,
          'font.size' : 11,
          'font.family' : 'lmodern',
          'text.latex.unicode': True,
#          'figure.autolayout': True
          }
plt.rcParams.update(params) 

figHeight = 3
figWidth = 3
fig = plt.figure(figsize=(figWidth,figHeight),dpi=500)

#fig = plt.figure()
#a = plt.subplot(221)
#plt.subplots_adjust(hspace=4)
#plt.tight_layout(h_pad=4.0)

plt.plot(t,b0[:,0],'r-')#, label=r'$s_{Index}$')
plt.plot(t,b0[:,1],'r--')
plt.plot(t,b0[:,2],'r:')


plt.plot(t,b0[:,3],'y-')#, label=r'$s_{Pinky}$')
plt.plot(t,b0[:,4],'y--')
plt.plot(t,b0[:,5],'y:')

plt.grid(True)
plt.xlabel(r'$\theta_{MCP}$ [rad]')
plt.ylabel('B -field [mT]')
#a.legend()
#plt.text(0,-0.2, 'a) index, comparing sInd and sPin',transform=a.transAxes)
plt.savefig("../thesis/pictures/plots/bInd.png", dpi=500)

''' b2: values for performing ad-ab only with index (sInd, mInd) '''
#figHeight = 3
#figWidth = 3
fig = plt.figure(figsize=(figWidth,figHeight),dpi=500)

plt.plot(ad,b2[:,0],'r-')#, label=r'$s_{Index}$')
plt.plot(ad,b2[:,1],'r--')
plt.plot(ad,b2[:,2],'r:')
plt.axis([ad[0], ad[-1], -0.03, 0.04])
plt.grid(True)
plt.xlabel(r'$\phi_{MCP}$ [rad]')
plt.ylabel('B -field [mT]')
#b.legend()
#plt.text(0.1,-0.2, 'b) index, ad-ab',transform=.transAxes)
plt.savefig("../thesis/pictures/plots/bInd_A.png", dpi=500)


''' b_fist/b1: values at sMid and sPin for performing a fist with all magnets '''
figHeight = 3
figWidth = 7
fig = plt.figure(figsize=(figWidth,figHeight),dpi=500)

c = plt.subplot(121)
c.plot(t,b1[:,0],'g-')#, label=r'$s_{Mid}$')
c.plot(t,b1[:,1],'g--')
c.plot(t,b1[:,2],'g:')

plt.grid(True)
c.plot(t,b1[:,3],'y-')#, label=r'$s_{Pinky}$')
c.plot(t,b1[:,4],'y--')
c.plot(t,b1[:,5],'y:')

c.set_xlabel(r'$\theta_{MCP}$ and $\theta_{PIP}$ [rad]')
c.set_ylabel('B -field [mT]')
#c.legend()
#c.text(0.2,-0.2, 'c) making fist',transform=c.transAxes)

lineX, = c.plot(np.arange(0,6e-5,16e-1),'k-',label='x')
lineY, = c.plot(np.arange(0,6e-5,16e-1),'k--',label='y')
lineZ, = c.plot(np.arange(0,6e-5,16e-1),'k:',label='z')
linePinky = mlines.Line2D([], [], color='yellow',
                          markersize=15, label=r'$s_{Pinky}$')
lineIndex = mlines.Line2D([], [], color='red',
                          markersize=15, label=r'$s_{Index}$')                          
lineMid = mlines.Line2D([], [], color='green',
                          markersize=15, label=r'$s_{Middle}$')
                          
plt.figlegend((lineX,lineY,lineZ, lineIndex,lineMid,linePinky),
              ('x','y','z', r'$s_{Index}$',r'$s_{Mid}$',r'$s_{Pinky}$'),
                loc='center right', bbox_to_anchor=(0.75,0.55))


plt.savefig("../thesis/pictures/plots/bFist.png", dpi=500)

''' b3:  '''

#plo.plotter2d((b_dip[:,:3], b_dip[:,3:6], b_dip[:,6:9], b_dip[:,9:]),
#              ("dipole index","dipole middle","dipole ring","dipole pinky"))
#plo.plotter2d((b_cyl[:,:3], b_cyl[:,3:6], b_cyl[:,6:9], b_cyl[:,9:]),
#              ("cyl index","cyl middle","cyl ring","cyl pinky"))  




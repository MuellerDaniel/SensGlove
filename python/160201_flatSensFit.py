import numpy as np
import modelDip as modD
import modelCyl as modC
import plotting as plo
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import dataAcquisitionMulti as datAc


def meanScale(li):
    s = np.zeros((4,3))
    for i in range(4):  # iterating through all four sensors
        for j in range(3):      # iterating through three axes
            for k in range(len(li)):    # iterating through all scales
                s[i][j] += li[k][i][j]
                
    return s/len(li)


''' simulation of perfect data '''
l_mag = 0.015
r_mag = 0.0025

h0  = np.array([1.,0.,0.])
h90 = np.array([0.,1.,0.])

# s0 is the origin
s0 = np.array([0.,  0.,   0.])
s1 = np.array([0., -0.02, 0.])
s2 = np.array([0., -0.04, 0.])
s3 = np.array([0., -0.06, 0.])

zOff = np.array([0., 0., 0.02+0.0067])

#r = np.arange(0.05, 0.1, 0.001)
#r = np.arange(-0.06, 0., 0.001)

r = np.concatenate((np.arange(-0.06, -0.04, 0.001),
                    np.ones((15,))*-0.04, 
                    np.arange(-0.04, -0.02, 0.001),
                    np.ones((15,))*-0.02,
                    np.arange(-0.02,0.,0.001)))

p_dip = np.zeros((len(r),3))

cnt = 0
for i in r:
#    p_dip[cnt] = np.array([i, 0., 0.])
    p_dip[cnt] = np.array([0.07+0.01+l_mag/2, i, r_mag])    
    
    cnt += 1
#plo.plotter2d((p_dip,),("p",))

b_dip0 = np.zeros((len(r),3))    
b_dip1 = np.zeros((len(r),3))    
b_dip2 = np.zeros((len(r),3))    
b_dip3 = np.zeros((len(r),3))    
b_cyl0 = np.zeros((len(r),3))    
b_cyl1 = np.zeros((len(r),3))    
b_cyl2 = np.zeros((len(r),3))    
b_cyl3 = np.zeros((len(r),3))  

tmp = np.zeros((len(r),3))  
cnt = 0
for i in p_dip:
    b_dip0[cnt] = modD.calcB(i-(s0+zOff), h0)
    b_dip1[cnt] = modD.calcB(i-(s1+zOff), h0)
    b_dip2[cnt] = modD.calcB(i-(s2+zOff), h0)
    b_dip3[cnt] = modD.calcB(i-(s3+zOff), h0)
        
    b_cyl0[cnt] = modC.calcB_cyl(i-(s0+zOff), 0.)
    b_cyl1[cnt] = modC.calcB_cyl(i-(s1+zOff), 0.)
    b_cyl2[cnt] = modC.calcB_cyl(i-(s2+zOff), 0.)
    b_cyl3[cnt] = modC.calcB_cyl(i-(s3+zOff), 0.)
    
    tmp[cnt] = (i-(s0+zOff))
    
#    b_dip0[cnt] = modD.calcB(i, h0)
#    b_cyl0[cnt] = modC.calcB_cyl(i, 0.)
   
    
    cnt += 1
    
#plo.plotter2d((b_dip0, b_dip1, b_dip2, b_dip3), ("DIP 0", "1", "2", "3"), shareAxis=False)        
#plo.plotter2d((b_cyl0, b_cyl1, b_cyl2, b_cyl3), ("CYL 0", "1", "2", "3"))

#plo.plotter2d((tmp,),("a",))
''' fitting of measured data '''
#d = datAc.textAcquisition("160208_flatFit1")
d = datAc.textAcquisition("160212_flatSens7")
#d = datAc.textAcquisition("160212_flatSens5")

#d[0] -= [  92.87515152,  286.92060606, -318.85131313]   # for 160201_s1_x5-10 
#d[1] -= [  46.86343434,  276.33575758, -423.56191919]
#d[2] -= [  47.29494949,  264.67717172, -422.53242424]
#d[3] -= [  74.65848485,  233.96656566, -403.30909091]

#d[0] -= [  95.95686869,  288.99565657, -316.52959596]   # for 160201_y4-0_x5 - 160201_y4-0_x7_2
#d[1] -= [  49.74555556,  276.99181818, -424.61929293]
#d[2] -= [  50.31323232,  265.79050505, -421.99272727]
#d[3] -= [  77.2389899 ,  235.17080808, -403.23666667]

#d[0] -= [ -41.76743719,  252.39633166, -391.40733668]   # for 160208
#d[1] -= [ -55.70944724 , 230.11417085, -402.72698492]
#d[2] -= [ -60.59075377 , 213.51316583, -400.75899497]
#d[3] -= [ -64.57613065 , 200.6280402 , -406.90467337]

#d[0] -= [  54.48904523 , 255.4001005 , -448.39547739]     # for 160212
#d[1] -= [ -15.48708543 , 207.15371859,  -54.84949749]
#d[2] -= [ -58.60231156 , 229.55512563, -419.81487437]
#d[3] -= [ -44.00075377 , 220.07562814, -298.0879397 ]

d[0] *= 1e-7
d[1] *= 1e-7
d[2] *= 1e-7
d[3] *= 1e-7

start = 23      # for 160212_flatSens7
end = 115
p = np.zeros((4,115-23,3))

#start = 32      # for 160212_flatSens5
#end = 124
#p = np.zeros((4,124-32,3))

p[0] = d[0][start:end]
p[1] = d[1][start:end]
p[2] = d[2][start:end]
p[3] = d[3][start:end]

#p = d

#scaled0 = datAc.scaleMeasurements(b_dip0,p[0])
#scaled1 = datAc.scaleMeasurements(b_dip1,p[1])
#scaled2 = datAc.scaleMeasurements(b_dip2,p[2])
#scaled3 = datAc.scaleMeasurements(b_dip3,p[3])

(scale0, off0) = datAc.getScaleOff(b_dip0, p[0])
scaled05 = p[0]*np.array([1.20967052,  1.26494698 , 1.13013986])
off05 = np.array([b_dip0[0][0]-scaled05[0][0],
                  b_dip0[0][1]-scaled05[0][1],
                  b_dip0[0][2]-scaled05[0][2]])
scaled05 += off05    

scaled0 = p[0]*scale0 + off0

unscaled = p[0]
offUn = np.array([b_dip0[0][0]-unscaled[0][0],
                  b_dip0[0][1]-unscaled[0][1],
                  b_dip0[0][2]-unscaled[0][2]])
unscaled += offUn                  

#(scale1, off1, scaled1) = datAc.getScaleOff(b_dip1, p[1])
#scaled1 = p[1]*scale1+off1
#
#(scale2, off2, scaled2) = datAc.getScaleOff(b_dip2, p[2])
#scaled2 = p[2]*scale2+off2
#
#(scale3, off3, scaled3) = datAc.getScaleOff(b_dip3, p[3])
#scaled3 = p[3]*scale3+off3

#meanS = np.array([[ 0.52923734,  0.55621392,  0.54862538],      # mean of the scaled values
#                   [ 0.52998248,  0.54820189,  0.48811477],     # 160201_y4-0_x5 - 160201_y4-0_x7_2
#                   [ 0.61741302,  0.53209969,  0.55071248],
#                   [ 0.59696768,  0.49537316,  0.52832493]])
#                   
#scaled0 = d[0]*meanS[0]                   
#scaled1 = d[1]*meanS[1]                   
#scaled2 = d[2]*meanS[2]                   
#scaled3 = d[3]*meanS[3]                   

#plo.plotter2d((d[0], d[1], d[2], d[3]), ("meas 0", "1", "2", "3"))   
plt.close('all') 
#plo.plotter2d((b_dip0, scaled0, p[0]), ("model 0", "scaled 0", "raw"))
#plo.plotter2d((b_dip1, scaled1, p[1]), ("model 1", "scaled 1", "raw"))
#plo.plotter2d((b_dip2, scaled2, p[2]), ("model 2", "scaled 2", "raw"))
#plo.plotter2d((b_dip3, scaled3, p[3]), ("model 3", "scaled 3", "raw"))

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

con = 1e+3

figHeight = 5
figWidth = 6
fig = plt.figure(figsize=(figWidth,figHeight),dpi=500)
ax = plt.subplot(212)

sX, = ax.plot(np.arange(0,6e-5,16e-1),'k-',label='x')
sY, = ax.plot(np.arange(0,6e-5,16e-1),'k--',label='y')
sZ, = ax.plot(np.arange(0,6e-5,16e-1),'k:',label='z')

lineSim, = ax.plot(b_dip0[:,0]*con,'r-',label='simulated data')
ax.plot(b_dip0[:,1]*con,'r--',b_dip0[:,2]*con,'r:')

lineS7, = ax.plot(scaled0[:,0]*con,'b-', label='scaled with factors from x=7cm')
ax.plot(scaled0[:,1]*con,'b--',scaled0[:,2]*con,'b:')

lineS5, = ax.plot(scaled05[:,0]*con,'g-', label='scaled with factors from x=5cm')
ax.plot(scaled05[:,1]*con,'g--',scaled05[:,2]*con,'g:')

lineUs, = ax.plot(unscaled[:,0]*con,'c-', label='unscaled')
ax.plot(scaled05[:,1]*con,'c--',scaled05[:,2]*con,'c:')
ax.set_ylabel(r'B-field [mT]')
ax.set_xlabel('y position [m]')
ax.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5,1.7))
plt.savefig("../thesis/pictures/plots/flatFit.png", dpi=500)


plt.show()
    

    
    
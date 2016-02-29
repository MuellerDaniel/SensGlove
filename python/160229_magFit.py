import matplotlib.pyplot as plt
import dataAcquisitionMulti as datAc
import plotting as plo
import numpy as np
import matplotlib.lines as mlines
from matplotlib.image import BboxImage,imread
from matplotlib.transforms import Bbox

sstring = 'set1'    
dayString = '160210'
magFile = "../datasets/"+dayString+'/'+dayString+'_'+sstring+"_mag"
(tMag,s1,s2,s3,s4) = datAc.readMag(magFile)


s = 0
e = 450
tMag = tMag[s:e]
s1 *= 1e+3
s1 = s1[s:e]

plt.close('all')

###Direct input
#plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
##Options
#params = {'text.usetex' : True,
#         'font.size' : 11,
#         'font.family' : 'lmodern',
#         'text.latex.unicode': True,
#         'figure.autolayout': True
#         }
#plt.rcParams.update(params)
##    
#figHeight = 5
#figWidth = 5
#    
#fig = plt.figure(figsize=(figWidth,figHeight),dpi=300)   
plt.figure()
#
#ax = fig.add_axes([0,0,figWidth,figHeight],frameon=False)


plt.xlim((tMag[0],tMag[-1]))
plt.xticks(np.arange(0,tMag[-1], 3))
plt.plot(tMag,s1[:,0],'r', label='x')
plt.plot(tMag,s1[:,1],'g', label='y')
plt.plot(tMag,s1[:,2],'b', label='z')




plt.xlabel('Time [sec]')
plt.ylabel('B-field [mT]')

plt.legend()
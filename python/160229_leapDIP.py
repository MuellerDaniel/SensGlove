import matplotlib.pyplot as plt
import dataAcquisitionMulti as datAc
import plotting as plo
import numpy as np
import matplotlib.lines as mlines
from matplotlib.image import BboxImage,imread
from matplotlib.transforms import Bbox

sstring = 'set14'    

leapFile = "../datasets/evalSets/"+sstring+"_leap"
magFile = "../datasets/evalSets/"+sstring+"_mag"

(tLeap,ind,mid,rin,pin) = datAc.readLeap(leapFile)
#(tMag,s1,s2,s3,s4) = datAc.readMag(magFile)
s = 1300
e = -2700
tLeap = tLeap[s:e]

mcpf = ind[:,0][s:e]
pip = ind[:,1][s:e]
dip = ind[:,2][s:e]
mcpa= ind[:,3][s:e]

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
figHeight = 5
figWidth = 5
    
fig = plt.figure(figsize=(figWidth,figHeight),dpi=300)   
#plt.figure()
#
#ax = fig.add_axes([0,0,figWidth,figHeight],frameon=False)


plt.xlim((tLeap[0],tLeap[-1]))
# TODO format them to be without decimals!
plt.xticks(np.arange(tLeap[0],tLeap[-1],1))

#plt.plot(tLeap,mcpf,label=r'$\theta_{MCP}$')
plt.plot(tLeap,pip,'r', label=r'$\theta_{PIP}$')
plt.plot(tLeap,dip,'g', label=r'$\theta_{DIP}$')
plt.plot(tLeap,mcpa,'b', label=r'$\phi_{MCP}$')
plt.axhline(0.0,color='k')
# color the regions of interest!
plt.axvspan(tLeap[200],tLeap[350],color='y',alpha=0.5)  # region 0
plt.axvspan(tLeap[550],tLeap[700],color='y',alpha=0.5)  # region 1
plt.axvspan(tLeap[900],tLeap[1080],color='y',alpha=0.5)  # region 2

''' adding the pictures... '''
TICKYPOS = -.75
#plt.gca().get_xaxis().set_ticklabels([])


#    lowerCorner = difP.transData.transform((.8,TICKYPOS-.2))
#    upperCorner = difP.transData.transform((1.2,TICKYPOS+.2))
lowPos = [0,TICKYPOS-1.2]
upPos = [lowPos[0]+1.2,lowPos[1]+1.2]
print lowPos
print upPos
lowerCorner = plt.gca().transData.transform((lowPos[0],lowPos[1]))
upperCorner = plt.gca().transData.transform((upPos[0],upPos[1]))

# first
bbox_image0 = BboxImage(Bbox([[lowerCorner[0], lowerCorner[1]],
                             [upperCorner[0], upperCorner[1]]]),
                   norm = None,
                   origin=None,
                   clip_on=False,
                   )   
bbox_image0.set_data(imread('../thesis/pictures/statePics/set14/set14_0.jpg'))
plt.gca().add_artist(bbox_image0)                       
# second
#lowC1 = plt.gca().transData.transform((lowPos[0]+6.5,lowPos[1]))
#upC1 = plt.gca().transData.transform((upPos[0]+6.5,upPos[1]))
#bbox_image1 = BboxImage(Bbox([[lowC1[0], lowC1[1]],
#                             [upC1[0], upC1[1]]]),
#                   norm = None,
#                   origin=None,
#                   clip_on=False,
#                   )   
#bbox_image1.set_data(imread('../thesis/pictures/statePics/set14/set14_1.jpg'))
#plt.gca().add_artist(bbox_image1)
## third
#lowC2 = plt.gca().transData.transform((lowPos[0]+6.5,lowPos[1]))
#upC2 = plt.gca().transData.transform((upPos[0]+6.5,upPos[1]))
#bbox_image2 = BboxImage(Bbox([[lowC2[0], lowC2[1]],
#                             [upC2[0], upC2[1]]]),
#                   norm = None,
#                   origin=None,
#                   clip_on=False,
#                   )   
#bbox_image2.set_data(imread('../thesis/pictures/statePics/set14/set14_2.jpg'))
#plt.gca().add_artist(bbox_image2)


plt.ylabel('Angle [rad]')
plt.xlabel('Time [sec]')
plt.legend()
#plt.title('some...')

#plt.savefig("../thesis/pictures/plots/set14leap.png", dpi=300, bbox_inches='tight')                  
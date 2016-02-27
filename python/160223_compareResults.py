import numpy as np
import dataAcquisitionMulti as datAc
import plotting as plo
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def plotDif(inL):
    ''' inL : list
            [perfectStates, estimated1, estimated2, ...] '''

    colorL = ['r','g','b','y']
    styleL = ['solid','dashed','dotted','dash-dot']
    labelL = ['Defined states', 'Estimated states0', 'Estimated states1', 'Estimated states2']

    ##Direct input
    plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
    #Options
    params = {'text.usetex' : True,
             'font.size' : 11,
             'font.family' : 'lmodern',
             'text.latex.unicode': True,
             'figure.autolayout': True
             }
    plt.rcParams.update(params)

    figHeight = 5
    figWidth = 5

    fig = plt.figure(figsize=(figWidth,figHeight),dpi=300)
    # fig = plt.figure()

    # the plot of all states in one
    a = plt.subplot(221)
    a.set_ylabel('Finger states [rad]')
    plt.setp(a.get_xticklabels(), visible=False)

    lineMCP, = a.plot(np.arange(0,6e-5,16e-1),'k-',label=r'\theta_{MCP}')
    linePIP, = a.plot(np.arange(0,6e-5,16e-1),'k--',label=r'\theta_{PIP}')
    lineDIP, = a.plot(np.arange(0,6e-5,16e-1),'k:',label=r'\theta_{DIP}')
    linePHI, = a.plot(np.arange(0,6e-5,16e-1),'k-.',label=r'\phi_{MCP}')
    # if (inL[0].shape[1] == 4) lineAD =

    colorCnt = 0
    for i in inL:
        styleCnt = 0
        for state in i.T:
            a.plot(state,color=colorL[colorCnt],ls=styleL[styleCnt])
            styleCnt += 1
        colorCnt += 1

    # plot of normed differences
    colorCnt = 1
    b = plt.subplot(223, sharex = a)
    b.set_xlabel('Time [sec]')
    b.set_ylabel('Difference, normed [rad]')
    for i in inL[1:]:
        dif = inL[0] - i
        difNormed = np.linalg.norm(dif,axis=1)
        b.plot(difNormed, color=colorL[colorCnt])
        print "mean of normed differences of element %s: %s" % (colorCnt, np.mean(difNormed))
        colorCnt += 1

    linePerf = mlines.Line2D([], [], color=colorL[0],
                      markersize=15, label='Perfect States')
    lineEst = mlines.Line2D([], [], color=colorL[1],
                      markersize=15, label='Estimated States')

#    plt.figlegend((lineMCP,linePIP,lineDIP,linePHI,linePerf,lineEst),
#                    (r'$\theta_{MCP}$',r'$\theta_{PIP}$',r'$\theta_{DIP}$',r'$\phi_{MCP}$', 'Perfect States', 'Estimated States'),
#                    loc='center right',bbox_to_anchor=(1,0.3), ncol=1)

#    plt.savefig("../thesis/pictures/plots/difOne.png", dpi=300)
    return fig


def printMeanVar(est, sim):
    namelist = ['unconstr Dip A: ', 'unconstr Cyl A:',  'constr Dip A: ', 'constr Cyl A:', ]
    cnt = 0
    for i in est:
        dif = sim-i
        mean = np.mean(np.linalg.norm(dif, axis=1))
        var = np.var(dif)**2
        print "%s %s +- %s" % (namelist[cnt], mean, var)
        # print "var of "+namelist[cnt], var

        cnt += 1


def plotDif_sub(inL):
    ''' inL : list
            [perfectStates, estimated1, estimated2, ...] '''

    colorL = ['r','g','b','y']
    styleL = ['solid','dashed','dotted','dash-dot']
#    labelL = ['Defined states', 'Estimated states0', 'Estimated states1', 'Estimated states2']
    
    xTime = np.arange(0,70.9,0.05)
    
    strA = 'a) Comparison of the estimated with\nthe perfect states and the normed\ndifferences for each time step. The underlying estimation is done\nfor N=1, K=1, using the cylindrical model with constraints and phiMCP'    
    strB = 'b) Comparison of the estimated with\nthe perfect states\nand the normed difference for each time step.\nThe underlying estimation is done for N=2, K=1, using the cylindrical model with constraints and phiMCP'    
    
    ##Direct input
    plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
    #Options
    params = {'text.usetex' : True,
             'font.size' : 11,
             'font.family' : 'lmodern',
             'text.latex.unicode': True,
             'figure.autolayout': True
             }
    plt.rcParams.update(params)

    figHeight = 7
    figWidth = 6

    fig = plt.figure(figsize=(figWidth,figHeight),dpi=300)
#    fig = plt.figure()
    
    ''' plot of first set '''
    a = plt.subplot(423)    
    plt.setp(a.get_xticklabels(), visible=False)

    lineMCP, = a.plot(np.arange(0,6e-5,16e-1),'k-',label=r'\theta_{MCP}')
    linePIP, = a.plot(np.arange(0,6e-5,16e-1),'k--',label=r'\theta_{PIP}')
    lineDIP, = a.plot(np.arange(0,6e-5,16e-1),'k:',label=r'\theta_{DIP}')
    linePHI, = a.plot(np.arange(0,6e-5,16e-1),'k-.',label=r'\phi_{MCP}')
            
    colorCnt = 0    
    styleCnt = 0
    
    i = inL[0]
    for state in i.T:
        a.plot(xTime,state,color=colorL[colorCnt],ls=styleL[styleCnt])
        styleCnt += 1
    colorCnt += 1    
    
    styleCnt = 0    
    i = inL[1]
    for state in i.T:
        a.plot(xTime,state,color=colorL[colorCnt],ls=styleL[styleCnt])
        styleCnt += 1
    colorCnt += 1
    
    a.set_ylabel('Finger states [rad]')
    a.set_yticks(np.arange(-0.2,1.9,0.2))    

    # plot of normed differences
    colorCnt = 1
    b = plt.subplot(425, sharex=a)    
    i = inL[1]
    dif = inL[0] - i
    difNormed = np.linalg.norm(dif,axis=1)
    b.plot(xTime,difNormed, color=colorL[colorCnt])
    print "mean of normed differences of element %s: %s" % (colorCnt, np.mean(difNormed))
    colorCnt += 1
#    b.set_title('a) blabla bla', y=yTitle)
    b.set_xlabel('Time [sec]')
    b.set_ylabel('Difference, normed [rad]')
    b.set_yticks(np.arange(0.,0.5,0.1))
    
    b.text(0,-0.35, strA)
    b.text(100,-0.35, strB)

    ''' plot of second set '''
    c = plt.subplot(424, sharey=a, sharex=a)
    plt.setp(c.get_xticklabels(), visible=False)

    colorCnt = 0    
    styleCnt = 0
    
    i = inL[0]
    for state in i.T:
        c.plot(xTime,state,color=colorL[colorCnt],ls=styleL[styleCnt])
        styleCnt += 1
    colorCnt += 1    
    
    styleCnt = 0
    i = inL[2]
    for state in i.T:
        c.plot(xTime,state,color=colorL[colorCnt],ls=styleL[styleCnt])
        styleCnt += 1
    colorCnt += 1
    
    # plot of normed differences
    colorCnt = 1
    d = plt.subplot(426, sharex=a, sharey=b)
    d.set_xlabel('Time [sec]')
#    d.set_ylabel('Difference, normed [rad]')
    i = inL[2]
    dif = inL[0] - i
    difNormed = np.linalg.norm(dif,axis=1)
    d.plot(xTime,difNormed, color=colorL[colorCnt])
    print "mean of normed differences of element %s: %s" % (colorCnt, np.mean(difNormed))
    colorCnt += 1


    linePerf = mlines.Line2D([], [], color=colorL[0],
                      markersize=15, label='Perfect States')
    lineEst = mlines.Line2D([], [], color=colorL[1],
                      markersize=15, label='Estimated States')

    

    plt.figlegend((lineMCP,linePIP,lineDIP,linePHI,linePerf,lineEst),
                    (r'$\theta_{MCP}$',r'$\theta_{PIP}$',r'$\theta_{DIP}$',r'$\phi_{MCP}$', 'Perfect States', 'Estimated States'),
                    loc='center right',bbox_to_anchor=(0.9,0.8), ncol=3)

    plt.savefig("../thesis/pictures/plots/difOne.png", dpi=300)
    return fig



folderStr = "../simResults/11/160224/"
simValues = datAc.readStateFile(folderStr+"simStates.txt")
simValues_nA = np.delete(simValues, np.s_[-1],1)
loc = folderStr
print "witout ad-ab:"
#uDip_nA = datAc.readStateFile(loc+"estAng_dip0")
cCyl_nA11 = datAc.readStateFile("../simResults/11/160224/"+"estAng_cyl1")
#cDip_nA = datAc.readStateFile(loc+"estAng_dip1")
#cCyl_nA = datAc.readStateFile(loc+"estAng_cyl1")
# nAlist = [uDip_nA, uCyl_nA, cDip_nA, cCyl_nA]
# printMeanVar(nAlist, simValues_nA)
print "\nwith ad-ab:"
#uDip_A = datAc.readStateFile(loc+"estAng_dip_A0")
cCyl_nA12 = datAc.readStateFile("../simResults/12/160224/"+"estAng_cyl1")
#cDip_A = datAc.readStateFile(loc+"estAng_dip_A1")
#cCyl_A = datAc.readStateFile(loc+"estAng_cyl_A1")
#Alist = [uDip_A, uCyl_A, cDip_A, cCyl_nA]
# printMeanVar(Alist, simValues)

#fig, pl = plt.subplots(1,2)
plt.close('all')
pl = plotDif_sub([simValues_nA, cCyl_nA11, cCyl_nA12])
#pl11.savefig("../thesis/pictures/plots/difOne.png", dpi=300)

#pl = plt.subplot(122)
#pl[1] = plotDif([simValues_nA, cCyl_nA12])

#pl22

''' for single finger '''
# l = ['11','12','14']
# for i in l:
#     loc = "../simResults/"+i+"/160224/"
#     print "\n\n",i
#     print "witout ad-ab:"
#     uDip_nA = datAc.readStateFile(loc+"estAng_dip0")
#     uCyl_nA = datAc.readStateFile(loc+"estAng_cyl0")
#     cDip_nA = datAc.readStateFile(loc+"estAng_dip1")
#     cCyl_nA = datAc.readStateFile(loc+"estAng_cyl1")
#     nAlist = [uDip_nA, uCyl_nA, cDip_nA, cCyl_nA]
#     printMeanVar(nAlist, simValues_nA)
#     print "\nwith ad-ab:"
#     uDip_A = datAc.readStateFile(loc+"estAng_dip_A0")
#     uCyl_A = datAc.readStateFile(loc+"estAng_cyl_A0")
#     cDip_A = datAc.readStateFile(loc+"estAng_dip_A1")
#     cCyl_A = datAc.readStateFile(loc+"estAng_cyl_A1")
#     Alist = [uDip_A, uCyl_A, cDip_A, cCyl_A]
#     printMeanVar(Alist, simValues)


# # s11 = datAc.readStateFile(folderStr+"estAng_cyl_A1")
# s11 = datAc.readStateFile(folderStr+"estAng_cyl1")
#
# folderStr = "../simResults/12/160224/"
# # s12 = datAc.readStateFile(folderStr+"estAng_cyl_A1")
# s12 = datAc.readStateFile(folderStr+"estAng_cyl1")
#
# folderStr = "../simResults/14/160224/"
# # s14 = datAc.readStateFile(folderStr+"estAng_cyl_A1")
# s14 = datAc.readStateFile(folderStr+"estAng_cyl1")
''' plotting '''
''' plot the error/dif to perfect normed, s.t. you have a single value (for more readability)! '''
# pl = plotDif([simValues, cCyl_nA, s12, s14])
# pl = plotDif([simValues_A, cCyl_nA])


''' without ad-ab '''
# dCyl0 = simValues_nA-sCyl0
# a=plt.subplot(221)
# a.plot(np.linalg.norm(dCyl0,axis=1))
# a.set_title('norm deviation dCyl1')
# print "overall deviation dCyl1: ",np.linalg.norm(np.linalg.norm(dCyl0,axis=1))

#dCyl2 = simValues_nA-sCyl1
#a=plt.subplot(222)
#a.plot(np.linalg.norm(dCyl2,axis=1))
#a.set_title('norm deviation dCyl2')
#print "overall deviation dCyl2: ",np.linalg.norm(np.linalg.norm(dCyl2,axis=1))
#
#
#dDip1 = simValues_nA-sDip1
#a=plt.subplot(223)
#a.plot(np.linalg.norm(dDip1,axis=1))
#a.set_title('norm deviation dDip1')
#print "overall deviation dDip1: ",np.linalg.norm(np.linalg.norm(dDip1,axis=1))
#
#dDip2 = simValues_nA-sDip2
#a=plt.subplot(224)
#a.plot(np.linalg.norm(dDip1,axis=1))
#a.set_title('norm deviation dDip2')
#print "overall deviation dDip2: ",np.linalg.norm(np.linalg.norm(dDip2,axis=1))
#
#
#plo.plotter2d((dCyl1,dCyl2),("difference to cyl_1","to cyl_2"), shareAxis=False)
#plo.plotter2d((dDip1,dDip2),("difference to dip_1","to dip_2"), shareAxis=False)
#
#''' with ad-ab '''
#
#plt.figure()
#dCyl_A1 = simValues-sCyl_A1
#a=plt.subplot(221)
#a.plot(np.linalg.norm(dCyl_A1,axis=1))
#a.set_title('norm deviation dCyl_A1')
#print "overall deviation dCyl_A1: ",np.linalg.norm(np.linalg.norm(dCyl_A1,axis=1))
#
#dCyl_A2 = simValues-sCyl_A2
#a=plt.subplot(222)
#a.plot(np.linalg.norm(dCyl_A2,axis=1))
#a.set_title('norm deviation dCyl_A2')
#print "overall deviation dCyl_A2: ",np.linalg.norm(np.linalg.norm(dCyl_A2,axis=1))
#
#
#dDip_A1 = simValues-sDip_A1
#a=plt.subplot(223)
#a.plot(np.linalg.norm(dDip_A1,axis=1))
#a.set_title('norm deviation dDip_A1')
#print "overall deviation dDip_A1: ",np.linalg.norm(np.linalg.norm(dDip_A1,axis=1))
#
#dDip_A2 = simValues-sDip_A2
#a=plt.subplot(224)
#a.plot(np.linalg.norm(dDip_A2,axis=1))
#a.set_title('norm deviation dDip_A2')
#print "overall deviation dDip_A2: ",np.linalg.norm(np.linalg.norm(dDip_A2,axis=1))
#
#
#plo.plotter2d((dCyl_A1,dCyl_A2),("difference to cyl_A1","to cyl_A2"), shareAxis=False)
#plo.plotter2d((dDip_A1,dDip_A2),("difference to dip_A1","to dip_A2"), shareAxis=False)

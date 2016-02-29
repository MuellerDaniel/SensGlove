# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:00:35 2015

@author: daniel
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plotter2d(inputlist, titlelist, shareAxis = True, mtitle=None, typ='mag'):
    """plot the data

    Parameters
    ----------
    inputlist : list
        list of the data matrices (shape = ())
    titlelist : list
        list for the corresponding titles
    shareAxis : bool
        share the y-axis or not


    """
#    plt.close("all")
#    print "len(inputlist) ", len(inputlist)
#    print "len(titlelist) ", len(titlelist)
    if len(inputlist) != len(titlelist):
        print "len(inputlist) != len(titlelist)"
        pass
    else:
        plotIt2d(inputlist,titlelist, len(inputlist), shareAxis, mtitle, typ)



def plotIt2d(data, title, sizeData, shareAxis, mtitle, typ):
    colorList = ('r','b','g','y')
    #fingerList = ('index', 'middle', 'ring', 'pinky')
    cnt = 0
    if sizeData == 1:
        for i in data:
            print i.shape
            plt.plot(i[:,0], ls='-',color='r', label='x')
            try:
                plt.plot(i[:,1], ls='--',color='r', label='y')
                plt.plot(i[:,2], ls=':',color='r', label='z')
                plt.plot(i[:,3], ls='-.',color='r', label='PIP')
            except:
                print "doesn't have it..."
            plt.title(title[0])
            plt.legend()
#            cnt = 0
#            for j in i:
#                linCol = colorList[cnt%4]
#                plt.plot(j[:,0], color=linCol, ls='-', label='x')
#                plt.plot(j[:,1], color=linCol, ls='--', label='y')
#                plt.plot(j[:,2], color=linCol, ls=':', label='z')
#                plt.title(title[0])
#                if cnt==0: plt.legend()
#                cnt+=1



    if sizeData >= 2:
        lst = [sizeData]
        f, lst = plt.subplots(1,sizeData, sharey=shareAxis)
        for i in range(sizeData):
            cnt = 0
            for j in data:
                linCol = colorList[cnt%4]
                # line plot representation
                lst[cnt].plot(j[:,0], color=linCol, ls='-', label='x')
                lst[cnt].plot(j[:,1], color=linCol, ls='--', label='y')
                try:
                    lst[cnt].plot(j[:,2], color=linCol, ls=':', label='z')
                    lst[cnt].plot(j[:,3], color=linCol, ls='-.', label='z')
                    
                except:
                    print "only 2d..."
                # scatter plot representation
#                lst[cnt].scatter(np.arange(len(j[:,0])),j[:,0], color=linCol, label='x')
#                lst[cnt].scatter(np.arange(len(j[:,1])),j[:,1], color=linCol, label='y')
#                lst[cnt].scatter(np.arange(len(j[:,2])),j[:,2], color=linCol, label='z')
#                plt.legend()
#                else:
#                    lst[cnt].plot(j[:,0], color=linCol, ls='-')
#                    lst[cnt].plot(j[:,1], color=linCol, ls='--')
#                    lst[cnt].plot(j[:,2], color=linCol, ls=':')

                lst[cnt].set_title(title[cnt])
                if typ == 'mag':
                    lst[cnt].set_xlabel('meas Nr')
                    lst[cnt].set_ylabel(r'B-field[mT]')
                else:
                    lst[cnt].set_xlabel('meas Nr')
                    lst[cnt].set_ylabel('angle [rad]')
                cnt+=1
    if mtitle != None: plt.suptitle(mtitle)


def plotter3d(inputlist, titlelist):
    """plot the data

    Parameters
    ----------
    inputlist : list
        list of the data matrices
    titlelist : list
        list for the corresponding titles


    """
    print "len(inputlist) ", len(inputlist)
    print "len(titlelist) ", len(titlelist)
    if len(inputlist) != len(titlelist):
        print "not enough title given!"
        pass
    else:
        plotIt3d(inputlist,titlelist, len(inputlist))

def plotIt3d(data, title, sizeData):
    fig = plt.figure()
    initPos = 0
    if len(data[0][0]) == 4:
        initPos = 1

#    if sizeData == 1:
#        ax = fig.gca(projection='3d')
#        ax.plot(data[0][:,initPos], data[0][:,initPos+1], data[0][:,initPos+2])
#    elif sizeData >= 2:
    for i in range(sizeData):
        ax = fig.add_subplot(1,sizeData,i, projection='3d', title=title[i])
        ax.plot(data[i][:,initPos], data[i][:,initPos+1], data[i][:,initPos+2])
#            ax = fig.add_subplot(1,2,2, projection='3d', title=title[1])
#            ax.plot(data[1][:,initPos], data[1][:,initPos+1], data[1][:,initPos+2])
#    elif sizeData == 3:
#        ax = fig.add_subplot(1,3,1, projection='3d', title=title[0])
#        ax.plot(data[0][:,initPos], data[0][:,initPos+1], data[0][:,initPos+2])
#        ax = fig.add_subplot(1,3,2, projection='3d', title=title[1])
#        ax.plot(data[1][:,initPos], data[1][:,initPos+1], data[1][:,initPos+2])
#        ax = fig.add_subplot(1,3,3, projection='3d', title=title[2])
#        ax.plot(data[2][:,initPos], data[2][:,initPos+1], data[2][:,initPos+2])


def multiPlotter(data, title, comp=None):
    f = plt.figure(title)

    a = f.add_subplot(2,3,1, projection='3d', title='3d projection')
    a.plot(data[:,0],data[:,1],data[:,2], color='b')
    if comp != None:
        a.plot(comp[:,0],comp[:,1],comp[:,2], color='r')

    b = f.add_subplot(2,3,2, title='x vs y')
    #b.plot(data[:,0],data[:,1], color='b')
    b.plot(data[:,1],data[:,0], color='b')
    if comp != None:
        #b.plot(comp[:,0],comp[:,1], color='r')
        b.plot(comp[:,1],comp[:,0], color='r')

    c = f.add_subplot(2,3,3, title='z vs y')
    #c.plot(data[:,2],data[:,1], color='b')
    c.plot(data[:,2],data[:,0], color='b')
    if comp != None:
        #c.plot(comp[:,2],comp[:,1], color='r')
        c.plot(comp[:,2],comp[:,0], color='r')

    if comp != None:
        bla=float(10./len(data[:,0]))
        bla=0.06329113924050633
#        print "nr ", len(data[:,0])*0.001
        d = f.add_subplot(2,3,4, title='errorPlot x')
        d.scatter(np.arange(0,len(data[:,0]),1),comp[:,0]-data[:,0])


        e = f.add_subplot(2,3,5, title='errorPlot y',sharey=d)
        e.scatter(np.arange(0,len(data[:,0]),1),comp[:,1]-data[:,1])
#        e.set_yticklabels([])

        g = f.add_subplot(2,3,6, title='errorPlot z',sharey=d)
        g.scatter(np.arange(0,len(data[:,0]),1),comp[:,2]-data[:,2])
#        g.set_yticklabels([])


#def visMagData(data,title = None):
#    if len(data.shape) == 3:
#        colorList = ('b','g','r','y')
#        cnt = 0
#        fig = plt.figure()
#        a = fig.add_subplot(2,3,2,projection='3d')
#        a.axis('equal')
#        xy = fig.add_subplot(2,3,4)
#        xz = fig.add_subplot(2,3,5)
#        yz = fig.add_subplot(2,3,6)
#
#        for i in data:
#            a.scatter(i[:,0],i[:,1],i[:,2],c=colorList[cnt%4])
#
#            xy.scatter(i[:,0],i[:,1],c=colorList[cnt%4])
#            xz.scatter(i[:,0],i[:,2],c=colorList[cnt%4])
#            yz.scatter(i[:,1],i[:,2],c=colorList[cnt%4])
#            cnt += 1
#    else:
#        fig = plt.figure()
#        a = fig.add_subplot(111,projection='3d')
#        a.axis('equal')
#        a.scatter(data[:,0],data[:,1],data[:,2],marker='o')

def visMagData(data,title = None):
    colorList = ('b','g','r','y')
    fig = plt.figure()
    a = fig.add_subplot(2,3,2,projection='3d')      # 3d scatter plot
    a.axis('equal')
    a.set_title('3d representation')
    xy = fig.add_subplot(2,3,4)                     # 2d scatter plot
    xy.axis('equal')
    xy.set_title('xy')
    xy.grid()
    xz = fig.add_subplot(2,3,5)                     # 2d scatter plot
    xz.axis('equal')
    xz.set_title('xz')
    xz.grid()
    yz = fig.add_subplot(2,3,6)                     # 2d scatter plot
    yz.axis('equal')
    yz.set_title('yz')
    yz.grid()

    cnt = 0
    for i in data:
        a.scatter(i[:,0],i[:,1],i[:,2],c=colorList[cnt%4])
        xy.scatter(i[:,0],i[:,1],c=colorList[cnt%4])
        xz.scatter(i[:,0],i[:,2],c=colorList[cnt%4])
        yz.scatter(i[:,1],i[:,2],c=colorList[cnt%4])
        cnt += 1


#    if len(data.shape) == 3:
#        colorList = ('b','g','r','y')
#        cnt = 0
#        fig = plt.figure()
#        a = fig.add_subplot(2,3,2,projection='3d')
#        a.axis('equal')
#        xy = fig.add_subplot(2,3,4)
#        xz = fig.add_subplot(2,3,5)
#        yz = fig.add_subplot(2,3,6)
#
#        for i in data:
#            a.scatter(i[:,0],i[:,1],i[:,2],c=colorList[cnt%4])
#
#            xy.scatter(i[:,0],i[:,1],c=colorList[cnt%4])
#            xz.scatter(i[:,0],i[:,2],c=colorList[cnt%4])
#            yz.scatter(i[:,1],i[:,2],c=colorList[cnt%4])
#            cnt += 1
#    else:
#        fig = plt.figure()
#        a = fig.add_subplot(111,projection='3d')
#        a.axis('equal')
#        a.scatter(data[:,0],data[:,1],data[:,2],marker='o')


def timeDatPlot(data,title):
    colorList = ('r','b','g','y')
    #fingerList = ('index', 'middle', 'ring', 'pinky')
    cnt = 0
    sizeData = len(data)
    if sizeData == 1:
        for i in data:
#            print i.shape
            plt.plot(i[:,0],i[:,1], ls='-',color='r', label='x')
            try:
                plt.plot(i[:,0],i[:,2], ls='--',color='r', label='y')
                plt.plot(i[:,0],i[:,3], ls=':',color='r', label='z')
            except:
                print "doesn't have it..."
            plt.title(title[0])
            plt.legend()
#            cnt = 0
#            for j in i:
#                linCol = colorList[cnt%4]
#                plt.plot(j[:,0], color=linCol, ls='-', label='x')
#                plt.plot(j[:,1], color=linCol, ls='--', label='y')
#                plt.plot(j[:,2], color=linCol, ls=':', label='z')
#                plt.title(title[0])
#                if cnt==0: plt.legend()
#                cnt+=1



    if sizeData >= 2:
        lst = [sizeData]
        f, lst = plt.subplots(1,sizeData)
        for i in range(sizeData):
            cnt = 0
            for j in data:
                linCol = colorList[cnt%4]
                # line plot representation
                lst[cnt].plot(j[:,0],j[:,1], color=linCol, ls='-', label='x')
                lst[cnt].plot(j[:,2], color=linCol, ls='--', label='y')
                try:
                    lst[cnt].plot(j[:,3], color=linCol, ls=':', label='z')
                except:
                    print "only 2d..."
                # scatter plot representation
#                lst[cnt].scatter(np.arange(len(j[:,0])),j[:,0], color=linCol, label='x')
#                lst[cnt].scatter(np.arange(len(j[:,1])),j[:,1], color=linCol, label='y')
#                lst[cnt].scatter(np.arange(len(j[:,2])),j[:,2], color=linCol, label='z')
#                plt.legend()
#                else:
#                    lst[cnt].plot(j[:,0], color=linCol, ls='-')
#                    lst[cnt].plot(j[:,1], color=linCol, ls='--')
#                    lst[cnt].plot(j[:,2], color=linCol, ls=':')

                lst[cnt].set_title(title[cnt])
                cnt+=1



def plotAngles(timeStamps,data,head=None):    
    ''' plot multiple datasets with individual timestamps in the same ONE plot 
        for the calculated/estimated finger angles '''
    
    cList = ('r','g','b','y')
    lList = ('MCP', 'PIP', 'DIP', 'ad-ab')
    styleList = ('solid', 'dashed', 'dotted', 'dashdot')
    
#    indPatch = mpatches.Patch(color=cList[0], label='Index')
#    midPatch = mpatches.Patch(color=cList[1], label='Middle')
#    rinPatch = mpatches.Patch(color=cList[2], label='Ring')
#    pinPatch = mpatches.Patch(color=cList[3], label='Pinky')
    
    # check if you have a list of timestamps, indicating that you have two datasets; plot them together
    if isinstance(data,tuple):     
        for i in range(0,len(data)):
            for j in range(0,4):
                plt.plot(timeStamps, data[i][:,j], color=cList[i], label=lList[j], ls=styleList[j])
#                plt.plot(timeStamps, data[i][:,j], color=cList[i], ls=styleList[j])
        plt.ylabel('angle [rad]')
        plt.xlabel('time [s]')
        plt.legend()
        if head: plt.title(head)
        plt.show()
    # you only have one timestamp                
    else:           
        print "data must be tuple!"



def plotLeapVsMag(leapData,magData,head=None,dif=False):
    ''' ploting leap or angle/state values on top and underneath the measured magnetic data '''
    cList = ('r','g','b','y')
    angL = ('MCP', 'PIP', 'DIP', 'ad-ab')
    axisL = ('x', 'y', 'z', 'angles...')
    styleList = ('solid', 'dashed', 'dotted', 'dashdot')    
    
    if dif:
        f, lst = plt.subplots(3, sharex=True)    
    else:
        f, lst = plt.subplots(2, sharex=True)    
    
    # plot leap
    for i in range(1,len(leapData)):
        for j in range(0,(leapData[i].shape[1])):
#            print "i ",
#            print "j ", j
            lst[0].plot(leapData[0], leapData[i][:,j], color=cList[i-1], label=angL[j], ls=styleList[j])            
            lst[0].set_title('states Leap')
            lst[0].set_ylabel('angles [rad]')
            if head: lst[0].set_title(head)
        lst[0].legend()
        
    # plot mag data/angles
    for i in range(1,len(magData)):
        if magData[i].shape[1] == 3:
            for j in range(0,(magData[i].shape[1])):
                lst[1].plot(magData[0], magData[i][:,j], color=cList[i-1], label=axisL[j], ls=styleList[j])
                lst[1].set_title('Magnetic Field')
                lst[1].set_ylabel('B-field [T]')
                lst[1].set_xlabel('time [s]')
            lst[1].legend()            
        elif magData[i].shape[1] == 4:
            for j in range(0,(magData[i].shape[1])):
                lst[1].plot(magData[0], magData[i][:,j], color=cList[i-1], label=angL[j], ls=styleList[j])
                lst[1].set_title('estimated states')
                lst[1].set_ylabel('angles [rad]')
                lst[1].set_xlabel('time [s]')
            lst[1].legend()  
            
    if dif:
        print "bla..."            
    
    
    
    
    
    

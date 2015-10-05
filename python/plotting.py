# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:00:35 2015

@author: daniel
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plotter2d(inputlist, titlelist, shareAxis = True):
    """plot the data

    Parameters
    ----------
    inputlist : list
        list of the data matrices
    titlelist : list
        list for the corresponding titles
    shareAxis : bool
        share the y-axis or not


    """
#    plt.close("all")
    print "len(inputlist) ", len(inputlist)
    print "len(titlelist) ", len(titlelist)
    if len(inputlist) != len(titlelist):
        print "len(inputlist) != len(titlelist)"
        pass
    else:
        plotIt2d(inputlist,titlelist, len(inputlist), shareAxis)



def plotIt2d(data, title, sizeData, shareAxis):
    colorList = ('b','g','r','y')
    cnt = 0
    if sizeData == 1:
        for i in data:
            cnt = 0
            for j in i:
                linCol = colorList[cnt]
                plt.plot(j[:,0], color=linCol, ls='-', label='x')
                plt.plot(j[:,1], color=linCol, ls='--', label='y')
                plt.plot(j[:,2], color=linCol, ls=':', label='z')
                plt.title(title[0])
                if cnt==0: plt.legend()
                cnt+=1

    if sizeData >= 2:
        lst = [sizeData]
        f, lst = plt.subplots(1,sizeData, sharey=shareAxis)
        for i in range(sizeData):
            cnt = 0
            for j in data[i]:
                linCol = colorList[cnt]
                lst[i].plot(j[:,0], color=linCol, ls='-', label='x')
                lst[i].plot(j[:,1], color=linCol, ls='--', label='y')
                lst[i].plot(j[:,2], color=linCol, ls=':', label='z')
                lst[i].set_title(title[i])
                if cnt==0: plt.legend()
                cnt+=1


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
    b.plot(data[:,0],data[:,1], color='b')
    if comp != None:
        b.plot(comp[:,0],comp[:,1], color='r')

    c = f.add_subplot(2,3,3, title='z vs y')
    c.plot(data[:,2],data[:,1], color='b')
    if comp != None:
        c.plot(comp[:,2],comp[:,1], color='r')

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

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
    print "len(inputlist) ", len(inputlist)
    print "len(titlelist) ", len(titlelist)
    if len(inputlist) != len(titlelist):
        print "len(inputlist) != len(titlelist)"
        pass
    else:
        plotIt2d(inputlist,titlelist, len(inputlist), shareAxis)
    
    
def plotIt2d(data, title, sizeData, shareAxis):
    initPos = 0
        
    if len(data[0][0]) == 4:
        initPos = 1
    
    if sizeData == 1:
#        for i in range(len(data[0])):
        if max(data[0][:,0]) == 0:
            plt.plot(data[0][:,initPos], color='b', ls='-', label='x')
            plt.plot(data[0][:,initPos + 1], color='b', ls='--', label='y')
            plt.plot(data[0][:,initPos + 2], color='b', ls=':', label='z')
            plt.title(title[0])
            plt.legend()
        
        if max(data[0][:,0]) == 1:
            data0=[[0.,0.,0.]]
            data1=[[0.,0.,0.]]
            for i in range(len(data[0])):
                tmp = data[0][i]                
                if tmp[0] == 0:
                    data0=np.append(data0, [data[0][i][1:]], axis=0)
                elif tmp[0] == 1:
                    data1=np.append(data1, [data[0][i][1:]], axis=0)
                
            plt.plot(data0[:,0], color='b', ls='-', label='x')
            plt.plot(data0[:,1], color='b', ls='--', label='y')
            plt.plot(data0[:,2], color='b', ls=':', label='z')
            plt.plot(data1[:,0], color='r', ls='-', label='x')
            plt.plot(data1[:,1], color='r', ls='--', label='y')
            plt.plot(data1[:,2], color='r', ls=':', label='z')
            
            plt.title(title[0])
            plt.legend()
                
#        plt.plot(data[0][:,initPos], color='b', ls='-', label='x')
#        plt.plot(data[0][:,initPos + 1], color='b', ls='--', label='y')
#        plt.plot(data[0][:,initPos + 2], color='b', ls=':', label='z')
#        plt.title(title[0])
#        plt.legend()
        
    elif sizeData == 2:
        f,(one, two) = plt.subplots(1,2, sharey=shareAxis)
        one.plot(data[0][:,initPos], color='b', ls='-', label='x')
        one.plot(data[0][:,initPos + 1], color='b', ls='--', label='y')
        one.plot(data[0][:,initPos + 2], color='b', ls=':', label='z')
        one.set_title(title[0])
        one.legend()
        
        two.plot(data[1][:,initPos], color='b', ls='-', label='x')
        two.plot(data[1][:,initPos + 1], color='b', ls='--', label='y')
        two.plot(data[1][:,initPos + 2], color='b', ls=':', label='z')
        two.set_title(title[1])
        
    elif sizeData == 3:
        f, (one, two, three) = plt.subplots(1,3, sharey=shareAxis)
        one.plot(data[0][:,initPos], color='b', ls='-', label='x')
        one.plot(data[0][:,initPos + 1], color='b', ls='--', label='y')
        one.plot(data[0][:,initPos + 2], color='b', ls=':', label='z')
        one.set_title(title[0])
        one.legend()
        
        two.plot(data[1][:,initPos], color='b', ls='-', label='x')
        two.plot(data[1][:,initPos + 1], color='b', ls='--', label='y')
        two.plot(data[1][:,initPos + 2], color='b', ls=':', label='z')
        two.set_title(title[1])
    
        three.plot(data[2][:,initPos], color='b', ls='-', label='x')
        three.plot(data[2][:,initPos + 1], color='b', ls='--', label='y')
        three.plot(data[2][:,initPos + 2], color='b', ls=':', label='z')
        three.set_title(title[2])
        
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
    
    if sizeData == 1:
        ax = fig.gca(projection='3d')
        ax.plot(data[0][:,initPos], data[0][:,initPos+1], data[0][:,initPos+2])
    elif sizeData == 2:
        ax = fig.add_subplot(1,2,1, projection='3d', title=title[0])
        ax.plot(data[0][:,initPos], data[0][:,initPos+1], data[0][:,initPos+2])
        ax = fig.add_subplot(1,2,2, projection='3d', title=title[1])
        ax.plot(data[1][:,initPos], data[1][:,initPos+1], data[1][:,initPos+2])
    elif sizeData == 3:
        ax = fig.add_subplot(1,3,1, projection='3d', title=title[0])
        ax.plot(data[0][:,initPos], data[0][:,initPos+1], data[0][:,initPos+2])
        ax = fig.add_subplot(1,3,2, projection='3d', title=title[1])
        ax.plot(data[1][:,initPos], data[1][:,initPos+1], data[1][:,initPos+2])
        ax = fig.add_subplot(1,3,3, projection='3d', title=title[2])
        ax.plot(data[2][:,initPos], data[2][:,initPos+1], data[2][:,initPos+2])
        
    
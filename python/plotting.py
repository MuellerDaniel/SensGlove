# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:00:35 2015

@author: daniel
"""
import matplotlib.pyplot as plt

def plotter(inputlist, titlelist, shareAxis = True):
    print "len(inputlist) ", len(inputlist)
    print "len(titlelist) ", len(titlelist)
    if len(inputlist) != len(titlelist):
        print "not enough title given!"
        pass
    else:
        plotIt(inputlist,titlelist, len(inputlist), shareAxis)
    
    
def plotIt(data, title, sizeData, shareAxis):
    initPos = 0
    
    if len(data[0][0]) == 4:
        initPos = 1
    
    if sizeData == 1:
        plt.plot(data[0][:,initPos], color='r', label='x')
        plt.plot(data[0][:,initPos + 1], color='g', label='y')
        plt.plot(data[0][:,initPos + 2], color='b', label='z')
        plt.title(title[0])
        plt.legend()
        
    elif sizeData == 2:
        f,(one, two) = plt.subplots(1,2, sharey=shareAxis)
        one.plot(data[0][:,initPos], color='r', label='x')
        one.plot(data[0][:,initPos + 1], color='g', label='y')
        one.plot(data[0][:,initPos + 2], color='b', label='z')
        one.set_title(title[0])
        one.legend()
        
        two.plot(data[1][:,initPos], color='r', label='x')
        two.plot(data[1][:,initPos + 1], color='g', label='y')
        two.plot(data[1][:,initPos + 2], color='b', label='z')
        two.set_title(title[1])
        
    elif sizeData == 3:
        f, (one, two, three) = plt.subplots(1,3, sharey=shareAxis)
        one.plot(data[0][:,initPos], color='r', label='x')
        one.plot(data[0][:,initPos + 1], color='g', label='y')
        one.plot(data[0][:,initPos + 2], color='b', label='z')
        one.set_title(title[0])
        one.legend()
        
        two.plot(data[1][:,initPos], color='r', label='x')
        two.plot(data[1][:,initPos + 1], color='g', label='y')
        two.plot(data[1][:,initPos + 2], color='b', label='z')
        two.set_title(title[1])
    
        three.plot(data[2][:,initPos], color='r', label='x')
        three.plot(data[2][:,initPos + 1], color='g', label='y')
        three.plot(data[2][:,initPos + 2], color='b', label='z')
        three.set_title(title[2])
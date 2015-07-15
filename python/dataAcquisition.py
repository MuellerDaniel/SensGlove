# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 08:52:55 2015

@author: daniel
"""
import numpy as np
import serial
import string
import time


def serialAcquisition(serPort, fileName, offset, measNr, timeStamp = True):
    """function for acquiring data from the serial port
    
    Parameters
    ----------
    serPort : str
        Name of serial Port
    fileName : str
        Name of the .txt file, the data gets saved to
        Remember: the file contains a timestamp!
    offset : int
        first samples, that get neglected
    measNr : int
        total number of measurements
    timeStamp : bool
        whether to add timeStamp to file or not
        
    Returns
    -------
    magMat : np.array(shape[measNr,3])
        the recorded magnetic field in the x-, y-, z-direction
        
    """
    ser = serial.Serial(port=serPort, baudrate=9600, timeout=1)
    fl = open(fileName, 'w')
    start_time = time.time()
    if timeStamp:
        fl.write("# measurement started at start_time " + str(start_time) + "\n")
    magMat = np.empty(shape=[0,3]) 
    b = np.array([0.,0.,0.])
    cnt = 0    
    #measNr = 0
    #offset = 0
    try:
        while cnt < measNr + offset:
            message = ser.readline()
            print cnt
            #print message
            if(cnt < offset):
                #cnt+=1
                print "too small..."
            else:            
              #  print "recording... taking " + str(measNr) + " measurements"
                mlist = string.split(message, "\t")
                #print message
                if len(mlist) > 2:       
                    try:
                        b[0] = 1*float(mlist[0])
                        b[1] = 1*float(mlist[1])
                        b[2] = 1*float(mlist[2])
                    except ValueError:
                        print 'float conversion not possible ', mlist
                else: 
                    pass

                magMat = np.append(magMat, [b])  
                #print b   
                if timeStamp:                    
                    fl.write(format((time.time()-start_time), '.3f') + "\t" + 
                                str(b[0]) + "\t" + str(b[1]) + "\t" + str(b[2]) + "\n")            
                else:
                    fl.write(str(b[0]) + "\t" + str(b[1]) + "\t" + str(b[2]) + "\n")
            cnt+=1


    # to catch a ctrl-c
    except KeyboardInterrupt:
        print "here!"
        #pass
      
    print str(cnt-offset) + " measurements taken"
    magMat = np.reshape(magMat, (magMat.size/3, 3))
    fl.close()
    ser.close()
    
    return magMat
    

def textAcquistion(fileName, timeStamp = False):
    """function for acquiring data from a text file
    
    Parameters
    ----------
    fileName : str
        name of .txt file of your data
    timeStamp : bool
        if you have a timeStamp in your data, assign it also in your mat
        
    Returns
    -------
    dataMat : np.array(shape[NrOfMeas, 4])
        timestamp of measurement(if written), magnetic field in x-, y-,z-direction
        
    """
    try:
        f = open(fileName, 'r')
    except IOError:
        print "File not found!"    
  
    line = f.readline() 
    dataMat = np.empty(shape=[0,3])
    
    if timeStamp:
        dataMat = np.empty(shape=[0,4])     
    
    while(line != ""):    
        if (line.startswith("#")):
            print line
        else:  
            dataString = string.split(line, "\t")
            #print dataString
            if len(dataString) == 4:
                if timeStamp:
                    dataMat = np.append(dataMat, 
                                        [[float(dataString[0]), 
                                          float(dataString[1]), 
                                          float(dataString[2]), 
                                          float(dataString[3])]],axis=0)        
                else:
                     dataMat = np.append(dataMat, 
                                    [[float(dataString[1]), 
                                      float(dataString[2]), 
                                      float(dataString[3])]],axis=0)
            elif len(dataString) == 3:
                dataMat = np.append(dataMat, 
                                    [[float(dataString[0]), 
                                      float(dataString[1]), 
                                      float(dataString[2])]],axis=0)
        line = f.readline() 
    
    if timeStamp:
        print "with timestamp!"
        
    return dataMat
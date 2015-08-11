# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 08:52:55 2015

@author: daniel
"""
import numpy as np
import serial
import string
import time
import subprocess
import struct


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
                
                #print "mean[uT]: ", np.mean(b)
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
    



def structDataBLE(inp):
    dataHex = []
    #print "STRUCTINPUT inp ", inp
    inp = inp.split()
    for x in inp:
        if len(x) == 2:
            dataHex.append(x) 
    if ((len(dataHex)<=0) or (len(dataHex)%4)) :
        print 'not enough numbers!'
        print dataHex
        return np.array([0.,0.,0.,0.])
        
    dataHex = [chr(int(x, base=16)) for x in dataHex] 
    d = []
    tmp = []
    value = np.array([0., 0., 0.,0.])
    i=0
    for i in range(len(dataHex)/4):
        d.append("".join(dataHex[(i*4):(i*4)+4]))
        tmp.append(struct.unpack("f", d[i]))    
        value[i] = "{0:.2f}".format(float(tmp[i][0]))             
        i+=1
        
    return value


def structDataSer(data):
    b = np.array([0.,0.,0.])
    data = data.split('\t')
    if len(data) > 2:  
            try: 
                b[0] = 1*float(data[0])
                b[1] = 1*float(data[1])
                b[2] = 1*float(data[2])
                return b
                #print "value: ", b
            except ValueError:
                print 'float conversion not possible ', data
                return np.array([0.,0.,0.])
    else: 
        return np.array([0.,0.,0.])


def pipeAcquisition(arg, fileName=None, measNr=None, offset=0):
    """function for acquiring data via pipe
    
    Parameters
    ----------
    args : str
        terminal command, to start the data acquisition
        
        "stty -F /dev/ttyUSB0 time 50; cat /dev/ttyUSB0" for serial
        
        "gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen" for ble
    fileName : str
        name of the file, the data should be stored in (optional)
        
    measNr : int
        Number of measurements, that should be taken
        
    Returns
    -------
    dataMat : np.array(shape[NrOfMeas, 3])
        magnetic field in x-, y-,z-direction
        
    """
    
    # "gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen"
    mat = [[0.,0.,0.,0.]]
    if "/dev/tty" in arg:
        proc = subprocess.Popen(arg, stdout=subprocess.PIPE, 
                                close_fds=True, shell=True)
    if "gatttool" in arg:
        proc = subprocess.Popen(arg.split(), 
                                stdout=subprocess.PIPE, close_fds=True)
    if fileName != None:
        fl = open(fileName, 'w')   
    i=0                 
    data = np.array([0.,0.,0.,0.])
    if measNr == None: 
        measNr = np.inf
    try:
        while i<measNr+offset:     
            
            output = proc.stdout.readline()
            # read the input file only till the end!            
            if output != '':                
                if "gatttool" in arg:                
                    data = structDataBLE(output)
                    #print "raw output: ", output
                if "/dev/tty" in arg:
                    data = structDataSer(output)
    #                print data
                if fileName != None:
                    fl.write(str(data[0]) + "\t" + 
                            str(data[1]) + "\t" + 
                            str(data[2]) + "\t" + 
                            str(data[3]) + "\n")
                    print "Data written: ", data
                else:
                    print "Data: ", data
                mat = np.append(mat, [data], axis=0)                
    #                print "writing...", data
#                if i%10 == 0: print "measurement nr ", i
                
            else :                
                proc.stdout.close()
                proc.kill()
                break
            i += 1
            
    except KeyboardInterrupt:       
        print "here!"            
#        proc.stdout.close()
#        proc.kill()
#        raise
        
#    mat = np.reshape(mat, (mat.size/4, 4))
    proc.stdout.close()
    proc.kill()
    if fileName != None:
        fl.close()
    mat = mat[offset+2:]
    return mat
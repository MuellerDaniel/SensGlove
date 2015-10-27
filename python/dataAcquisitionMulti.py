# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 08:52:55 2015

@author: daniel
"""
import numpy as np
import serial,string,time,subprocess,struct,select

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
#    dataString = string.split(line, "\t")
#    form=0
#    if len(dataString) == 4:
#        form=4
#        dataMat = [[0.,0.,0.,0.]]
#        dataMat[0] = [float(dataString[0]), 
#                     float(dataString[1]), 
#                     float(dataString[2]), 
#                     float(dataString[3])]
#                     
#    elif len(dataString) == 3:
#        form=3
#        dataMat = [[0.,0.,0.]]
#        dataMat[0] = [float(dataString[0]), 
#                       float(dataString[1]), 
#                       float(dataString[2])]
#    else: 
#        print "wrong data format!!!!"
    dataMat = [[0.,0.,0.,0.]]
    form = 4
    while(line != ""):    
        if (line.startswith("#")):
            print line
        else:  
            dataString = string.split(line, "\t")
            
        if form == 4:
            dataMat = np.append(dataMat, 
                            [[float(dataString[0]),
                              float(dataString[1]), 
                              float(dataString[2]), 
                              float(dataString[3])]],axis=0)                                         
        elif form == 3:
             dataMat = np.append(dataMat, 
                            [[float(dataString[1]), 
                              float(dataString[2]), 
                              float(dataString[3])]],axis=0)

        line = f.readline()    
#    dataMat = dataMat[1:]
    dataMat = sortData(dataMat)
    return dataMat
    



def structDataBLE(inp):
    dataHex = []
    #print "STRUCTINPUT inp ", inp
    inp = inp.split()
    for x in inp:
        if len(x) == 2:
            dataHex.append(x) 
    if ((len(dataHex)<=0) or (len(dataHex)%4)) :
#        print 'not enough numbers!'
#        print dataHex
        return np.array([0.,0.,0.,0.])
        
    dataHex = [chr(int(x, base=16)) for x in dataHex] 
    d = []
    tmp = []
    value = np.array([0., 0., 0., 0.])
    i=0
    for i in range(len(dataHex)/4):
        d.append("".join(dataHex[(i*4):(i*4)+4]))
        tmp.append(struct.unpack("f", d[i]))    
        value[i] = "{0:.2f}".format(float(tmp[i][0]))             
        #i+=1
    
#    print "pipe: ", value
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



def invertX(data):
    return data*[1.,-1.,1.,1.]
    
def eraseZeros(data):
    cnt=0
    for i in data:
        if i[1:].any() == False:
            data = np.delete(data, cnt, 0)
            cnt-=1
        cnt+=1
    return data

def sortData(data):     
    # erasing the first [0.,0.,0.] in the dataarray
    print "sort beginning: ", data.shape
    cnt=0
    for i in data:
        if i[1:].any() == False:
            data = np.delete(data, cnt, 0)
            cnt-=1
        cnt+=1
    print "sort after deleting...", data.shape    
    # removing surplus taken measurements
    nrSens = int(max(data[:,0])+1)
    if len(data)%nrSens:
        print "too much  measurements taken...", len(data)%nrSens
        datadel = np.delete(data, np.s_[-1*(len(data)%nrSens):], axis=0)
        print datadel.shape
#        np.reshape(datadel,(nrSens,len(datadel),3))
        data = None
        data = datadel
    # matrix for results
    s=np.zeros((nrSens, (len(data)/nrSens), 3))
    #cnt = np.zeros(shape=(nrSens,1), dtype=np.int)
    cnt = np.zeros((nrSens,1))
    for j in data:
        s[int(j[0])][int(cnt[int(j[0])])] = j[1:]              
        cnt[int(j[0])] += 1  
#    else:
#        print "right amount of measurements..."
#        np.reshape(data,(nrSens,len(data),3))    
    return data
    
def splitData(data):
    one = np.array([0.,0.,0.])    
    two = np.array([0.,0.,0.])    
    three = np.array([0.,0.,0.])     
    four = np.array([0.,0.,0.])    
    print "data: ",data.shape
    
    for i in data:
        if i[0] == 0:
            one = np.append(one,i[1:])
            print "one!"
        elif i[0] == 1:
            two = np.append(two,i[1:])
        elif i[0] == 2:
            three = np.append(three,i[1:])
        elif i[0] == 3:
            four = np.append(four,i[1:])
            
    one = np.reshape(one,((len(one)/3,3)))            
    two = np.reshape(two,((len(two)/3,3)))
    three = np.reshape(three,((len(three)/3,3)))
    four = np.reshape(four,((len(four)/3,3)))
    print one.shape
    print two.shape
    print three.shape
    print four.shape
    return (one[1:],two[1:],three[1:],four[1:])


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
#                    data = invertX(data)
#                    print "raw output: ", output
                    print "data output: ", data
                if "/dev/tty" in arg:
                    data = structDataSer(output)
#                    data = invertX(data)
    #                print data
                if (i>offset) and not bool((i-offset)%100) :                    
                    print i-offset, "measurements taken"
                    
#                else: print "below offset ", i
#                print "data: ",data
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
        proc.stdout.close()
        proc.kill()
#        raise
        
#    mat = np.reshape(mat, (mat.size/4, 4))
    proc.stdout.close()
    proc.kill()
    
    mat = mat[offset+2:]
    if fileName != None:
        for i in mat:
            fl.write(str(i[0]) + "\t" +
                    str(i[1]) + "\t" + 
                    str(i[2]) + "\t" +
                    str(i[3]) + "\n")
        fl.close()     
    mat = sortData(mat)
#    print "blabla"
    return mat
    
    
def RTdata(data,proc):       
    tmpData = np.array([0.,0.,0.,0.])     
    while proc.stdout in select.select([proc.stdout], [], [], 0)[0]:
      line = proc.stdout.readline() 
#      print "line in RT: ", line
      if line != ' ':
        tmpData = structDataBLE(line)        
        if tmpData[0] == 0: data[0][1:] = tmpData[1:]
        if tmpData[0] == 1: data[1][1:] = tmpData[1:]
        if tmpData[0] == 2: data[2][1:] = tmpData[1:]
        if tmpData[0] == 3: data[3][1:] = tmpData[1:]
        
    return data    
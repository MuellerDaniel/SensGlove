import dataAcquisitionMulti as datAc
import numpy as np
import subprocess, threading, Queue, sys, ctypes, select

''' version with threading and a queue
    works, but it is not so easy to stop the thread and to stop the ble communication...
'''
#ON_POSIX = 'posix' in sys.builtin_module_names
#
#def enqueue_output(out, queue): 
#    for line in iter(out.readline, b''):
#        if line != None:
#            queue.put(line)
#    out.close()
#
#proc = subprocess.Popen(" gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen", 
#                            stdout=subprocess.PIPE, close_fds=True, shell=True)
#
##runIt = True
#
#qu = Queue.Queue()
#th = threading.Thread(target=enqueue_output, args=(proc.stdout, qu))
#th.daemon = True
#th.start()
#
#data = np.array([0.,0.,0.,0.])    
#cnt,received = 0,0    
#while received < 10:
#    cnt += 1
#    try: line = qu.get_nowait()
#    except Queue.Empty:
#        print data            
#    else:                                 
##        output = proc.stdout.readline()
#        data = datAc.structDataBLE(line)
#        print data
#        print "iterations ", cnt
#        received += 1
#
#qu.task_done()
#print "alive ? ", th.is_alive()
#proc.stdout.close()
#proc.kill()
    
''' version with select call
'''


#def RTdata(data,proc):                    
##    received, cnt = 0,0       
#    tmpData = np.array([0.,0.,0.,0.])                 
##    while received < 10:    
#    while proc.stdout in select.select([proc.stdout], [], [], 0)[0]:
#      line = proc.stdout.readline()      
#      if line:
#        tmpData = datAc.structDataBLE(line)
#        if tmpData[0] == 0: data[0][1:] = tmpData[1:]
#        if tmpData[0] == 1: data[1][1:] = tmpData[1:]
#        if tmpData[0] == 2: data[2][1:] = tmpData[1:]
#        if tmpData[0] == 3: data[3][1:] = tmpData[1:]
#        print "NEW!\n", data
##        received += 1      
##    else:
##      print "nothing new...\n", data
#    return data
#
#subuproc = subprocess.Popen(" gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen", 
#                            stdout=subprocess.PIPE, close_fds=True, shell=True)
#
#data = np.array([[0,0.,0.,0.],
#                 [1,0.,0.,0.],
#                 [2,0.,0.,0.],
#                 [3,0.,0.,0.]])
#cnt = 0
#while True:
#    data = RTdata(data,subuproc)
#    print data
##    cnt += 1
# 
#print "here" 
#subuproc.stdout.close()
#subuproc.kill()

''' how to use the function
'''

subproc = subprocess.Popen("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen".split(), 
                            stdout=subprocess.PIPE, close_fds=True)

data = np.array([[0,0.,0.,0.],
                 [1,0.,0.,0.],
                 [2,0.,0.,0.],
                 [3,0.,0.,0.]])
                 
collect = np.array([[0,0.,0.,0.],
                 [1,0.,0.,0.],
                 [2,0.,0.,0.],
                 [3,0.,0.,0.]])                
                 
cnt = 0                 
while True:
    cnt += 1
    data = datAc.RTdata(data,subproc) 
    
    if data[0][1:].any() != 0:
        print "here"
        print data
#        break
    
    

print cnt
subproc.terminate() 

    
#    collect = np.append(collect,data,axis=0)
##    startPos = time.time()             
#    tmp = modE.estimatePos(np.concatenate((estPos[0][i],estPos[1][i],estPos[2][i],estPos[3][i])),
#                         np.reshape([s1,s2,s3,s4],((12,))),     # for calling the cython function
#                         np.concatenate((b[0][i+1],b[1][i+1],b[2][i+1],b[3][i+1])),
#                         i,bndsPos)
#                         
#    resPos = np.reshape(tmp.x,(4,1,3))
##    lapPos[i] = ((time.time()-startPos),tmp.nit)
#    estPos[0][i+1] = resPos[0]
#    estPos[1][i+1] = resPos[1]
#    estPos[2][i+1] = resPos[2]
#    estPos[3][i+1] = resPos[3]                         

  
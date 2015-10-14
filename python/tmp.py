import os, time, sys, signal
pipe_name = 'pipe_test0'

def child( ):
    print "child!"
    pipeout = os.open(pipe_name, os.O_WRONLY)
    counter = 0
    while True:
        time.sleep(1)
        os.write(pipeout, 'Number %03d\n' % counter)
        counter = (counter+1) % 5

def parent( ):
    print "parent!"
    pipein = open(pipe_name, 'r')
    i=0
    while i<10:
        line = pipein.readline()[:-1]
        print 'Parent %d got line "%s" at %s sec' % (os.getpid(), line, time.time( ))
        i = i+1

i = 0
while i < 10:
    if not os.path.exists(pipe_name):
        os.mkfifo(pipe_name)  
        
    pid = os.fork()    
    if pid != 0:
        parent()
    else:       
        child()
        
    i = i+1
    print "i: ",i

os.kill(os.getpid(),signal.SIGKILL)
print "finished"        
    
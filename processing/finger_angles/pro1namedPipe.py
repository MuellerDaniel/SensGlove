import os,time
import socket, errno

mPath = 'myPath5'

if not os.path.exists(mPath):
    os.mkfifo(mPath)
#else:
##    os.unlink(mPath)
#    os.mkfifo(mPath)
print "pid: ", os.getpid()

counter = 0
while True:
    print "in while..."
    pipeout = os.open(mPath, os.O_WRONLY)
    time.sleep(0.1)
    try:                   #thumb      #index       #middle      #ring        #pinky
        os.write(pipeout, "0.0 0.0 0.0 90.0 0.0 0.0 0.0 90.0 0.0 0.0 0.0 90.0 0.0 90.0 0.0\n")
        counter = counter+1
        print "process1 running..."
    except OSError,e:
        print "error! listener disconnected"
        os.unlink(mPath)
        break
    except KeyboardInterrupt,e:
        print "keyboard interrupt"
        os.unlink(mPath)

import subprocess, time

def doEstimation(counter):
    outstr = "0.0000 0.0000 0.0000"
    for i in range(12):
        outstr = outstr+" {0:.4f}".format(counter)
    time.sleep(0.3)
    return outstr

fileName = "tst.txt"
f = open(fileName, 'w')

#cmd = "python txtRead.py " + fileName
# cmd = "./../SensGlove/visualization/riggedAni/HandGame.blend " + fileName
cmd = "./HandGame.blend" + fileName
print cmd.split()
subPro = subprocess.Popen(cmd.split())#, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

cnt = 0.0000
while cnt < 100:
    toSend = doEstimation(cnt)
    f = open(fileName, 'a')
    f.write(toSend+'\n')
    cnt += 0.011
    print "written ", toSend
    f.close()

#f.close()

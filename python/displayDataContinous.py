from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial
import time
import pyqtgraph.console
 
app = QtGui.QApplication([])
 
p = pg.plot()
p.setWindowTitle('live plot from serial')
curve1 = p.plot(pen=(255,0,0))
curve2 = p.plot(pen=(0,255,0))
curve3 = p.plot(pen=(0,0,255))

datax = [0]
datay = [0]
dataz = [0]
dataArr = np.empty(shape=[0,3])
dataArr = np.append(dataArr, np.array([0,100,200]))
#raw=serial.Serial("/dev/ttyACM0",9600)
#raw.open()
cntarr = np.array([0,100,200])
cnt = 0
#cnt[0] = 0
#cnt[1] = 100
#cnt[2] = 200


def update():
    global curve1, curve2, curve3, datax, datay, dataz, cntarr, cnt, dataArr
#    cntarr += np.array([1, -1, 0])
#    cnt += 1
#    dataArr = np.append(dataArr, cntarr)
#    dataArr = np.reshape(dataArr, (dataArr.size/3, 3))
    
    datax.append(cntarr[0])
    datay.append(cntarr[1])
    dataz.append(cntarr[2])
    #data.append(cnt)
    #line = raw.readline()
    #data.append(int(line))
#    xdata = np.array(datax)
#    ydata = np.array(datay)
#    zdata = np.array(dataz)    
    #print "xdata ", xdata    
    #print "ArrXdata ", dataArr[:,0]    
    
#    curve1.setData(xdata)
#    curve2.setData(ydata)
#    curve3.setData(zdata)
    curve1.setData(dataArr[:,0])
    curve2.setData(dataArr[:,1])
    curve3.setData(dataArr[:,2])
    
    app.processEvents()
 
#timer = QtCore.QTimer()
#timer.timeout.connect(update)
#timer.start(100)
try:
    while True:
        cntarr += np.array([1, -1, 0])
        cnt += 1
        dataArr = np.append(dataArr, cntarr)
        dataArr = np.reshape(dataArr, (dataArr.size/3, 3))        
  
        update()
        #time.sleep(.5)
        
except KeyboardInterrupt:
    print "out!"
    print "dataArr", dataArr.size
    pass


#app.closeAllWindows()
    
#if __name__ == '__main__':
#    import sys
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        QtGui.QApplication.instance().exec_()

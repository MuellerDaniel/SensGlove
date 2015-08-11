from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import subprocess
import dataAcquisitionMulti as datAcM
 
app = QtGui.QApplication([])
 
p = pg.plot()
p.setWindowTitle('live plot from ble')
p.addLegend()
curvesRed = []
curvesRed.append(p.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.SolidLine), name='x'))
curvesRed.append(p.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.DashLine), name='y'))
curvesRed.append(p.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.DotLine), name='z'))
curvesBlue = []
curvesBlue.append(p.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.SolidLine), name='x'))
curvesBlue.append(p.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.DashLine), name='y'))
curvesBlue.append(p.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.DotLine), name='z'))
#curve1 = p.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.SolidLine), name='x')
#curve2 = p.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.DashLine), name='y')
#curve3 = p.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.DotLine), name='z')

datax = [0]
datay = [0]
dataz = [0]
dataArrRed = [[0.,0.,0.]]
dataArrBlue = [[0.,0.,0.]]

#dataArr = np.empty(300)
displayArr = np.empty(shape=[0,3])
#dataArr = np.append(dataArr, np.array([0,100,200]))

cnt = 0
overcnt = 0
overcntRed = 0
overcntBlue = 0
maxSize = 100

def update():
    global cnt, dataArrRed, dataArrBlue, maxSize, overcnt, overcntRed, overcntBlue, curves
    
    if b[0] == 0:
        dataArrRed = np.append(dataArrRed, [b[1:]], axis=0)
    elif b[0] == 1:
        dataArrBlue = np.append(dataArrBlue, [b[1:]], axis=0)
#    dataArr = np.reshape(dataArr, (dataArr.size/3,3))
    
    cnt += 1
    
    if dataArrRed.shape[0]>maxSize:
#        overcnt+=1
#        curve1.setData(dataArr[overcnt:,0])
#        curve2.setData(dataArr[overcnt:,1])
#        curve3.setData(dataArr[overcnt:,2])
        if b[0] == 0:
            overcntRed += 1
            curvesRed[0].setData(dataArrRed[overcnt:,0])
            curvesRed[1].setData(dataArrRed[overcnt:,1])
            curvesRed[2].setData(dataArrRed[overcnt:,2])
        elif b[0] == 1:
            overcntBlue += 1
            curvesBlue[0].setData(dataArrBlue[overcnt:,0])
            curvesBlue[1].setData(dataArrBlue[overcnt:,1])
            curvesBlue[2].setData(dataArrBlue[overcnt:,2])    

    else:
#        curve1.setData(dataArr[:,0])
#        curve2.setData(dataArr[:,1])
#        curve3.setData(dataArr[:,2])
        if b[0] == 0:
            curvesRed[0].setData(dataArrRed[:,0])
            curvesRed[1].setData(dataArrRed[:,1])
            curvesRed[2].setData(dataArrRed[:,2])
        elif b[0] == 1:
            curvesBlue[0].setData(dataArrBlue[:,0])
            curvesBlue[1].setData(dataArrBlue[:,1])
            curvesBlue[2].setData(dataArrBlue[:,2])
        
    
#    curve3.setPos(-cnt, 0)
    
    app.processEvents()
    


# BLE acquisition
proc = subprocess.Popen("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen".split(), 
                        stdout=subprocess.PIPE, close_fds=True)
# serial acquisition
#proc = subprocess.Popen("stty -F /dev/ttyUSB0 time 50; cat /dev/ttyUSB0", 
#                        stdout=subprocess.PIPE, close_fds=True, shell=True) 
b = np.array([0.,0.,0.,0.]) 
i = 0
try:
    while True:          
        output = proc.stdout.readline()
        b = datAcM.structDataBLE(output)   
#        b = datAc.structDataSer(output)
        update()


# to catch a ctrl-c
except KeyboardInterrupt:    
    proc.stdout.close()
    proc.kill()
    print "Killed ble listener!"
    pass


#app.closeAllWindows()
    
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        print "here!"
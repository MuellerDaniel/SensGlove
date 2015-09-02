from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
#from pyqtgraph.ptime import time
import subprocess
import dataAcquisitionMulti as datAcM
import modelEq as modE
 
app = QtGui.QApplication([])
 
magPlot = pg.plot()
magPlot.setWindowTitle('live plot from ble')
magPlot.addLegend()
curvesRed = []
curvesRed.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.SolidLine), name='x'))
curvesRed.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,255,0), style=QtCore.Qt.DashLine), name='y'))
curvesRed.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.DotLine), name='z'))
curvesBlue = []
curvesBlue.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.SolidLine), name='x'))
curvesBlue.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.DashLine), name='y'))
curvesBlue.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.DotLine), name='z'))
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
maxSize = 500       # amount of data, displayed on the screen

def updateMagnet():
    global cnt, dataArrRed, dataArrBlue, maxSize, overcntRed, overcntBlue
    
    if b[0] == 0:
        dataArrRed = np.append(dataArrRed, [b[1:]], axis=0)
    elif b[0] == 1:
        dataArrBlue = np.append(dataArrBlue, [b[1:]], axis=0)
#    dataArr = np.reshape(dataArr, (dataArr.size/3,3))
    
    cnt += 1
    factorX = 1
    if dataArrRed.shape[0]>maxSize:
#        overcnt+=1
#        curve1.setData(dataArr[overcnt:,0])
#        curve2.setData(dataArr[overcnt:,1])
#        curve3.setData(dataArr[overcnt:,2])
        if b[0] == 0:
            overcntRed += 1
            curvesRed[0].setData(factorX*dataArrRed[overcntRed:,0])
            curvesRed[1].setData(dataArrRed[overcntRed:,1])
            curvesRed[2].setData(dataArrRed[overcntRed:,2])
        elif b[0] == 1:
            overcntBlue += 1
            curvesBlue[0].setData(factorX*dataArrBlue[overcntBlue:,0])
            curvesBlue[1].setData(dataArrBlue[overcntBlue:,1])
            curvesBlue[2].setData(dataArrBlue[overcntBlue:,2])    

    else:
#        curve1.setData(dataArr[:,0])
#        curve2.setData(dataArr[:,1])
#        curve3.setData(dataArr[:,2])
        if b[0] == 0:
            curvesRed[0].setData(factorX*dataArrRed[:,0])
            curvesRed[1].setData(dataArrRed[:,1])
            curvesRed[2].setData(dataArrRed[:,2])
        elif b[0] == 1:
            curvesBlue[0].setData(factorX*dataArrBlue[:,0])
            curvesBlue[1].setData(dataArrBlue[:,1])
            curvesBlue[2].setData(dataArrBlue[:,2])
#    curve3.setPos(-cnt, 0)
    app.processEvents()     # needed?
    


posPlot = pg.plot()
posPlot.setWindowTitle("estimated Position")
posPlot.addLegend()
curvePos = []
curvePos.append(posPlot.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.SolidLine), name='x'))
curvePos.append(posPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,255,0), style=QtCore.Qt.SolidLine), name='y'))
curvePos.append(posPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.SolidLine), name='z'))
overCntPos = 0
dataArrPos = [[0.,0.,0.]]

def updatePos():
    global dataArrPos, overCntPos
#    p=[1.3,4.5,6.4]
    dataArrPos = np.append(dataArrPos, [p], axis=0)
    
    if dataArrPos.shape[0]>maxSize:
        overCntPos+=1
        curvePos[0].setData(dataArrPos[overCntPos:,0])
        curvePos[1].setData(dataArrPos[overCntPos:,1])
        curvePos[2].setData(dataArrPos[overCntPos:,2])
        
    else:
        curvePos[0].setData(dataArrPos[:,0])
        curvePos[1].setData(dataArrPos[:,1])
        curvePos[2].setData(dataArrPos[:,2])
        
# BLE acquisition
proc = subprocess.Popen("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen".split(), 
                        stdout=subprocess.PIPE, close_fds=True)
# serial acquisition
#proc = subprocess.Popen("stty -F /dev/ttyUSB0 time 50; cat /dev/ttyUSB0", 
#                        stdout=subprocess.PIPE, close_fds=True, shell=True) 
b = np.array([0.,0.,0.,0.]) 
s0 = [0.00920 , 0.06755, 0.]             # sensor position
angle = [0., 0.02272, 0.01087]          # angle position of the finger
r = 0.08829                     # length of the finger
p = [[angle[0]+s0[0], angle[1]+s0[1]+r, s0[2]+angle[2]]]           # initial position

bnds=((angle[0]+s0[0]-0.003,angle[0]+s0[0]+0.003),  # bounds for the actual finger
      (angle[1]+s0[1],angle[1]+s0[1]+r),
      (angle[2]+s0[2],angle[2]+s0[2]+r))

scale = [ 0., 0.41656681, 0.28542467]
offset = [ 0., 240.46739245, 5.38012971]
i = 0
try:
    while True:          
        output = proc.stdout.readline()
        b = datAcM.structDataBLE(output)
        updateMagnet()
#        if (i==1) & (b.any()>0.0):
#            print "one"
#            p = modE.estimatePos(p0,s0,b[1:],bnds)
#            updatePos()            
        if i>1:                 # p should reflect the old position...???
            print "bigger one"
#            p = modE.estimatePos(p,s0,np.add(np.multiply(b[1:],scale),offset),bnds)
#            print p
#            p = [0.5*i, -0.05*i, 2*i]
#            updatePos()            
        i+=1


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
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
#from pyqtgraph.ptime import time
import subprocess
import dataAcquisitionMulti as datAc
import modelEq as modE
 
app = QtGui.QApplication([])
 
magPlot = pg.plot()
magPlot.setWindowTitle('live plot from ble')
magPlot.addLegend()
curvesRed = []
curvesRed.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.SolidLine), name='x'))
curvesRed.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.DashLine), name='y'))
curvesRed.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.DotLine), name='z'))
curvesBlue = []
curvesBlue.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.SolidLine), name='x'))
curvesBlue.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.DashLine), name='y'))
curvesBlue.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.DotLine), name='z'))
curvesGreen = []
curvesGreen.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,255,0), style=QtCore.Qt.SolidLine), name='x'))
curvesGreen.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,255,0), style=QtCore.Qt.DashLine), name='y'))
curvesGreen.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,255,0), style=QtCore.Qt.DotLine), name='z'))
curvesYellow = []
curvesYellow.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(255,255,0), style=QtCore.Qt.SolidLine), name='x'))
curvesYellow.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(255,255,0), style=QtCore.Qt.DashLine), name='y'))
curvesYellow.append(magPlot.plot(pen=pg.mkPen(color=QtGui.QColor(255,255,0), style=QtCore.Qt.DotLine), name='z'))

datax = [0]
datay = [0]
dataz = [0]
dataArrRed = dataArrBlue = dataArrGreen = dataArrYellow = np.array([[0.,0.,0.]])
#dataArr = np.empty(300)
displayArr = np.empty(shape=[0,3])
#dataArr = np.append(dataArr, np.array([0,100,200]))

cnt = 0
overcnt = 0
overcntRed = overcntBlue = overcntGreen = overcntYellow = 0
 
maxSize = 500       # amount of data, displayed on the screen

def updateMagnet(b):
    global cnt, dataArrRed, dataArrBlue, dataArrGreen, dataArrYellow, maxSize, overcntRed, overcntBlue, overcntGreen, overcntYellow
    
    if b[0] == 0:
        dataArrRed = np.append(dataArrRed, [b[1:]], axis=0)
    elif b[0] == 1:
        dataArrBlue = np.append(dataArrBlue, [b[1:]], axis=0)
    elif b[0] == 2:
        dataArrGreen = np.append(dataArrGreen, [b[1:]], axis=0)
    elif b[0] == 3:
        dataArrYellow = np.append(dataArrYellow, [b[1:]], axis=0)     
    
    cnt += 1
    factorX = 1
    if dataArrRed.shape[0]>maxSize:
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
        elif b[0] == 2:
            overcntGreen += 1
#            print "shape green: ",dataArrGreen.shape
            curvesGreen[0].setData(factorX*dataArrGreen[overcntGreen:,0])
            curvesGreen[1].setData(dataArrGreen[overcntGreen:,1])
            curvesGreen[2].setData(dataArrGreen[overcntGreen:,2])  
        elif b[0] == 3:
            overcntYellow += 1
#            print "shape yellow: ",dataArrYellow.shape
            curvesYellow[0].setData(factorX*dataArrYellow[overcntYellow:,0])
            curvesYellow[1].setData(dataArrYellow[overcntYellow:,1])
            curvesYellow[2].setData(dataArrYellow[overcntYellow:,2])                      

    else:
        if b[0] == 0:
            curvesRed[0].setData(factorX*dataArrRed[:,0])
            curvesRed[1].setData(dataArrRed[:,1])
            curvesRed[2].setData(dataArrRed[:,2])
        elif b[0] == 1:
            curvesBlue[0].setData(factorX*dataArrBlue[:,0])
            curvesBlue[1].setData(dataArrBlue[:,1])
            curvesBlue[2].setData(dataArrBlue[:,2])
        elif b[0] == 2:
            curvesGreen[0].setData(factorX*dataArrGreen[:,0])
            curvesGreen[1].setData(dataArrGreen[:,1])
            curvesGreen[2].setData(dataArrGreen[:,2])
        elif b[0] == 3:
            curvesYellow[0].setData(factorX*dataArrYellow[:,0])
            curvesYellow[1].setData(dataArrYellow[:,1])
            curvesYellow[2].setData(dataArrYellow[:,2])
    app.processEvents()     # needed?
    


#posPlot = pg.plot()
#posPlot.setWindowTitle("estimated Position")
#posPlot.addLegend()
#curvePos = []
#curvePos.append(posPlot.plot(pen=pg.mkPen(color=QtGui.QColor(255,0,0), style=QtCore.Qt.SolidLine), name='x'))
#curvePos.append(posPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,255,0), style=QtCore.Qt.SolidLine), name='y'))
#curvePos.append(posPlot.plot(pen=pg.mkPen(color=QtGui.QColor(0,0,255), style=QtCore.Qt.SolidLine), name='z'))
#overCntPos = 0
#dataArrPos = [[0.,0.,0.]]
#
#def updatePos():
#    global dataArrPos, overCntPos
##    p=[1.3,4.5,6.4]
#    dataArrPos = np.append(dataArrPos, [p], axis=0)
#    
#    if dataArrPos.shape[0]>maxSize:
#        overCntPos+=1
#        curvePos[0].setData(dataArrPos[overCntPos:,0])
#        curvePos[1].setData(dataArrPos[overCntPos:,1])
#        curvePos[2].setData(dataArrPos[overCntPos:,2])
#        
#    else:
#        curvePos[0].setData(dataArrPos[:,0])
#        curvePos[1].setData(dataArrPos[:,1])
#        curvePos[2].setData(dataArrPos[:,2])
        
# BLE acquisition
proc = subprocess.Popen("gatttool -t random -b E3:C0:07:76:53:70 --char-write-req --handle=0x000f --value=0300 --listen".split(), 
                        stdout=subprocess.PIPE, close_fds=True)
# serial acquisition
#proc = subprocess.Popen("stty -F /dev/ttyUSB0 time 50; cat /dev/ttyUSB0", 
#                        stdout=subprocess.PIPE, close_fds=True, shell=True) 
b = np.array([0.,0.,0.,0.]) 
data = np.array([[0,0.,0.,0.],
                 [1,0.,0.,0.],
                 [2,0.,0.,0.],
                 [3,0.,0.,0.]])
#s0 = [0.00920 , 0.06755, 0.]             # sensor position
#angle = [0., 0.02272, 0.01087]          # angle position of the finger
#r = 0.08829                     # length of the finger
#p = [[angle[0]+s0[0], angle[1]+s0[1]+r, s0[2]+angle[2]]]           # initial position
#
#bnds=((angle[0]+s0[0]-0.003,angle[0]+s0[0]+0.003),  # bounds for the actual finger
#      (angle[1]+s0[1],angle[1]+s0[1]+r),
#      (angle[2]+s0[2],angle[2]+s0[2]+r))
#
#scale = [ 0., 0.41656681, 0.28542467]
#offset = [ 0., 240.46739245, 5.38012971]
bla = 0
try:
    while True:          
#        while proc.stdout.readline() == None:
#            print "waiting..."
#        output = proc.stdout.readline()
#        b = datAc.structDataBLE(output)
#        print "here"
        data = datAc.RTdata(data,proc)
#        if data[0][1:].any() != 0:
#            print "waiting..."
        for d in data:
            updateMagnet(d)        
#            print bla
            bla += 1
#        else:
#            print "else..."                
        

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
        app = QtGui.QApplication.instance()
        app.exec_()
        
        print "here!"
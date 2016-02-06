''' for manipulating the jacobian from matlab '''

startString = "from __future__ import division\nfrom numpy import *\nimport handDim as h\n\n"

# function name
#startString += "def jacB_sing(mcp_I, dip_I, psi_I, mcp_M, dip_M, psi_M, mcp_R, dip_R, psi_R, mcp_P, dip_P, psi_P):\n"
startString += "def jacB_sing(mcp_I, dip_I, psi_I):\n"

# sensor positions
startString += "\t(sInd1, sInd2, sInd3) = h.sInd_car\n"
startString += "\t(sMid1, sMid2, sMid3) = h.sMid_car\n"
startString += "\t(sRin1, sRin2, sRin3) = h.sRin_car\n"
startString += "\t(sPin1, sPin2, sPin3) = h.sPin_car\n"

# joint positions
startString += "\t(jointInd1, jointInd2, jointInd3) = h.jointInd_car\n"
startString += "\t(jointMid1, jointMid2, jointMid3) = h.jointMid_car\n"
startString += "\t(jointRin1, jointRin2, jointRin3) = h.jointRin_car\n"
startString += "\t(jointPin1, jointPin2, jointPin3) = h.jointPin_car\n"

# bone lengths
startString += "\t(phalInd1, phalInd2, phalInd3) = h.phalInd\n"
startString += "\t(phalMid1, phalMid2, phalMid3) = h.phalMid\n"
startString += "\t(phalRin1, phalRin2, phalRin3) = h.phalRin\n"
startString += "\t(phalPin1, phalPin2, phalPin3) = h.phalPin\n"


line = open('jacB_sing.txt','r+').readline()
nLine = line.replace('matrix','array')
nLine = line.replace('^', '**')


jacFile = open('jacB_sing.py','w')
jacFile.write(startString + '\n')
jacFile.write('\treturn ' + nLine)
jacFile.close()

print "finished"
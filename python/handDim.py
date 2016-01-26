import numpy as np

''' static values for the dimensions on the hand '''

# lengths of the phalanges
#           prox-,   int-,     dist-    phalanges
phalInd = np.array([0.03080, 0.02581, 0.01678])
phalMid = np.array([0.03593, 0.03137, 0.01684])
phalRin = np.array([0.03404, 0.02589, 0.01820])
phalPin = np.array([0.02892, 0.02493, 0.01601])

''' the origin of the coordinate systems is the joint of the index finger '''

# sensor positions Cartesian (aligned like sensor)
# for dipole approach
sInd_car = np.array([-0.03, -0.0, 0.024] )    # rack1
sMid_car = np.array([-0.03, -0.02, 0.024])
sRin_car = np.array([-0.03, -0.04, 0.024])
sPin_car = np.array([-0.03, -0.06, 0.024])
#sInd_car = [-0.03, -0.0, 0.024]     # rack2
#sMid_car = [-0.05, -0.022, 0.024]
#sRin_car = [-0.03, -0.044, 0.024]
#sPin_car = [-0.05, -0.066, 0.024]

# for cylindrical approach
sInd_carC = np.array([0.03, -0.0, -0.024] )    # rack1
sMid_carC = np.array([0.03, -0.02, -0.024])
sRin_carC = np.array([0.03, -0.04, -0.024])
sPin_carC = np.array([0.03, -0.06, -0.024])

# joint positions Cartesian
jointInd_car = np.array([0.0, 0.0, -0.0])
jointMid_car = np.array([0.0, -0.02, 0.0])
jointRin_car = np.array([0.0, -0.04, 0.0])
jointPin_car = np.array([0.0, -0.06, -0.0])

# jointInd_car = np.array([0.0, 0.0, -0.0])
# jointMid_car = np.array([0.0, -0.02, 0.0])
# jointRin_car = np.array([0.0, -0.04, 0.0])
# jointPin_car = np.array([0.0, -0.06, -0.0])

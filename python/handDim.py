import numpy as np

''' static values for the dimensions on the hand '''

# lengths of the phalanges
#           prox-,   int-,     dist-    phalanges
phalInd = np.array([0.03080, 0.02581, 0.01678])
phalMid = np.array([0.03593, 0.03137, 0.01684])
phalRin = np.array([0.03404, 0.02589, 0.01820])
phalPin = np.array([0.02892, 0.02493, 0.01601])

# my own dimensions:
phalInd_m = np.array([0.05022, 0.02968, 0.01718])
phalMid_m = np.array([0.06081, 0.03430, 0.01790])
phalRin_m = np.array([0.05520, 0.03146, 0.01695])
phalPin_m = np.array([0.04348, 0.02278, 0.01674])

''' the origin of the coordinate systems is the joint of the index finger '''

# sensor positions Cartesian (aligned like sensor)
# for dipole approach
sInd_car = np.array([-0.03, -0.0,  0.025])    # rack1
sMid_car = np.array([-0.03, -0.02, 0.025])
sRin_car = np.array([-0.03, -0.04, 0.025])
sPin_car = np.array([-0.03, -0.06, 0.025])

# my own dimensions
# TODO measure them really!
# sInd_car_m = np.array([0, -0.0,  0])    # rack1
# sMid_car_m = np.array([-0.03, -0.02, 0.025])
# sRin_car_m = np.array([-0.03, -0.04, 0.025])
# sPin_car_m = np.array([-0.03, -0.06, 0.025])


# joint positions Cartesian
jointInd_car = np.array([0.0,  0.0,  -0.0])
jointMid_car = np.array([0.0, -0.02,  0.0])
jointRin_car = np.array([0.0, -0.04,  0.0])
jointPin_car = np.array([0.0, -0.06, -0.0])

# my own dimensions
jointInd_m = np.array([0.0,           0.0,  0.0])
jointMid_m = np.array([0.0,      -0.02516,  0.0])
jointRin_m = np.array([-0.01152, -0.05091,  0.0])
jointPin_m = np.array([-0.01152, -0.06892,  0.0])


# jointInd_car = np.array([0.0, 0.0, -0.0])
# jointMid_car = np.array([0.0, -0.02, 0.0])
# jointRin_car = np.array([0.0, -0.04, 0.0])
# jointPin_car = np.array([0.0, -0.06, -0.0])

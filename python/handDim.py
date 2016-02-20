import numpy as np

''' static values for the dimensions on the hand '''

# WOODEN HAND
#           prox-,   int-,     dist-    phalanges
# phalInd = np.array([0.03080, 0.02581, 0.01678])
# phalMid = np.array([0.03593, 0.03137, 0.01684])
# phalRin = np.array([0.03404, 0.02589, 0.01820])
# phalPin = np.array([0.02892, 0.02493, 0.01601])

# OWN HAND
phalInd = np.array([0.05022, 0.02968, 0.01718])
phalMid = np.array([0.06081, 0.03430, 0.01790])
phalRin = np.array([0.05520, 0.03146, 0.01695])
phalPin = np.array([0.04348, 0.02278, 0.01674])

''' the origin of the coordinate systems is the joint of the index finger '''

# WOODEN HAND
# sensor positions Cartesian (aligned like sensor)
# sInd = np.array([-0.03, -0.0,  0.025])    # rack1
# sMid = np.array([-0.03, -0.02, 0.025])
# sRin = np.array([-0.03, -0.04, 0.025])
# sPin = np.array([-0.03, -0.06, 0.025])

# OWN HAND

# sInd = np.array([-0.012, -0.004,  0.026])    # for 160209
# sMid = np.array([-0.012, -0.024, 0.026])
# sRin = np.array([-0.012, -0.044, 0.026])
# sPin = np.array([-0.012, -0.064, 0.026])

sInd = np.array([-0.02,  -0.009, 0.030])      # for 160210 NEAR to joints
sMid = np.array([-0.02,  -0.029, 0.030])
sRin = np.array([-0.018, -0.049, 0.030])
sPin = np.array([-0.016, -0.069, 0.030])

# sInd = np.array([-0.057,  -0.00, 0.027])      # for 160210 FAR from joints
# sMid = np.array([-0.057,  -0.02, 0.027])
# sRin = np.array([-0.051, -0.04, 0.027])
# sPin = np.array([-0.048, -0.06, 0.027])

# sInd = np.array([-0.017,  -0.008, 0.030])      # for 160212 NEAR to joints
# sMid = np.array([-0.017,  -0.028, 0.030])
# sRin = np.array([-0.015, -0.048, 0.030])
# sPin = np.array([-0.015, -0.068, 0.030])

# sInd = np.array([-0.021,  -0.006, 0.026])      # for 160217 NEAR to joints
# sMid = np.array([-0.021,  -0.026, 0.026])
# sRin = np.array([-0.017, -0.046, 0.026])
# sPin = np.array([-0.017, -0.066, 0.026])


# WOODEN HAND
# joint positions Cartesian
# jointInd = np.array([0.0,  0.0,  -0.0])
# jointMid = np.array([0.0, -0.02,  0.0])
# jointRin = np.array([0.0, -0.04,  0.0])
# jointPin = np.array([0.0, -0.06, -0.0])

# OWN HAND
jointInd = np.array([0.0,           0.0,  0.0])
jointMid = np.array([0.0,      -0.02516,  0.0])
jointRin = np.array([-0.01152, -0.05091,  0.0])
jointPin = np.array([-0.01152, -0.06892,  0.0])

import numpy as np
import modelDip as modD
import matplotlib.pyplot as plt
import plotting as plo
import EKF as kalman


def jacoCalcB(rx,ry,rz):
    ''' First derivative of dip function for H = [1,0,0]
        imported from Matlab... '''
    J = np.array([
        [(18303781807138305.*rx)/(2305843009213693952.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) + (18303781807138305.*abs(rx)*np.sign(rx))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx**2*abs(rx)*np.sign(rx))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)), 
         (18303781807138305.*abs(ry)*np.sign(ry))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx**2*abs(ry)*np.sign(ry))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)), 
         (18303781807138305.*abs(rz)*np.sign(rz))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx**2*abs(rz)*np.sign(rz))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2))],
        
        [ (18303781807138305.*ry)/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx*ry*abs(rx)*np.sign(rx))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)),
         (18303781807138305.*rx)/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx*ry*abs(ry)*np.sign(ry))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)),
        -(91518909035691525.*rx*ry*abs(rz)*np.sign(rz))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2))],

        [(18303781807138305.*rz)/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx*rz*abs(rx)*np.sign(rx))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)),
         -(91518909035691525.*rx*rz*abs(ry)*np.sign(ry))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2)),
         (18303781807138305.*rx)/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(5./2)) - (91518909035691525.*rx*rz*abs(rz)*np.sign(rz))/(4611686018427387904.*(abs(rx)**2 + abs(ry)**2 + abs(rz)**2)**(7./2))]])
    
    return J



def EKF_predict_dip(x, P_old, Q):
    
    x_pred = x
    P_pred = P_old + Q
    
    return (x_pred, P_pred)



def EKF_update_dip(jaco, meas, x_pred, P_pred, R):
    
    c = jaco(x_pred[0], x_pred[1], x_pred[2])
    
    g = np.dot(np.dot(P_pred, c.T), np.linalg.inv(np.dot(np.dot(c, P_pred), c.T) + R))
    
    x_now = x_pred + np.dot(g, (meas - modD.calcB(x_pred,np.array([1., 0., 0]))))
#    dif = meas - calcB_dip(x_pred(1:3)',[1 0 0])'
    
    P_now = np.dot((np.eye(3) - np.dot(g, c)), P_pred)
    
    return (x_now, P_now)    
    

#a = jacoMatlab(0.04, 0., 0.)

''' data simulation '''

p = 0.5
h = np.array([1., 0., 0.])
t = np.arange(0.04, 0.1, 0.001)

r = np.zeros((len(t),3))
b_sim = np.zeros((len(t),3))
b_sim_noise = np.zeros((len(t),3))

cnt = 0
for i in t:
    r[cnt] = np.array([i, 0., 0.])
    
    b_sim[cnt] = modD.calcB(r[cnt], h)
    b_sim_noise[cnt] = modD.calcB(r[cnt], h) + p*np.random.randn(1,3) + [0.5, -1.8, 2.0]
#    b_sim_noise[cnt] = modD.calcB(r[cnt], h) + [0.5, -1.8, 2.0]

    cnt += 1    
    
#plt.close('all')    
#plo.plotter2d((b_sim, b_sim_noise), ("simulated", "sim Noisy"))


''' Kalman stuff '''

# error covariance matrix (3x3), gets updated each step, so the initial one is not so important...
P = np.eye(3)

# process noise covariance matrix (3x3)
Q = np.array([[1e+2, 1e-10, 1e-10],
              [1e-10, 1e-2, 1e-10],
              [1e-10, 1e-10, 1e-2]])
                
# measurement noise covariance matrix (3x3)                
R = np.zeros((3,3))         
#R = np.diag([1e-10, 1e-10, 1e-10])                


x_EKF = np.zeros((len(t)+1, 3))
x_EKF[0] = r[0]

cnt = 1
for i in b_sim_noise:
#for i in b_sim:
#    print "---------step ",cnt,"--------"

    (x_p, P_p) = kalman.EKF_predict_dip(x_EKF[cnt-1], P, Q)
#    print "x_p\n", x_p
#    print "P_p\n", P_p
    
    (x_EKF[cnt], P) = kalman.EKF_update_dip(kalman.jacoCalcB, i, x_p, P_p, R)

    cnt += 1    



x_est = np.zeros((len(t)+1, 3))
x_est[0] = r[0]

cnt = 0
for i in b_sim_noise:
    print "---------normal estimation step ",cnt,"--------"
    tmp = modD.estimatePos(x_est[cnt], h, i)
    x_est[cnt+1] = tmp.x
    
    cnt += 1


#plt.figure()
plo.plotter2d((x_EKF[:-2],x_est),("EKF states","estimated states"))
plt.show()










import numpy as np
import modelDip as modD


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


def jacoAngToB(mcp, dip):



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
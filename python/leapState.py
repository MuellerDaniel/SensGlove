################################
################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys, thread, time
sys.path.append('/usr/local/lib/leap')
import Leap, subprocess
import numpy as np
import sys,signal


''' routine for recognizing the sigint '''
def cleanup(signum, frame):
    print "leapState end..."
#    controller.remove_listener(listener)
    sys.exit()


''' Avg Framerate, system running alone:
    9062 mu_s -> f = 110 Hz '''



class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    joint_names = ['MCP', 'PIP', 'DIP']

    stateFile = open("160226_leap",'w')
    upCnt = 0


    def getFlexionAngles(self,finger,hand):
        angleStr = " "
#        print self.finger_names[finger.type]
#        theta_mcp = np.pi - hand.direction.angle_to(finger.bone(Leap.Bone.TYPE_PROXIMAL).direction)
        theta_mcp = hand.palm_normal.angle_to(finger.bone(Leap.Bone.TYPE_PROXIMAL).direction) - np.pi/2.    # take the normal, since it leads better results
#        print "angle: ", theta_mcp
        angleStr += str(theta_mcp) + " "
        for b in range(1, 4):
            bone = finger.bone(b)
            if b < 3:
                jointAngleTo = bone.direction.angle_to(finger.bone(b+1).direction)

#                print "joint angle %s : %s (rad)" % (self.joint_names[b],
#                          jointAngleTo)
                angleStr += str(jointAngleTo) + " "

        angleStr += self.getAbductionAngles(finger,hand)    # for ad-ab angle
        return angleStr



    # angle between two fingers
    def getAbductionAngles(self,fing, hand):
        handD_V = hand.direction
        handD_V.y = 0
        handD_V = handD_V.normalized

        fing_V = -fing.bone(Leap.Bone.TYPE_PROXIMAL).direction
        fing_V.y = 0
        fing_V = fing_V.normalized

        ang = handD_V.angle_to(fing_V)
        cross = handD_V.cross(fing_V)
        direc = hand.palm_normal.dot(cross)

        if direc < 0: ang *= -1
#        print ang

        return str(ang)




    def on_exit(self, controller):
        self.stateFile.close()
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
#        print "controller up..."
        frame = controller.frame()

        # Get hands
        if len(frame.hands) > 0:
            if self.upCnt == 0:
                print "LEAP up!"
                self.upCnt += 1
            for hand in frame.hands:
#                 print "LEAP: hand detected"
                 angleString = "leap " + str(frame.timestamp) + " "
                 for finger in hand.fingers:
                     if finger.type == Leap.Finger.TYPE_THUMB:
                         continue
                     angleString += self.getFlexionAngles(finger,hand)

            print "LEAP\tUP"
#            print angleString
            self.stateFile.write(angleString + '\n')

        else:
            print "LEAP down..."
            self.upCnt = 0








def main():

    signal.signal(signal.SIGINT, cleanup)

#    try:
#        sys.stdin.readline()
#    except KeyboardInterrupt:
#        pass

    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)


    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    signal.signal(signal.SIGINT, cleanup)
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass

    finally:
        print "in finaly..."
        # Remove the sample listener when done
        controller.remove_listener(listener)
#        f.close()


if __name__ == "__main__":
    main()

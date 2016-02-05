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

''' Avg Framerate, system running alone: 9062 µs -> f = 110 Hz '''

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    joint_names = ['MCP', 'PIP', 'DIP']
    
    stateFile = open("anglesLeap.txt",'w')
    
    
    def getFlexionAngles(self,finger):
        # print "here..."
        print "Flexion angles for ", self.finger_names[finger.type]
        angleStr = ""
        for b in range(0, 4):
            bone = finger.bone(b)
            if b < 3:
                jointAngleTo = bone.direction.angle_to(finger.bone(b+1).direction)
                print "joint angle %s : %s (rad), %s (deg)" % (self.joint_names[b],
                          jointAngleTo, np.rad2deg(jointAngleTo))
                angleStr += str(jointAngleTo) + " "
        
        return angleStr                
                          
    

    def getAbductionAngles(self,hand):
        for f in range(1,4):
            fingerA = hand.fingers[f]
            dA = fingerA.bone(Leap.Bone.TYPE_PROXIMAL).direction
            fingerB = hand.fingers[f+1]
            dB = fingerB.bone(Leap.Bone.TYPE_PROXIMAL).direction
            angle = dA.angle_to(dB)

            crossP = dA.cross(dB)
            di = hand.palm_normal.dot(crossP)

            if di < 0:
                angle *= -1

            print "angle between %s and %s: %s (rad), %s (deg) " % (
                    self.finger_names[fingerA.type] , self.finger_names[fingerB.type],
                    angle, np.rad2deg(angle))


    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"
        
    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        self.stateFile.close()
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information

        frame = controller.frame()
#        f = open(self.fileName,'w')

        # Get hands
        if len(frame.hands) > 0:
            for hand in frame.hands:
#                 self.getAbductionAngles(hand)               
                 angleString = str(frame.timestamp)
                 
                 for finger in hand.fingers:
                     if finger.type == Leap.Finger.TYPE_THUMB:
                         continue
                     angleString += " " + self.getFlexionAngles(finger)
            
            self.stateFile.write(angleString + '\n')
                 
       
           




def main():

    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)
#        f.close()
        # subPro.kill()


if __name__ == "__main__":
    main()

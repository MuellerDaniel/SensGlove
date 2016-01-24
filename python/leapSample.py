################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import sys, thread, time
sys.path.append('/usr/local/lib/leap')
import Leap, subprocess
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import numpy as np



class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    joint_names = ['MCP', 'PIP', 'DIP']

    fileName = 'leapFile.txt'
    # f = open(fileName,'w')
    zString = "0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000\n"


    def getFlexionAngles(self,finger):
        # print "here..."
        print "Flexion angles for ", self.finger_names[finger.type]
        for b in range(0, 4):
            bone = finger.bone(b)
            if b < 3:
                jointAngleTo = bone.direction.angle_to(finger.bone(b+1).direction)
                print "joint angle %s : %s (rad), %s (deg)" % (self.joint_names[b],
                          jointAngleTo, np.rad2deg(jointAngleTo))


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

        # Enable gestures
        # controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        # controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        # controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        # controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        # self.f.close()
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
#        time.sleep(2)
        frame = controller.frame()
        f = open(self.fileName,'w')
        # print "Frame available"
        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        #        frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        if len(frame.hands) > 0:
            for hand in frame.hands:
                 self.getAbductionAngles(hand)
                #  index = hand.fingers[1]
                #  indexProx = index.bone(Leap.Bone.TYPE_PROXIMAL)
                #  middle = hand.fingers[2]
                #  middleProx = middle.bone(Leap.Bone.TYPE_PROXIMAL)
                #  print "direction index: %s, direction middle:%s" % (
                #             indexProx.direction,
                #             middleProx.direction)
                #  angle = indexProx.direction.angle_to(middleProx.direction)
                #  print "angle %s (rad), %s (deg) " % (angle, np.rad2deg(angle))

                 angleString = "0.000 0.000 0.000 "
                 for finger in hand.fingers:
                     if finger.type == Leap.Finger.TYPE_THUMB:
                         continue
                    #  print self.finger_names[finger.type]
                     self.getFlexionAngles(finger)
                    #  print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                    #      self.finger_names[finger.type],
                    #      finger.id,
                    #      finger.length,
                    #      finger.width)

                     # Get bones
                    #  for b in range(0, 4):
                    #      bone = finger.bone(b)
                    #      if b < 3:
                    #          jointCross = bone.direction.dot(finger.bone(b+1).direction)
                    #          jointAngle_rad = np.arccos(jointCross)
                    #          jointAngle_deg = np.rad2deg(jointAngle_rad)
                     #
                    #          jointAngleTo = bone.direction.angle_to(finger.bone(b+1).direction)
                     #
                    #         #  angleString += str(jointAngle_rad) + " "       # for blender
                     #
                    #          print "joint angle(cross) %s : %s (rad), %s (deg)" % (self.joint_names[b],
                    #                     jointAngle_rad, jointAngle_deg)
                    #          print "joint angle(angleTo) %s : %s (rad), %s (deg)" % (self.joint_names[b],
                    #                    jointAngleTo, np.rad2deg(jointAngleTo))

                # self.f.write(str(frame.id) + '\t' + self.joint_names[b] + '\t' + str(jointAngle) + '\n' )
                 f.write(angleString + '\n')
                #  print angleString
                            #  f.close()
        else:
            f.write(self.zString)
            print(self.zString)
        f.close()




def main():
    # Create a sample listener and controller
    f = open('leapFile.txt','w')

    blendCmd = "./../visualization/riggedAni/HandGame.blend " + 'leapFile.txt'
    # subPro = subprocess.Popen(blendCmd.split())

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
        f.close()
        # subPro.kill()


if __name__ == "__main__":
    main()

# the server

import socket, time,subprocess, select

def doEstimation(counter):
    outstr = "0.0000 0.0000 0.0000"
    for i in range(12):
        outstr = outstr+" {0:.4f}".format(counter)
    time.sleep(0.3)
    return outstr

UDP_IP = "127.0.1.6"
UDP_PORT = 5511
counter = 0.0001
sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#sock.bind((UDP_IP,UDP_PORT))

cmd = "python udpReceive.py"
#cmd = "./../SensGlove/visualization/blend-file/gameSock.blend"
#cmd = "./../SensGlove/visualization/sockTestGame.blend"
#cmd = "./RiggedsockTest.blend"
#cmd = "./../visualization/riggedAni/HandGame.blend"
subpro = subprocess.Popen(cmd.split())

tosend = "0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000"
#global msg
#msg = tosend
#doEstimation(counter)
try:
    while True:
        #data, addr = sock.recvfrom(1024)    # receive a message from the game, to determine its current address
        # try it with a select method... -> doesn't work, because you have no file IO
        # while doEstimation in select.select([doEstimation(counter)],[],[],0)[0]:
        #     tosend = doEstimation(counter)
        #     counter += 0.0051
        # else:
        #     sock.sendto(tosend,addr)

        # the blocking method...
        tosend = doEstimation(counter)
        counter += 0.0051
        #sock.sendto(tosend, addr)
        sock.sendto(tosend, (UDP_IP,UDP_PORT))
        print "sent message!"
        print "fileno: ",sock.fileno()

except KeyboardInterrupt:
    print "interrupted"
    print "send ",counter
    sock.close()

# import socket,time
# import sys
#
# # Create a TCP/IP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# # Bind the socket to the port
# server_address = ('localhost', 10000)
# print >>sys.stderr, 'starting up on %s port %s' % server_address
# sock.bind(server_address)
#
# print >>sys.stderr, '\nwaiting to receive message'
# data, address = sock.recvfrom(4096)
# print "received this: ",data
# counter = 0.0001
# while True:
#     outstr = "0.0000 0.0000 0.0000"
#     for i in range(12):
#         outstr = outstr+" {0:.4f}".format(counter)
#     sent = sock.sendto(outstr, address)
#     print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)
#     time.sleep(0.5)

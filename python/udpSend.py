import socket, time,subprocess

UDP_IP = "127.0.1.1"
UDP_PORT = 5511
counter = 0.0001
sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
#sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

#cmd = "python udpReceive.py"
#cmd = "./../SensGlove/visualization/blend-file/gameSock.blend"
#cmd = "./../SensGlove/visualization/sockTestGame.blend"
#cmd = "./RiggedsockTest.blend"
cmd = "./../SensGlove/visualization/riggedAni/HandGame.blend"
#subpro = subprocess.Popen(cmd.split())
try:
    while True:
        outstr = "0.0000 0.0000 0.0000 "
        for i in range(12):
            outstr = outstr+" {0:.4f}".format(counter)
        sock.sendto(outstr, (UDP_IP, UDP_PORT))
        print "sent message!"
        counter += 0.0001
        time.sleep(0.5)

except KeyboardInterrupt:
    print "interrupted"


'''
    Simple udp socket server
    Silver Moon (m00n.silv3r@gmail.com)
'''
#import socket,time
#import sys
#
#HOST = ''   # Symbolic name meaning all available interfaces
#PORT = 8888 # Arbitrary non-privileged port
#
## Datagram (udp) socket
#try :
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    print 'Socket created'
#except socket.error, msg :
#    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#    sys.exit()
#
#
## Bind socket to local host and port
#try:
#    s.bind((HOST, PORT))
#except socket.error , msg:
#    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#    sys.exit()
#
#print 'Socket bind complete'
#
#clientUp = False
#counter = 0.0001
##now keep talking with the client
#while 1:
#    # receive data from client (data, addr)
##    d = s.recvfrom(1024)
##    data = d[0]
##    addr = d[1]
#    if clientUp:
#        outstr = "0.0000 0.0000 0.0000"
#        for i in range(12):
#            outstr = outstr+" {0:.4f}".format(counter)
#        s.sendto(outstr,(HOST,PORT))
#        counter += 0.0001
#        time.sleep(0.2)
#    else:
#        if s.recvfrom(1024)[0] == "start":
#            clientUp = True
#        else:
#            print "waiting..."
##    if not data:
##        break
#
##    reply = 'OK...' + data
#
##    s.sendto(reply , addr)
##    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
#
#s.close()

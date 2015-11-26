# the client...

import socket, select

UDP_IP = "127.0.1.6"
UDP_PORT = 5511

#sock = socket.socket(socket.AF_INET, # Internet
                     #socket.SOCK_DGRAM) # UDP
#sock = socket.fromfd(3,socket.AF_INET,socket.SOCK_DGRAM)
#sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#sock.bind((UDP_IP, UDP_PORT))
epoll = select.epoll()
sock = epoll.fromfd(3)
msg = " "
cnt = 0

#sock.sendto("ready!",(UDP_IP,UDP_PORT))

try:
    while True:
        #while sock in select.select([sock],[],[],0)[0]:
        data, addr = sock.recvfrom(104) # buffer size is 1024 bytes
        msg = data
        cnt += 1
        print "!!!!NEW MESSAGE!!!! ", msg
        #else:
        #    print "received message:", msg
        # try:
        #     data, addr = sock.recvfrom(104)
        #     print "received",data
        #     cnt += 1
        # except:
        #     print "ooh...."
except KeyboardInterrupt:
    print "ended!"
    print "received ",cnt
    sock.close()


# import socket
# import sys
#
# # Create a UDP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# server_address = ('localhost', 10000)
# message = 'This is the message.  It will be repeated.'
# # Send data
# print >>sys.stderr, 'sending "%s"' % message
# sent = sock.sendto(message, server_address)
#
# while True:
#
#     # Receive response
#     print >>sys.stderr, 'waiting to receive'
#     data, server = sock.recvfrom(4096)
#     print >>sys.stderr, 'received "%s"' % data

# finally:
#     print >>sys.stderr, 'closing socket'
#     sock.close()

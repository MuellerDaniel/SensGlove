import socket, select

UDP_IP = "127.0.1.1"
UDP_PORT = 5511

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((UDP_IP, UDP_PORT))
msg = " "
cnt = 0

try:
    while True:
        while sock in select.select([sock],[],[],0)[0]:
            data, addr = sock.recvfrom(104) # buffer size is 1024 bytes
            msg = data
            cnt += 1
            print "NEW MESSAGE!!!!"
        else:
            print "received message:", msg
except KeyboardInterrupt:
    print "ended!"
    print cnt
    


'''
    udp socket client
    Silver Moon
'''
#import socket   #for sockets
#import sys  #for exit
#
## create dgram udp socket
#try:
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#except socket.error:
#    print 'Failed to create socket'
#    sys.exit()
#
#host = 'localhost';
#port = 8888;
#
#s.sendto("start",(host,port))
#
#while(1) :
##    msg = raw_input('Enter message to send : ')
#    try :
#        #Set the whole string
##        s.sendto(msg, (host, port))
#
#        # receive data from client (data, addr)
#        d = s.recvfrom(1024)
#        reply = d[0]
#        addr = d[1]
#
#        print 'Server message : ' + reply
#
#    except socket.error, msg:
#        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#        sys.exit()

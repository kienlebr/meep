#! /usr/bin/env python
import sys
import os
import socket
import miniapp

import time
import threading

def handle_connection(sock):
    print 'handling connection...'
    index = 0;
    endset = "\r\n\r\n"
    recieved = ''
    data = ''
    while 1:
        try:
            recieved = sock.recv(1)
            data += recieved;
            if recieved == endset[index]:
                index+=1
            else:
                index = 0
            if index == 4:
                if("POST" in data[0:5]):
                    content = data.find("Content-Length:")
                    content += 16
                    #print "MAH CONTENT LENGTHES!: "
                    length = ''
                    while(data[content].isdigit()):
                        length += data[content]
                        content += 1
                    recieved = sock.recv(int(content))
                    #print recieved
                    data += recieved
                break;
            if not data:
                print 'no data recieved'
                break

        except socket.error:
            return

    #print 'data:', (data,)
    data = miniapp.format_return(data)

    #print 'data:', (data,)
    data = str(data)
    #print 'data:', (data,)

    sock.sendall(data)
    print "data sent"
    sock.close()
    print "Done"

#Dependency Injection
#Woooo
#class _fake_socket(object):
#    closed = False
#    def recv(self, size):
#        return 'some data.\r\n'
#    
#    def sendall(self, data):
#        assert data == 'some data.\r\n'
#        
#    def close(self):
#        self.closed = True
#        
#handle_connection(_fake_socket())

if __name__ == '__main__':
    #interface, port = sys.argv[1:3]

    port = 80
    interface = 'localhost'

    print 'binding', interface, port
    sock = socket.socket()
    sock.bind( (interface, port) )
    sock.listen(5)
    #threads = []
    while 1:
        print 'waiting...'
        (client_sock, client_address) = sock.accept()
        print 'got connection', client_address
        #print client_sock
        handle_connection(client_sock)


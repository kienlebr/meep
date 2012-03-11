#! /usr/bin/env python
import sys
import os
import socket
import miniapp

def handle_connection(sock):
    print 'handling connection...'
    try:
        print 'recieving data...'
        data = ''
        recieved = sock.recv(1024)
        if(recieved):
            while(1):
                data += recieved
                if len(recieved) < 1024:
                    break
                else:
                    recieved = sock.recv(1024)
        elif not data:
            print 'no data recieved'
            return
        print 'data recieved...'
        print ''
        print data
        print ''

        #print 'data:', (data,)
        data = miniapp.format_return(data)

        #print 'data:', (data,)
        data = str(data)
        #print 'data:', (data,)

        sock.sendall(data)
        print "data sent"
        sock.close()

    except socket.error:
        return
print "Done"

if __name__ == '__main__':
    #interface, port = sys.argv[1:3]

    port = 8000
    interface = 'localhost'

    print 'binding', interface, port
    sock = socket.socket()
    sock.bind( (interface, port) )
    sock.listen(5)

    while 1:
        print 'waiting...'
        (client_sock, client_address) = sock.accept()
        print 'got connection', client_address
        #print client_sock
        handle_connection(client_sock)


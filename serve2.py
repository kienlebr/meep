#! /usr/bin/env python
import sys
import os
import socket
import miniapp

def handle_connection(sock):
    print 'handling connection...'
    while 1:
        try:
            print 'recieving data...'
            data = sock.recv(4096)
            print 'data recieved...'
            if not data:
                print 'No data...'
                break

            #print 'data:', (data,)
            data = miniapp.format_return(data)

            #print 'data:', (data,)
            data = str(data)
            #print 'data:', (data,)

            sock.sendall(data)
            print "data sent"
            sock.close()
            break

        except socket.error:
            break
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


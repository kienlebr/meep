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


if __name__ == '__main__':
    #interface, port = sys.argv[1:3]

    port = 8000
    interface = 'localhost'

    print 'binding', interface, port
    sock = socket.socket()
    sock.bind( (interface, port) )
    sock.listen(5)
    threads = []
    while 1:
        print 'waiting...'
        (client_sock, client_address) = sock.accept()
        print 'got connection', client_address
        T1 = threading.Thread(target=handle_connection, args=(client_sock,));
        T1.run();
        #print client_sock
        handle_connection(client_sock)


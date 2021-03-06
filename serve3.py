#! /usr/bin/env python
import sys
import os
import socket
import miniapp
import meep_example_app

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
            if endset in data:
                if("POST" in data[0:5]):
                    content = data.find("Content-Length:")
                    content += 16
                    #print "MAH CONTENT LENGTHES!: "
                    length = int(data[content:].split()[0])
                    #while(data[content].isdigit()):
                    #    length += data[content]
                    #    content += 1
                    #print "LENGTH: ", length
                    if length:
                        recieved = sock.recv(int(length))
                        #print recieved
                        data += recieved
                break;
            if not data:
                print 'no data recieved'
                break

        except socket.error:
            return
    if data:
        #print 'data:', (data,)
        data = miniapp.format_return(data)

        #print 'data:', (data,)
        data = str(data)
        #print 'data:', (data,)

        sock.sendall(data)
        print "data sent"
    else:
        print 'No data'
    sock.close()
    print "Done"



if __name__ == '__main__':
    #interface, port = sys.argv[1:3]

    port = 80
    interface = 'localhost'
    meep_example_app.initialize()

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
        #t1 = threading.Thread(target=handle_connection, args=(client_sock,));
        #t1.start()
        handle_connection(client_sock)


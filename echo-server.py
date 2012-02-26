#! /usr/bin/env python
import sys
import socket

def handle_connection(sock):
    print 'Handling connection...'
    while 1:
        try:
            print 'Recieving data...'
            data = sock.recv(4096)
            print 'Data recieved...'
            if not data:
                break

            print 'data:', (data,)

            print 'Sending data...'
            sock.sendall(data)
            print 'Data sent...'

            if '.\r\n' in data:
                sock.close()
                break
        except socket.error:
            break

if __name__ == '__main__':
    interface, port = sys.argv[1:3]
    port = int(port)

    print 'binding', interface, port
    sock = socket.socket()
    sock.bind( (interface, port) )
    sock.listen(5)

    while 1:
        print 'waiting...'
        (client_sock, client_address) = sock.accept()
        print 'got connection', client_address
        handle_connection(client_sock)
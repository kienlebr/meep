#! /usr/bin/env python
import sys
import os
import socket

interface, port, message = sys.argv[1:4]
port = int(port)

sock = socket.socket()

print 'connecting to', interface, port
sock.connect((interface, port))

filename = '1-request.txt'
fp = open(filename, 'rb')
text = fp.read()
message = text
print message


print 'sending %d bytes' % len(message)
sock.sendall(message)

print 'received:'
x = sock.recv(4096)
print (x,)
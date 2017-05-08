"""
Example demontsrating how TCP communcation may be set up with the BB using
client to client communication over sockets and a server. To run the example,
open three terminals and write, in order,

In terminal 1: python TCPServer.py
In terminal 2: python TCPClientA.py
In terminal 3: python TCPClientB.py 

After which the terminals running client A and client B may communcate over the
IP network using the pythonBeagle module.
"""
# Import modules
import sys
import os
import inspect
import socket

curdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
pardir = os.path.dirname(os.path.dirname(curdir))
moddir = os.path.join(pardir, "modules")
sys.path.insert(0,moddir) 
from pythonBeagle import ServerThread

# Setup server
ipHost = "0.0.0.0"
port = 1724

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ipHost, port))
server.listen(2)

# Main program
print "Waiting to accept the clients"
try:
    clientA, addressA = server.accept() 
    clientB, addressB = server.accept()
    c1 = ServerThread(clientA, clientB, size=1024)
    c2 = ServerThread(clientB, clientA, size=1024)
    c1.start()
    c2.start()
except:
    raise("There was an error in connecting the clients")

print "Both clients accepted, ready to communicate"
cont = True
while c1.isAlive() and c1.isAlive() and cont:
    try:
        continue
    except KeyboardInterrupt:
        print "Exiting"
        clientA.close()
        clientB.close()
        cont = False

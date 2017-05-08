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
from pythonBeagle import SenderThread, ReceiverThread

# Uncomment to run on the local network
#adress = (192.168.7.2', 1724)

# Uncomment to run on the local network
adress = ('127.0.0.1', 1724)

# Set up sockets and create sender and receiver threads
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(adress)

sender = SenderThread(client=client, protocol="TCP")
sender.start()

receiver = ReceiverThread(client=client, protocol="TCP", verbose=True)
receiver.start()

# Main program
while sender.isAlive() and receiver.isAlive():
    data = raw_input("Enter:")
    sender.send_data(data)

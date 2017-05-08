"""
Example demonstrating how UDP communcation may be set up with the BB using
client to client communication over sockets. To run the example, open two
terminals and write

In terminal 1: python UDPClientA.py
In terminal 2: python UDPClientB.py 

After which the terminals may communcate over the IP network using the
pythonBeagle module.
"""

# Import modules
import sys
import os
import inspect

curdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
pardir = os.path.dirname(os.path.dirname(curdir))
moddir = os.path.join(pardir, "modules")
sys.path.insert(0,moddir) 
from pythonBeagle import SenderThread, ReceiverThread

# Set up senders and receivers
senderAddress = ('127.0.0.1', 1724)
sender = SenderThread(address=senderAddress, protocol="UDP")
sender.start()

receiverAddress = ('127.0.0.1', 5004)
receiver = ReceiverThread(address=receiverAddress, protocol="UDP", verbose=True)
receiver.start()

# Main loop
while sender.isAlive():
    data = raw_input("Enter:")
    sender.send_data(data)
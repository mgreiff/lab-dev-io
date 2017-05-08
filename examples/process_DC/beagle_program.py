import sys
import os
import inspect
import numpy as np
import time as tt

curdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
pardir = os.path.dirname(os.path.dirname(curdir))
moddir = os.path.join(pardir, "modules")
sys.path.insert(0,moddir) 
from pythonBeagle import SenderThread, ReceiverThread, encode_hex_to_array, encode_array_to_hex, DCmotor

## Create sender and receiver threads ###
senderAddress = ('127.0.0.1', 5004)
sender = SenderThread(address=senderAddress, protocol="UDP")
sender.start()

receiverAddress = ('127.0.0.1', 1724)
receiver = ReceiverThread(address=receiverAddress, protocol="UDP", size=16) # 16 characters per entry, on reference
receiver.start()

### Main program ###
loopRate = 30.0                  # [Hz]
h = 1.0/loopRate                 # [s]
Nref = 1                         # Number of references
Nstate = 3                       # Number of states
references = np.zeros((Nref,1))  # References sent to the DC motor open loop
states = np.zeros((Nstate,1))    # State responses
loopTime = np.array([])          # Loop times
execTime = np.array([])          # Execution times
startTime = tt.time()            # Time at which the main loop starts

# Instantiate the motor object
x0 = np.zeros((3,1))
parameters = {
    "x0": x0,
    "J": 0.13,
    "b": 0.1,
    "Kt": 580.0,
    "Ke": 0.001,
    "R": 2.3,
    "L": 0.1,
}
motor = DCmotor(param=parameters, timestep=h)

# Start main program
print "Starint main loop, press ^C to terminate and plot data"
continueMainLoop = True          # Flag to interrup main loop and plot
executionTime = 0.0
while continueMainLoop:
    try:
        startLoopTime = tt.time()

        # Get data from host
        recData = receiver.get_data()
        if recData is not None:
            # Decode data and store loop time
            reference = encode_hex_to_array(recData)
            loopTime = np.concatenate((loopTime, np.array([startLoopTime - startTime])))
            
            # Simulate response
            stateResponse = motor(reference)
            
            # Encode data
            hexString = encode_array_to_hex(stateResponse)

            # Send to the host
            sender.send_data(hexString)

        # Compute and store execution time
        executionTime = tt.time() - startLoopTime
        execTime = np.concatenate((execTime, np.array([executionTime])))

        if executionTime > 1.0/loopRate:
            print "Warning. The main loop deadline was not met at exec={}".format(executionTime)
        else:
            tt.sleep(1.0/loopRate - executionTime)
    except KeyboardInterrupt:
        continueMainLoop = False
        pass
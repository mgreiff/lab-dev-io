import sys
import os
import inspect
import numpy as np
from math import floor
import time as tt
import matplotlib.pylab as plt

curdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
pardir = os.path.dirname(os.path.dirname(curdir))
moddir = os.path.join(pardir, "modules")
sys.path.insert(0,moddir) 
from pythonBeagle import SenderThread, ReceiverThread, encode_hex_to_array, encode_array_to_hex

### Communication threads ###
senderAddress = ('127.0.0.1', 1724)
sender = SenderThread(address=senderAddress, protocol="UDP")
sender.start()

receiverAddress = ('127.0.0.1', 5004)
receiver = ReceiverThread(address=receiverAddress, protocol="UDP", size=3*16)
receiver.start()

### Reference signal computation ###
def pulse_reference(startTime):
    pulseWidth = 5.0          # [s]
    pulseAmplitude = 1.0      # [in this case voltage]
    pulseDutyCycle = 0.5      # [float in 0..1]
    currentTime = tt.time()   # Current time
    timeSinceStart = startTime - currentTime
    timeOfPulse = (timeSinceStart - pulseWidth*floor(timeSinceStart / pulseWidth)) / pulseWidth
    if timeOfPulse < pulseDutyCycle:
        return np.array([[0.0]])
    else:
        return np.array([[pulseAmplitude]])

### Main program ###
loopRate = 100.0                  # [Hz]
Nref = 1                         # Number of references
Nstate = 3                       # Number of states
references = np.zeros((Nref,1))  # References sent to the DC motor open loop
states = np.zeros((Nstate,1))    # State responses
loopTime = np.array([])          # Loop times
execTime = np.array([])          # Execution times
startTime = tt.time()            # Time at which the main loop starts

continueMainLoop = True          # Flag to interrup main loop and plot
numberOfLooptimingsMissed = 0
while continueMainLoop:
    try:
        startLoopTime = tt.time()
        loopTime = np.concatenate((loopTime, np.array([startLoopTime - startTime])))

        # Compute control signal (onedimensional vector)
        ref = pulse_reference(startTime)
        references = np.concatenate((references, ref), 1)
    
        # Encode and end data
        sender.send_data(encode_array_to_hex(ref))
        
        # Receive response
        data = receiver.get_data()
        if data != None:
            x = encode_hex_to_array(data)
        else:
            x = np.zeros((3,1))
        states = np.concatenate((states, x), 1)
        
        # Compute execution time
        executionTime = tt.time() - startLoopTime
        execTime = np.concatenate((execTime, np.array([executionTime])))

        if executionTime > 1.0/loopRate:
             #continueMainLoop = False
             numberOfLooptimingsMissed += 1
        else:
            tt.sleep(1.0/loopRate - executionTime)
    except KeyboardInterrupt:
        continueMainLoop = False
        pass

### Plot results ###
N = len(execTime)
loopTime = loopTime[0:N]
references = references[0,1:N+1]
angle = states[0,1:N+1]
speed = states[1,1:N+1]
current = states[2,1:N+1]
data = [references, execTime, angle, speed, current]
titles = ["References as a function of time",
          "Loop execution time as a function of time",
          "Motor angle as a function of time",
          "Motor speed as a function of time",
          "Motor current as a function of time"]
ylabels = ["Motor voltage [V]",
           "Loop execution time",
           "Motor angle [rad]",
           "Motor speed [rad/s]",
           "Motor current [A]"]
positions = [311, 323, 324, 325, 326]
for ii in range(len(data)):
    plt.subplot(positions[ii])
    plt.plot(loopTime, data[ii])
    plt.title(titles[ii])
    plt.ylabel(ylabels[ii])
    plt.xlabel("Time [s]")
    plt.axis([min(loopTime),
              max(loopTime),
              1.2*min(data[ii]),
              1.2*max(data[ii])])
plt.subplot(323)
plt.plot([min(loopTime), max(loopTime)], [1.0/loopRate, 1.0/loopRate], 'r')
plt.tight_layout()
plt.show()

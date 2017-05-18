import sys
import os
import inspect
import numpy as np
import matplotlib.pylab as plt

curdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
pardir = os.path.dirname(os.path.dirname(curdir))
moddir = os.path.join(pardir, "modules")
sys.path.insert(0,moddir) 
from pythonBeagle import DCmotor

loopRate = 100.0    # [Hz]
h = 1.0/loopRate
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

# Simulate a unit step
N = 200
t = np.zeros((1,N))
u = np.zeros((1,N))
x = np.zeros((3,N))
for ii in range(0,N):
    voltage = np.array([[1.0]])
    u[0,ii] = voltage[0,0]
    t[0,ii] = ii * h
    if ii == 0:
        x[:,ii] = x0[:,0]
    else:
        x[:,ii] = motor(voltage)[:,0]

plt.plot(t[0,:],x[0,:])
plt.plot(t[0,:],x[1,:])
plt.plot(t[0,:],1e3*x[2,:])
plt.show()

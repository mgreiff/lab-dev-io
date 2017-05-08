"""This module contains contains all required dependencies to
    run the Python project and serves three purposes. The first
    is to establish communication with the BBB via the TCP/IP
    protocol. The second is to simulate actuators in discrete time
    and the third is to allow actuator and sensory objects to
    manipulate and measure processes in real-time from the BBB."""

__license__ = "MIT"
__docformat__ = 'reStructuredText'

import socket as st
import numpy as np
import scipy.linalg as sl
import struct
import threading
import socket

class ServerThread(threading.Thread):
    """
    Create a server daemon which handles communication between receiver and
    sender clients implementing TCP/IP.
    
    :param cientReceiver: A client which is to receive data
    :param cientSender:   A client from which data is sent
    :param size: The buffer size
    :type cientReceiver: socket.socket()
    :type cientSender: socket.socket()
    :type size: int
    """
    def __init__(self, clientReceiver, clientSender, size=1024):
        threading.Thread.__init__(self)
        self.clientReceiver = clientReceiver
        self.clientSender = clientSender
        self.size = size
        self.daemon = True

    def run(self):
        """
        Main loop of the thread
        """
        while True:
            data = self.clientReceiver.recv(self.size)
            if data:
                self.clientSender.send(data)
            else:
                raise Exception('Client disconnected')

class SenderThread(threading.Thread):
    """
    Sender daemon which publishes data to a socket.
    
    :param address: An adress which needs to be specified in thent of UDP
    :param client: An client which needs to be specified in thent of TCP
    :param protocol: A string tag set to TCP or UDP
    :type address: (ip[str], port[int])
    :type client: socket.socket()
    :type protocol: string
    """
    def __init__(self, client=None, address=None, protocol="TCP"):
        threading.Thread.__init__(self)
        self.daemon = True
        self.enabled = True
        self.issetup = False
        self.protocol = protocol
        self.address = address
        
        if protocol == "UDP" and address is not None:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.issetup = True
        if protocol == "TCP" and client is not None:
            self.client = client
            self.issetup = True
        if not self.issetup:
            raise ValueError("The protocol %s is not supported" % protocol)

    def send_data(self, data):
        """
        Send data to the receiver
        
        :param protocol: A data valued string
        :type data: string
        """
        if self.protocol == "UDP":
            self.client.sendto(data, self.address)
        if self.protocol == "TCP":
            self.client.send(data)

    def run(self):
        """
        Main loop of the thread
        """
        while self.enabled:
            continue

    def terminate(self):
        """
        Kills the thread instantaneously
        """
        self.enabled = False    

class ReceiverThread(threading.Thread):
    """
    Receiver daemon which receives data on a socket.
    
    :param address: An adress which needs to be specified in thent of UDP
    :param client: An client which needs to be specified in thent of TCP
    :param protocol: A string tag set to TCP or UDP
    :type address: (ip[str], port[int])
    :type client: socket.socket()
    :type protocol: string
    :type size: int
    """
    def __init__(self, client=None, address=None, protocol="TCP", size=1024, verbose=False):
        threading.Thread.__init__(self)
        self.daemon = True
        self.enabled = True
        self.issetup = False
        self.size = size
        self.protocol = protocol
        self.data = None
        self.verbose=verbose
        if protocol == "UDP" and address is not None:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.client.bind(address)
            self.issetup = True
        if protocol == "TCP" and client is not None:
            self.client = client
            self.issetup = True
        if not self.issetup:
            raise ValueError("The protocol %s is not supported" % protocol)

    def run(self):
        """
        Main loop of the thread
        """
        while self.enabled:
            if self.protocol == "UDP":
                data = self.client.recvfrom(self.size)[0]
            if self.protocol == "TCP":
                data = self.client.recv(self.size)
            if data != "" or data:
                self.data = data
                if self.verbose:
                    print ("Receive data '{}' in the thread, may be accessed "+
                          "in the loop at self.data").format(data)

    def get_data(self):
        """
        Get data from the receiver, set to None if no data has been received
        
        :param protocol: A data valued string
        :type data: string
        """
        return self.data

    def terminate(self):
        """
        Kills the thread instantaneously
        """
        self.enabled = False

def encode_hex_to_array(string):
    """
    Data is received as N float 64 entries by the 745 standard, coded in
    a minimal hexadecimal representation and converted into a numpy array of
    length (N,1).
    
    :param string: A hexadecimal string with no separators
    :type string: string
    """
    # Read the first two bytes and find the number of elements
    l = len(string)
    n = 16
    if l%16 == 0:
        out=np.zeros((l/n,1))
        for ind in range(0, l/n):
            out[ind,0] = struct.unpack("<d",string[ind*n:(ind+1)*n].decode("hex"))[0]
        return out
    else:
        return None

def encode_array_to_hex(array):
    """
    Data is received as a numpy array with type dfloat64 in the the IEEE 745
    standardand and is encoded to a string with a minimal hexadecimal
    representation.

    :param array: Of shape (N,1) for some integer N>0
    :type array: numpy.array
    """
    return "".join([struct.pack('d',element).encode('hex') for element in array.T[0]])

class Actuator(object):
    """
    The actuator class provides an interface required to run
    any actuator, such as a DC or stepper motor.

    :param pins: A list of pins on which the motor is run
    :param isSimulating: A flag set to true if the actutator should be simulated
    :type pins: list
    :type isSimulating: bool
    """

    def __init__(self, pins=None, param=None, isSimulating=True):
        self.isSimulating = isSimulating
        self.supportRealtime = False
        if pins == None and param == None:
            self._warn("Neither simulation nor realtime operation is supported")

        # Check if the actuator can support operation in real-time mode
        self._assert_pins(pins)
        if pins != None:
            self.pins = pins
            self.supportRealtime = True
        else:
            self.supportRealtime = False

        # Check if the actuator can support operation in simulation mode
        self._assert_paramaters(param)
        if param != None:
            self.param = param
            self.x = self.param['x0']
            self.supportSimulate = True
        else:
            self.supportSimulate = False

    def _assert_paramaters(self, parameters):
        raise ValueError("Method has not been implemented")

    def _assert_pins(self, pins):
        raise ValueError("Method has not been implemented")

    def status(self):
        print (("\n~~~ %s ~~~\nReal time support: %s\nSimulation support: %s") % 
               (str(self), str(self.supportRealtime), str(self.supportSimulate)))

    def __call__(self, control):
        """
        Loads a trajectory for use in outer control and visualization
        """
        raise ValueError("Method has not been implemented")

    def __str__(self):
        return "Actuator object"

    def _warn(self, message):
        print message

    def discretize_dynamics(self, A, B, G, h):
        """
        Discretizes a continuous time LTI system \dot{x} = Ax + Bu + G using an
        exponential matrix formulation and zero-order hold
        
        :param A: System matrix shape (M,M)
        :param B: Control matrix shape (M,N)
        :param G: Constant matrix shape (M,1)
        :param h: Timestep in seconds
        :type A: numpy.array
        :type B: numpy.array
        :type G: numpy.array
        :type h: float
        """
        # Input dimension check
        if type(A) != np.ndarray or type(B) != np.ndarray or type(G) != np.ndarray:
            raise TypeError("The inputs must be of type numpy.ndarray")
        if A.shape[0] != B.shape[0] or A.shape[0] != G.shape[0] or G.shape[1] != 1:
            raise ValueError("Row dimensions do not match in the LTI system")
        
        nx = A.shape[1]
        nu = B.shape[1]
        E = np.zeros((nx+nu+1,nx+nu+1))
        E[0:nx,0:nx] = A
        E[0:nx,nx:nx+nu] = B
        E[0:nx,nx+nu:nx+nu+1] = G
        Ed = sl.expm(h*E)
        Ad = Ed[0:nx,0:nx]
        Bd = Ed[0:nx,nx:nx+nu]
        Gd = Ed[0:nx,nx+nu:nx+nu+1]
        print Ed
        return Ad, Bd, Gd

class DCmotor(Actuator):
    """
    The DC motor object enables simulation of and real-time interface to a 
    brushless DC motor
    """
    def __init__(self, pin=None, param=None, isSimulating=True, timestep=None):
        # Type check
        if type(pin) == list:
            pin = pin[0]
        elif type(pin) != str and pin != None: 
            raise ValueError("Invalide type %s of argument pin" % type(pin))
        if type(param) != dict and param != None:
            raise ValueError("Invalide type %s of argument param" % type(param))
        if type(isSimulating) != bool:
            raise ValueError("Invalide type %s of argument isSimulating" % type(isSimulating))
        if timestep == None and isSimulating:
            raise ValueError("The time step must be define to simulate the system")
        if pin == None:
            pins = None
        else:
            pins = [pin]
        # Initialize the actuator super class
        super(DCmotor, self).__init__(pins=pins, param=param, isSimulating=isSimulating)
        self.timestep = timestep

        # Define the discrete time dynamical system
        self.Ad, self.Bd, _ = self._get_dynamics()

    def _get_dynamics(self):
        # Form continuous time system
        J = 0.13
        b = 0.1
        Kt = 580.0
        Ke = 0.001
        R = 2.3
        L = 0.1
        A = np.array([[0.0, 1.0, 0.0],
                      [0.0, -b/J, Kt/J],
                      [0.0, -Ke/L, -R/L]])
        B = np.array([[0.0],
                      [0.0],
                      [1.0/L]])
        G = np.array([[0.0],
                      [0.0],
                      [0.0]])
        # Return discrete time system
        return self.discretize_dynamics(A, B, G, self.timestep)

    def __call__(self, u):
        self.x = self.Ad.dot(self.x) + self.Bd.dot(u)
        return self.x

    def __str__(self):
        return "DC motor object"

    def _assert_paramaters(self, parameters):
        if parameters != None:
            interface = {"x0":np.ndarray, "J":float, "b":float, "Ke":float, "Kt":float, "R":float, "L":float}
            for key in interface.keys():
                if not key in parameters.keys():
                    raise ValueError(("The parameter dictionary does not "+
                                      "contain the key %s" % key))
                if type(parameters[key]) != interface[key]:
                    raise ValueError((("The parameter entry %s must "+
                                       "convertable to a numeric scalar") % key))

    def _assert_pins(self, pins):
        options = ["P8_17", "P8_18", "P8_19", "P8_20"]
        if pins != None:
            for pin in pins:
                if not pin in options:
                    raise ValueError((("The pin %s does not support PWM and"+
                                       "cannot run the %s") % (pin, str(self))))
    
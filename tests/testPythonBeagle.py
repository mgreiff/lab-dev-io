"""This module contains contains all required dependencies to
    run the Python project and serves three purposes. The first
    is to establish communication with the BBB via the TCP/IP
    protocol. The second is to simulate actuators in discrete time
    and the third is to allow actuator and sensory objects to
    manipulate and measure processes in real-time from the BBB."""

__license__ = "MIT"
__docformat__ = 'reStructuredText'

import socket

class Server(object):
    """
    A server for IP communication which may be run on the BBB
    or the host computer.
    """
    def __init__(self, port, adress, protocol="UDP"):
        self.port = port
        self.adress = adress
        self.protocol = protocol
        self.connected
 
    def _setup_connection(self):
        """
        Register the port and returns true if succesful
        """
        try:
            print "Todo register port"
        except:
            return False
        return true

    def __call__(self, data):
        """
        Send data
        """
    def __str__(self):
        return "A Server object on port %s with address %s and %s, connection is %s"

class Client(object):
    
    def __init__(self, port, adress, protocol="UDP"):
        self.port = port
        self.adress = adress
        self.protocol = protocol
        self.connected
 
    def _setup(self):
        """
        Register the port and returns true if succesful
        """
        try:
            print "Todo register port"
        except:
            return False
        return True

    def __call__(self, data):
        """
        Send data
        """
    def __str__(self):
        return "A Server object on port %s with address %s and %s, connection is %s"

class Actuator(object):
    """
    The actuator class provides an interface required to run
    any actuator, such as a DC or stepper motor.
    """
    def __init__(self, pins=None, params=None, isSimulating=True):
        """
        :param pins: A list of pins on which the motor is run
        :param isSimulating: A flag set to true if the actutator should be simulated
        :type pins: list
        :type isSimulating: bool
        """
        self.isSimulating = isSimulating
        if pins == None and params == None:
            self._warn("Neither simulation nor realtime operation is supported")

        # Check if the actuator can support operation in real-time mode
        self.supportRealtime = False
        if pins != None:
            self.pins = pins
            self.supportRealtime = True
        else:
            self.supportRealtime = False

        # Check if the actuator can support operation in simulation mode
        if params != None:
            self.params = params
            if self._assert_paramaters():
                self.x = self.params['x0']
                self.supportSimulate = True
            else:
                raise ValueError("Parameter assertion failed")
        else:
            self.supportSimulate = False

    def _assert_paramaters():
        #raise ValueError("Method has not been implemented")
        print "AAAAA"
        return True

    def __call__(self, control):
        """
        Loads a trajectory for use in outer control and visualization
        """
        raise ValueError("Method has not been implemented")

    def __str__(self):
        return "Actuator object"

    def _warn(self, message):
        print message

class DCmotor(Actuator):
    """
    The DC motor object enables simulation of and real-time interface to a 
    brushless DC motor
    """
    def __init__(self, pin=None, param=None):
        if pin == None:
            # Check that the requested pin supports pulse width modulation
            options = ["P8_17", "P8_18", "P8_19", "P8_20"]
            if type(pin) == str:
                requestedPin = pin 
            elif type(pin) == list:
                requestedPin = pin[0]
            else:
                raise ValueError("Invalide type %s of attribute pin" % type(pin))
            if requestedPin in options:
                super(DCmotor, self).__init__(pins=[pin], isSimulating=False)
            else:
                raise ValueError("The pin %s does not support PWM")

        # Check consistency of the parameter dictionary and initialize
        super(DCmotor, self).__init__(pin=requestedPin,
                                      param=requestedParam,
                                      isSimulating=True)
            
    def __str__(self):
        if self.isSImulating:
            return "DC motor object in simulation mode"
        else:
            return "DC motor object in real-time mode running on %s" % (str(self.pins))

    def _assert_paramaters():
        print "BBBBB"
        return False
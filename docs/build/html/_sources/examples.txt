PythonBeagle examples
=====================
The examples (``*``) can be found in ``cd ~/examples/*``, and are meant to show how the module
may be implemented. See ``open ~/examples/*/README.md`` for notes on how to run the specific examples.

Encoding and decoding
---------------------
A problem when creating generic interfaces for the communication, especially
in Python, is to find a minimal and good way of representing data sent over
the IP network. As the host is presumably a 64 bit machine, running python
on both sides of the communication will result in issues, as the BBB
is a 32 bit machine and numpy's dfloat type is set depending on the machine
capabilities.

Hence, the numpy.array object is converted into a 16 sign hexadecimal
representation (64 bit) or 8 sign hexadecimal representation (32 bit) without
separators, sllowing conversion back to a numpy.array object, or any other
suitable structure in Julia, C or C++.

The example is accessible in ``*=communication_encode``.

Communication TCP/IP
--------------------
The TCP/IP communication is set up in two ways, first with UDP sockets where
packets fired at will, and the second with streaming TCP sockets linked
by a server. Both are implemented in the SenderThread and ReceiverThread daemons
which enable simple socket based communication, implemented in two separate
examples.

The examples are accessible in ``*={communication_UDP, communication_TCP}``

Operating a DC motor
--------------------
This example establishes UDP communication between a program running on the host
and a program run on the BB. Running at 30 Hz, voltage control signals are
sent from the main loop of the host to the BB where the DC motor Actuator object
simulates a physical response and sends data back to the host computer. By
setting the isSimulating flag of the DC motor to false, the object will instead
operate a PWM signal on a specified pin of the BB.

The examples are accessible in ``*=process_DC``

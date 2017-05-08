This example simply demonstrates how socketing may be accomplished
using daemons running in the background. The example is launch by
opening three terminals and running

python TCPServer.py
python TCPClientA.py
python TCPclientB.py

in the respective terminals. This starts three threads which
terminate safely when the program is exited, allowing messages to
be sent from a main loop in *A to the main loop in *B and vice versa.
The server thread is required to handle the connection of sockets
allowing for streaming of data.

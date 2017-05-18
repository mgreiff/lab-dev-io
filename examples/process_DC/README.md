This example demonstrates how a motor could concievably be controlled from the
host computer, and also shows the limitations of running a socket based UDP approach
in helping daemons. This is just a quick hack which shows some issues with the current
implementation, where a locking behaviour is seen. This will have to be fixed ASAP.

The example is run by opening two terminals, one on the host and anothort on the host
or the BBB, then run

python host_program.py

and

python beagle_program.py

in the two terminals respectively.

Project summary
===============

This page documents the current interfacing with the host computer running
either (i) ROS with Python/C++, (ii) a Julia client, (iii) a Matlab/Simulink
interface or finally (iv) and interface with Drake. All communication is done
via the TCP/IP protocol, and currently, the developments is being done with
the python module 'pythonBeagle.py' operating on both sides of the
communication.

Status
------
* The intended models have been implemented in Simulink
* Discrete time models have been implemented in and in 'pythonBeagle'
* Drivers for the DC and steppers motor have been implemented in 'pythonBeagle'
* Communication has been established between ROS and the BBB via TCP/UDP

Report
------
For an in-depth explanation in report form, see :download:`beagle-project.pdf <_latex/beagle-project.pdf>`.

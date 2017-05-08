.. beagle-project documentation master file, created by
   sphinx-quickstart on Sat Apr 29 12:39:15 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the beagle project's documentation!
==============================================

This page documents the current interfacing with the host computer running
either (i) ROS with Python/C++, (ii) a julia client, (iii) a Matlab/Simulink
interface or finally (iv) and interface with Drake. All communication is done
via the TCP/IP protocol, and currently, the developments is being done with
the python module 'pythonBeagle.py' operating on both sides of the
communication.

Requirements
------------
The requirements in terms of hardware are listed below in the materials section,
and the software requirements are here given in terms of the desired client/host
framework.

(i) Ubuntu 14.04 with a ROS Indigo installation, a BBB flashed with Ångström
    installed with Python 2.7+ and the Adafruit BBIO module.

Contents
--------

.. toctree::
   :glob:

   project
   pythonBeagle
   examples
   notes
   materials
   hardware

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

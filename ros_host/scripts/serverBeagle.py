#!/usr/bin/env python

from std_msgs.msg import String, Header
import rospy
import socket
from math import sqrt, pi, floor
from json import dumps, load
import time
import numpy as np
import matplotlib.pyplot as plt
import sys
import subprocess
import os
import signal

class BeagleServer(object):

    def __init__(self, options, ):
        """
        Sets up and handles communication with the beaglebone black.

        ARGS:
            options - A dictionary containing three boolean entries:
            UDP: Set to true if running real-time.
            Plot: Set to true to enable real-time analysis of communication.
            Optimal: Set to true to use optimal stepper planning.
        """
        self.options = options
        self.isConnected = False
        self.isReading = False
        
        # Valid unused adresses for receiving and sending data, adresses
        # may be added but never removed for backwards compatibility
        self.UDP_RECEIVE = ('192.168.7.1', 5005)
        self.UDP_SEND_REFERENCE_A = ('192.168.7.2',6)
        self.UDP_SEND_REFERENCE_B = ('192.168.7.2',8)
        self.UDP_SEND_CONTROL_A = ('192.168.7.2',14)
        self.UDP_SEND_CONTROL_B = ('192.168.7.2',16)

        self.reference_A_sub = rospy.Subscriber('reference_A', String, self.handle_ref_A)
        self.reference_B_sub = rospy.Subscriber('reference_B', String, self.handle_ref_B)
        self.control_A_sub = rospy.Subscriber('control_A', String, self.handle_ctr_A)
        self.control_B_sub = rospy.Subscriber('control_B', String, self.handle_ctr_B)
        
        self.connect_to_BBB()

    def connect_to_BBB(self):
        if self.options['UDP']:
            # Sets up the sockets for communicating with the beaglebone
            #command = "ssh 192.168.7.2 -l root"
            #subprocess.Popen(command, shell=True, env=os.environ)
            #sleep(3)
            try:
                self.sock_sender = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                self.sock_receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock_receiver.bind(self.UDP_RECEIVE)
                self.isConnected = True
                self.isReading = True
            except:
                print("Could not connect, make the BBB is plugged in and relaunch")
                pass
        else:
            print("Not connecting as the UDP flag is set to false")

    def handle_ref_A(self, msg):
        # TODO sanity check on data
        self.sendData(msg.data, self.UDP_SEND_REFERENCE_A)

    def handle_ref_B(self, msg):
        # TODO sanity check on data
        self.sendData(msg.data, self.UDP_SEND_REFERENCE_B)

    def handle_ctr_A(self, msg):
        # TODO sanity check on data
        self.sendData(msg.data, self.UDP_SEND_CONTROL_A)

    def handle_ctr_B(self, msg):
        # TODO sanity check on data
        self.sendData(msg.data, self.UDP_SEND_CONTROL_B)

    def handle_beagle_status(self, msg):
        """
        Callback for the beaglebone status subscriber. Returns a string with
        an exception message from the beagle bone. Currnelty only prints the
        message in the terminal.
        
        ARGS:
            msg - A std_msgs.msg message object.
        """
        print(msg.data)

    def sendData(self, data, address):
        # Send data to the BBB safely via sockets if the systemis to be run
        # in real-time. Callback driven, executing only when new data arrives
        if self.options['UDP'] and self.isConnected:
            print('sent data %s to %s' % (data, address))
            self.sock_sender.sendto(data, address)

    def getData(self):
        # An infinite loop which may temporarily disabled temporarily
        while not rospy.is_shutdown():
            h = Header()
            print h.frame_id
            h.stamp.secs = 10
            h.stamp.nsecs = 100
            print h
            if self.isConnected and self.isReading:
                try:
                    data, _ = self.sock_receiver.recvfrom(2048)
                    decode_line(data)
                except:
                    pass

def decode_line(data):
    # Decode the packet
    print("decode")
if __name__ == '__main__':
    options = {'UDP': True,'Plots': False,'Optimal': False}
    for arg in sys.argv:
        settings = arg.split(",")
        for setting in settings:
            if setting == 'Real':
                options['UDP'] = True
            elif setting == 'Plots':
                options['Plots'] = True
            elif setting == 'Optimal':
                options['Optimal'] = True
    rospy.init_node('beagleServer')
    server = BeagleServer(options)
    server.getData()

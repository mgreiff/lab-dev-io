#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import os
import sys
from json import dumps, load
import time

class Master(object):

    def __init__(self):
        # Sets up publishers and subscribers
        self.data_pub = rospy.Publisher('routine_data', String, queue_size = 10)
        self.LHR_status_sub = rospy.Subscriber('LHR_status', String, self.handle_status)
        self.dummy_status_sub = rospy.Subscriber('dummy_status', String, self.handle_status)
        self.status = True
        
    def initializeRobot(self, data):
        self.status = False
        self.data_pub.publish(data)

    def handle_status(self, msg):
        self.status = True

def main():
    rospy.init_node('master')
    master = Master()
    while not rospy.is_shutdown():
        try:
            cmd = raw_input('@master Interact: ')
            data = cmd.split(' ')
        except:
            pass

if __name__ == '__main__':
    main()

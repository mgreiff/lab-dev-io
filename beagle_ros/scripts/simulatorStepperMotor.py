#!/usr/bin/env python

from std_msgs.msg import String, Float64
import rospy
from math import pi
import time

class MotorZ(object):

    def __init__(self):
        self.routine_sub = rospy.Subscriber('LHR_z_routine', String, self.handle_routine_data)
	      self.position_pub = rospy.Publisher('LHR_z_pos', Float64, queue_size = 10)
	      self.status_pub = rospy.Publisher('LHR_motor_status', String, queue_size = 10)
	      self.position = 0
	      stepTimeBound = 0.01 #[s] lowest possible step time (bound on speed)
	      stepAngle = 0.9*2*pi/360 #[rad] (see motor spec.)
	      numberOfPullyTeeth = 18 #[/2pi rad] (see pully spec.)
	      numberOfBeltThreads = 962 # unitless (see belt spec.)
	      beltLength = 1955.8 #[mm] (see belt spec.)
	      distanceBetweenTeeth = float(numberOfBeltThreads)/beltLength #[mm]
	      self.distancePerStep = distanceBetweenTeeth*numberOfPullyTeeth*stepAngle #[mm]

    def handle_routine_data(self, msg):
        data = msg.data.split(' ')
	      print 'Starting motor Z...'
        badData = False
        for ii in range(len(data)):
            if not ii in [0,1]:
                try:
		                time.sleep(abs(float(data[ii])))
		                if float(data[ii]) < 0:
		                	  self.position -= self.distancePerStep
		                else:
			                self.position += self.distancePerStep
		                    self.position_pub.publish(float(self.position))
                except ValueError:
                    badData = True
        if badData:
            print 'WARNING. Encountered and ignored bad data in Motor X routine.'
        print '...motor Z complete!' 
        self.status_pub.publish('Z')

def main():
    rospy.init_node('MotorZ')
    mZ = MotorZ()
    rospy.spin()

if __name__ == '__main__':
    main()

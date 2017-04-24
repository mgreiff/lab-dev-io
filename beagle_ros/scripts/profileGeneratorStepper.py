#!/usr/bin/env python

from math import sqrt, pi, floor
import numpy as np

def generate1DStepperProfile(step, speed, accel, decel, stepAngle):
    """
    Generates a stepper profile for motion in optimal time, see the work of
    Austin, D., (http://fab.cba.mit.edu/classes/MIT/961.09/projects/i0/Stepper
    Motor_Speed_Profile.pdf) or the final surf report for more details on the
    mathematics involved. At the moment, accel == decel, but the distincition
    is made if some future application might need different bounds in different
    modes of operation (such as z-axis movement under the influence of gravity).

    ARGS:
        step: The number of steps which are to be taken
        speed: The angular velocity nound |omega(t)|<= speed for all t [rad/s]
        accel: The angular acceleration bound |\dot omega(t)|<= accel for all
            t [rad/s^2]
        decel: The angular deceleration bound |\dot omega(t)|<= accel for all
            t [rad/s^2]
        stepAngle: The angular increment of one step read from the motor spec.
            sheet (usually 200-400 degrees) [rad]
    """
    tt = 0.0001

    times = []
    speeds = []

    maxSAccelLim = int(floor(speed**2/(2*accel*stepAngle)))
    maxSDecelLim = step - int(floor(speed**2/(2*decel*stepAngle)))
    accelLim = int(floor(step*decel/(accel + decel)))
    decelLim = step - accelLim

    if maxSAccelLim < accelLim:
        # Accelerate to constant speed
        c = (1/tt)*sqrt((2*stepAngle)/accel) # Calculate sthe initial c
        dt = c*tt      
        times = [0, dt]
        speeds = [stepAngle/(dt)]
        for n in range(1, maxSAccelLim):
            newC = float(c)*(sqrt(n + 1) - sqrt(n))
            dt = newC*tt
            times = times + [times[len(times) - 1] + dt]
            speeds = speeds + [stepAngle/(dt)]

        # Keep constant speed
        for ii in range(maxSAccelLim, step - maxSAccelLim):
            dt = tt*float(c)*(sqrt(maxSAccelLim + 1 - 1) - sqrt(maxSAccelLim - 1))
            times = times + [times[len(times) - 1] + dt]
            speeds = speeds + [stepAngle/(dt)]

        # Decelerate from constant speed
        for ii in range(maxSDecelLim, step):
            c = (1/tt)*sqrt((2*stepAngle)/decel) 
            n = step - ii - 1
            newC = float(c)*(sqrt(n + 1) - sqrt(n))
            dt = tt*newC
            times = times + [times[len(times) - 1] + dt]
            speeds = speeds + [stepAngle/(dt)]
    else:
        # Accelerate to constant speed
        c = (1/tt)*sqrt((2*stepAngle)/accel) # Calculate sthe initial c
        dt = c*tt      
        times = [0, dt]
        speeds = [stepAngle/(dt)]
        for n in range(1, accelLim):
            newC = float(c)*(sqrt(n + 1) - sqrt(n))
            dt = newC*tt
            times = times + [times[len(times) - 1] + dt]
            speeds = speeds + [stepAngle/(dt)]

        # Decelerate from constant speed
        for ii in range(decelLim, step):
            c = (1/tt)*sqrt((2*stepAngle)/decel) 
            n = step - ii - 1
            newC = float(c)*(sqrt(n + 1) - sqrt(n))
            dt = tt*newC
            times = times + [times[len(times) - 1] + dt]
            speeds = speeds + [stepAngle/(dt)]

    return times, speeds

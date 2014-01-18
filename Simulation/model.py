 
from math import *
import random

import car
import track
import line_seg
import controller
import filters
import numpy

#TODO: merge the run programs
#TODO: smooth the input with an IIR filter and add the filter parameter to twiddle


def run_and_get_error_only(iterations, time, controller, mytrack, mycar, speed):

    sq_cte_sum = 0
    
    for i in range(iterations):

        #sensing
        line_sensed, CTE, abs_pt, true_cte = mycar.sense(mytrack)

        if not line_sensed:
            true_cte = mycar.sensor_width * 0.6667

        sq_cte_sum += true_cte**2

        #control
        steering = controller.run(CTE)

        # update the car's position
        mycar = mycar.move(steering, speed*time)

    return sq_cte_sum

def run(iterations, time, controller, mytrack, mycar, speed):
    
    pos_out = []
    sense_out = []

    filt = filters.single_pole_IIR(.1, 0.1)

    past_points = numpy.zeros([5,2])
    shift_down = numpy.matrix('[0 0 0 0 0, 1 0 0 0 0, 0 1 0 0 0, 0 0 1 0 0, 0 0 0 1 0, 0 0 0 0 1]')

    for i in range(iterations):

        #sensing
        line_sensed, CTE, abs_pt, true_cte = mycar.sense(mytrack)

        
        #past_points = shift_down * past_points

        #past_points[0,0] = abs_pt[0,0]
        #past_points[0,1] = abs_pt[0,1]


        if line_sensed:
            sense_out.append("%f, %f" % (abs_pt[0,0], abs_pt[0,1]))

        #control
        steering = controller.run(CTE)

        # update the car's position
        mycar = mycar.move(steering, speed*time)
        
        #output the position of the sensor (the front of the car
        pos = mycar.get_sensor_pos()
        pos_out.append("%f, %f, %f, %f, %f, %f" % (pos[0], pos[1], mycar.orientation, speed, steering, mycar.steering_angle))

    return (pos_out, sense_out) 

def build_default_car(time, speed):
    mycar = car.Car()
    mycar.set(0.0, 0.1, 0.0)
    mycar.set_steering_drift(0.0 / 180.0 * pi) 

    mycar.set_max_steering_delta(pi * 0.6 * time)
    #mycar.set_max_steering_delta(pi * 0.2 * time)

    mycar.set_noise(0.1 / 180.0 * pi, 0.005 * speed * time, 0.01 * mycar.sensor_width)
    
    return mycar



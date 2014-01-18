
from math import *
import random

import car
import track
import line_seg
import controller
import model
import twiddle


def run_for_plotting():

	# run params
	N = 200
	time = 0.02
	speed = 2.0 # motion distance is equal to speed (we assume time = 1)

	# the controller ( P, I, D, dt )
	#pid_controller = controller.PID_Controller(0.4, 0.001, 0.01, time)
	# why does this work so well? pid_controller = controller.PID_Controller(0.0, 0.0, 0.01, time)
	#pid_controller = controller.PID_Controller(0.2, 0.001, 0.01, time)
	pid_controller = controller.PID_Controller(0.5, 0.038, 0.0108, time)

	#build the track
	mytrack = track.get_track_1()
	line_seg_track = track.convert_to_line_segs(mytrack)
	track.write_to_file(mytrack, 'generated_files/track.csv')

	# create the car
	mycar = model.build_default_car(time, speed) 
	mycar.write_to_file('generated_files/car_data.csv')


	# Main program
	pos_out, sense_out  = model.run(N, time, pid_controller, line_seg_track, mycar, speed)

	f_Pos = open('generated_files/run_output.csv','w')
	for pos in pos_out:
			f_Pos.write("%s\n" % (pos))
	f_Pos.close()

	f_Sense = open('generated_files/sense_output.csv','w')
	for pos in sense_out:
			f_Sense.write("%s\n" % (pos))
	f_Sense.close()


class TwiddleHelper:
	
	def __init__(self, N, track, time, speed):
		self.N = N
		self.track = track
		self.time = time
		self.speed = speed

	def run(self, params):
		pid_controller = controller.PID_Controller(params[0], params[1], params[2], self.time)

		mycar = model.build_default_car(self.time, self.speed) 
	
		return model.run_and_get_error_only(self.N, self.time, pid_controller, self.track, mycar, self.speed)

def run_twiddle():
	# run params
	N = 200
	time = 0.02
	speed = 2.0 # motion distance is equal to speed (we assume time = 1)

	pid_params = [.2,.001,.01]
	step_sizes = [.01,.0005,.001]

	mytrack = track.get_track_1()
	line_seg_track = track.convert_to_line_segs(mytrack)

	TH = TwiddleHelper(N, line_seg_track, time, speed)
	
	twiddle.do_twiddle(TH, pid_params, step_sizes, .0001)
	


######################################
# Run the script
######################################

run_for_plotting()
# run_twiddle()




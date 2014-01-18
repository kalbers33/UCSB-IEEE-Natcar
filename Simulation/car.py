
from math import *
import random

import line_seg


# ------------------------------------------------
# 
# this is the car class
#

class Car:

	# --------
	# init: 
	#	creates car and initializes location/orientation to 0, 0, 0
	#

	def __init__(self, length = 0.2032, sensor_offset = 0.3175, sensor_width = 0.3556):
		self.x = 0.0
		self.y = 0.0
		self.orientation = 0.0
		self.length = length
		self.steering_noise = 0.0
		self.distance_noise = 0.0
		self.sensing_noise = 0.0
		self.steering_drift = 0.0
		self.sensor_offset = sensor_offset 
		self.sensor_width = sensor_width 
		self.last_cte = 0.0
		self.steering_angle = 0.0
		self.max_steering_delta = 2 * pi

	# --------
	# get_sensor_pos: 
	#	gets the positon of the car's sensor
	#

	def get_sensor_pos(self):

		return [self.x + self.sensor_offset*cos(self.orientation), self.y + self.sensor_offset*sin(self.orientation)]

	# --------
	# set: 
	#	sets a car coordinate
	#

	def set(self, new_x, new_y, new_orientation):

		self.x = float(new_x)
		self.y = float(new_y)
		self.orientation = float(new_orientation) % (2.0 * pi)


	# --------
	# set_noise: 
	#	sets the noise parameters
	#

	def set_noise(self, new_steer_noise, new_dist_noise, new_sense_noise):
		# makes it possible to change the noise parameters
		# this is often useful in particle filters
		self.steering_noise = float(new_steer_noise)
		self.distance_noise = float(new_dist_noise)
		self.sensing_noise = float(new_sense_noise)

	# --------
	# set_steering_drift: 
	#	sets the systematical steering drift parameter
	#

	def set_steering_drift(self, drift):
		self.steering_drift = drift

	# --------
	# set_max_steering_delta: 
	#	sets maximum change in steering angle that can occur in one time step
	#

	def set_max_steering_delta(self, delta_per_time):
		self.max_steering_delta = delta_per_time
		
	# --------
	# move: 
	#	steering = front wheel steering angle, limited by max_steering_angle. Defaults to 36 degrees (pi * 0.2)
	#	distance = total distance driven, must be non-negative

	def move(self, steering_cmd, distance, 
			 tolerance = 0.0001, max_steering_angle = pi * 0.2):

		# sanitzie the input
		if steering_cmd > max_steering_angle:
			steering_cmd = max_steering_angle
		if steering_cmd < -max_steering_angle:
			steering_cmd = -max_steering_angle
		if distance < 0.0:
			distance = 0.0


		# make a new copy
		res = Car()
		res.length		 = self.length
		res.steering_noise = self.steering_noise
		res.distance_noise = self.distance_noise
		res.sensing_noise = self.sensing_noise
		res.steering_drift = self.steering_drift
		res.sensor_offset = self.sensor_offset 
		res.sensor_width = self.sensor_width 
		res.last_cte = self.last_cte 
		res.steering_angle = self.steering_angle
		res.max_steering_delta = self.max_steering_delta


		steering = steering_cmd
		
		# apply steering drift
		steering += self.steering_drift

		# steering lag
		delta = steering_cmd - res.steering_angle
		abs_delta = abs(delta) 
		if (abs_delta > res.max_steering_delta):
			if (delta > 0):
				steering = res.steering_angle + res.max_steering_delta
			else:
				steering = res.steering_angle - res.max_steering_delta

		# apply noise
		steering2 = random.gauss(steering, self.steering_noise)
		distance2 = random.gauss(distance, self.distance_noise)


		# Execute motion
		turn = tan(steering2) * distance2 / res.length

		res.steering_angle = steering2

		if abs(turn) < tolerance:

			# approximate by straight line motion

			res.x = self.x + (distance2 * cos(self.orientation))
			res.y = self.y + (distance2 * sin(self.orientation))
			res.orientation = (self.orientation + turn) % (2.0 * pi)

		else:

			# approximate bicycle model for motion

			radius = distance2 / turn
			cx = self.x - (sin(self.orientation) * radius)
			cy = self.y + (cos(self.orientation) * radius)
			res.orientation = (self.orientation + turn) % (2.0 * pi)
			res.x = cx + (sin(res.orientation) * radius)
			res.y = cy - (cos(res.orientation) * radius)

		return res

	def get_sensor(self):
		sensor_mid = [self.x + self.sensor_offset*cos(self.orientation),
					  self.y + self.sensor_offset*sin(self.orientation)]
		sensor_left  = [sensor_mid[0] - self.sensor_width*sin(self.orientation),
					    sensor_mid[1] + self.sensor_width*cos(self.orientation)]

		sensor_right = [sensor_mid[0] + self.sensor_width*sin(self.orientation),
					    sensor_mid[1] - self.sensor_width*cos(self.orientation)]

		return line_seg.line_seg(sensor_left, sensor_right)

	def sense(self, track):

		#build the sensor line segment 
		sensor = self.get_sensor()

		hits = 0
		average = 0
		abs_pt = []
		true_cte = 0

		for seg in track:
			result = sensor.intersects(seg)
			if result[0] == True:
				hits += 1
				average += result[2]

		if hits != 0:
			cte = average / hits
			cte -= 0.5
			cte *= self.sensor_width * 2

			true_cte = cte

			# apply noise
			cte = random.gauss(cte, self.sensing_noise)

			#compute the absolute position of the sensed line
			scale = cte / (2 * self.sensor_width)
			scale += 0.5

			abs_pt = sensor.get_point(scale)

		else:
			cte = self.last_cte

		self.last_cte = cte
		line_sensed = (hits != 0)
		
		return (line_sensed, cte, abs_pt, true_cte)

	def write_to_file(self, filename):
		file_handle = open(filename, 'w')
		file_handle.write("%f, %f, %f\n" % (self.length, self.sensor_offset, self.sensor_width))
		file_handle.close()

	def __repr__(self):
		return '[x=%.5f y=%.5f orient=%.5f]'  % (self.x, self.y, self.orientation)



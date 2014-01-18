# ------------------------------------------------
# 
# this is a simple PID controller 
#

class PID_Controller:

	# --------
	# init: 
	#	Set the controller parameters
	#

	def __init__(self, p, i, d, dt = 1):
		self.p = p
		self.i = i
		self.d = d 
		self.last_error = 0
		self.cumulative_error = 0
		self.dt = dt # time between samples

	# --------
	# run: 
	#	run one iteration of the controller
	#

	def run(self, error, dt = 0):

		if dt <= 0:
			dt = self.dt

		diff_error = (error - self.last_error) / dt
		self.cumulative_error += error * dt
		
		last_error = error
		
		return -((self.p * error) + (self.i * self.cumulative_error) + (self.d * diff_error))






class single_pole_IIR:

	def __init__(self, pole, value = 0):
		self.pole = pole
		self.value = value


	def step(self, input_value):
		self.value = (self.pole * input_value) + ((1.0-self.pole) * self.value)
		return self.value


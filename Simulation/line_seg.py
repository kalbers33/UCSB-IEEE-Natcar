import math
import numpy


# --------
	# line: 
	#	A class that represents a line.
	#	Line is stored in the format A*x + B*y = 1

class line:
	
	def __init__(self, A = 0, B = 0):
		self.A = A
		self.B = B

	def best_fit(self, points):
		# A*x = y, y = [1]
		# x = A^-1*y


		pass
		
class line_seg:
	tolerance = 0.000001
	
	start = []
	end = []

	def __init__(self, start, end):
		
		self.start = numpy.matrix(start)
		self.end = numpy.matrix(end)


	# --------
	# intersects: 
	#	Determines if the line segments intersect and if they do, it returns the
	#		absolute positon of intersection and how far along itself the other line
	#		segment intersects. (0 = start, 1 = end)
	#

	def intersects(self, other):

		#print("debugging intersection") 

		#print("self; start:",self.start,", end:", self.end)
		#print("other; start:",other.start,", end:", other.end)

		p = self.start
		r = self.end - self.start

		q = other.start
		s = other.end - other.start

		#print("p =", p)
		#print("r =", r)
		#print("q =", q)
		#print("s =", s)
		
		# lines intersect at p +t*r = q + u*s

		denominator = numpy.cross(r,s)
		#print("den =", denominator)

		if numpy.abs(denominator) < self.tolerance: 
			#if (q - p).cross(r) < self.tolerance:
				# lines are colinear 
				#return (False, [])
			#else:
				# lines are parallel 
				#return (False, [])
			return (False, [], 0)

		t = ((numpy.cross(q-p,s))/denominator)[0]
		u = ((numpy.cross(q-p,r))/denominator)[0]

		#print("t =",t,", u=",u)

		if (((t >= 0 - self.tolerance) and (t <= 1 + self.tolerance)) 
		and ((u >= 0 - self.tolerance) and (u <= 1 + self.tolerance))):
			return (True, (p + t*r), t)
		else:
			return (False, [], 0)

	# --------
	# get_point: 
	#	Holds start constant and scales the line segment by the scale factor and
	#		returns the resulting end point
	#

	def get_point(self, scale_factor):
		p = self.start
		r = self.end - self.start
		return (p + scale_factor*r)

if __name__ == '__main__':

	start1 = numpy.matrix([1,2])
	end1 = [4,6]
	seg1 = line_seg(start1, end1)

	if not (seg1.start == start1).all():
		raise Exception("Fail")
	
	if not (seg1.end == end1).all():
		raise Exception("Fail")

	seg2 = line_seg([-2,-4], [-5,-10])

	if seg1.intersects(seg2)[0]:
		raise Exception("Fail")

	seg3 = line_seg([2,5], [3,1])

	if not seg1.intersects(seg3)[0]:
		raise Exception("Fail")

	print("victory!") 


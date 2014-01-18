import line_seg

def convert_to_line_segs(track):
	line_segs = []
	last_pt = track[-1].copy()
	for pt in track:
		line_segs.append(line_seg.line_seg(last_pt, pt))
		last_pt = pt
	return line_segs

def write_to_file(track, filename):
	if len(track) > 0:
		file_handle = open(filename,'w')
		for pos in track:
			file_handle.write("%f, %f\n" % (pos[0], pos[1]))
		# print first point again to complete track
		file_handle.write("%f, %f\n" % (track[0][0], track[0][1]))
		file_handle.close()


def get_box_track(size):
	track = []

	s = int(size)

	track.append([0,0])
	track.append([s,0])
	track.append([s,s])
	track.append([0,s])

	return track

def get_track_1():
	track = []

	track.append([0,0])
	track.append([5,0])
	track.append([20,10])
	track.append([30,20])
	track.append([35,30])
	track.append([35,35])
	track.append([25,40])
	track.append([20,45])
	track.append([15,45])
	track.append([5,37])
	track.append([0,40])
	track.append([-5,40])
	track.append([-10,35])
	track.append([-10,25])
	track.append([-10,15])
	track.append([-5,5])

	return track

def get_track_2010_official():
	track = []

	track.append([44,37])
	track.append([34,37])
	#arc center 34,34
	track.append([31.7917,36.125])
	track.append([3.875,8.125])

	return track

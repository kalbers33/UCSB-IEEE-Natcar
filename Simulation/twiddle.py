def calc_tolerence(params, step):
	total = 0
	for i in range(len(params)):
		total += abs(step[i] / params[i])
	return total

def do_twiddle(functor, initial_params, initial_step, tolerence):
	params = initial_params
	step_size = initial_step

	while calc_tolerence(params, step_size) > tolerence:
		
		base_error = functor.run(params)

		for i in range(len(params)):
			
			params[i] += step_size[i]

			new_error = functor.run(params)
			if base_error > new_error: 
				step_size[i] *= 1.1
				base_error = new_error
				continue

			params[i] -= 2 * step_size[i]
			
			new_error = functor.run(params)
			if base_error >  new_error:
				step_size[i] *= 1.1
				base_error = new_error
				continue
			
			# both changes made it worse.
			params[i] += step_size[i]
			step_size[i] *= .9
			
			# to keep it from getting stuck on a lucky run
			base_error = functor.run(params)

		print(params, new_error)



		

		
		 


	




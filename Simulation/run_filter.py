import filters

f = filters.single_pole_IIR(0.5)

for i in range(10):
	print(f.step(1))

import numpy as np
import matplotlib.pyplot as plt
import math

def makesin(time, freq, samplingFrequency):
	step = 1 / samplingFrequency
	npoints = int (time * samplingFrequency + 0.5)
	rads = [0 for i in range(npoints)]
	cords = [0 for i in range(npoints)]
	times = [0 for i in range(npoints)]
	for i in range(0, npoints, 1):
		rads[i] = freq * step * np.pi * i
		cords[i] = (int(128 * (math.sin(rads[i]) + 1)))
		times[i] = step * i
	plt.plot(times, cords)
	plt.title('Синусоида')
	plt.xlabel('Время')
	plt.ylabel('Значения напряжения')
	plt.show()
	return cords
makesin(10, 1, 100)
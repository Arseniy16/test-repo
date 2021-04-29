#Second script

import RPi.GPIO as GPIO
import time

num_bits = 8
comp = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(4, GPIO.IN)
GPIO.setup(comp, GPIO.IN)

D = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.output(17, 1)
GPIO.output(D[:], 0)

def decToBinList(decNumber):
    decNumber = decNumber % 256
    N = num_bits - 1
    bits = []
    while N > 0:
        if(int(decNumber/(2**N)) == 1):
            bits.append(1)
            decNumber -= 2**N
        else:
            bits.append(0)
        N -= 1
    bits.append(decNumber)
    return bits

def num2dac(value):
	bits = decToBinList(value)
	GPIO.output(D, bits)

def transfer(value):
	return (value * 3.3 / 255)

def sigdetection():
	for i in range(0, 2**num_bits):
		num2dac(i)
		time.sleep(0.001)
		if GPIO.input(comp) == 0:
			return i

try:
	while True:
		num = sigdetection()
		print("Digital value: ", num, ", Analog value: ", transfer(num))
except KeyboardInterrupt:
	print("\n############################################")
	print("# Программа была остановлена пользователем #")
	print("############################################\n")
	exit()
finally:
	GPIO.cleanup()
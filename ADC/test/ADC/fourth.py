#Fourth script

import RPi.GPIO as GPIO
import time

num_bits = 8

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

D = [26, 19, 13, 6, 5, 11, 9, 10]
LEDS = [24, 25, 8, 7, 12, 16, 20, 21]

GPIO.output(17, 1)
GPIO.output(D, 0)
GPIO.output(LEDS, 0)

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
	N = 7
	middle = 128
	while N > 0:
		num2dac(middle)
		time.sleep(0.001)
		if GPIO.input(4) == 0:
			middle -= 2**(N - 1)
		else:
			middle += 2**(N - 1)
		N -= 1
	if GPIO.input(4) == 0:
		middle -= 1
	else:
		middle += 1
	return middle

try:
	while True:
		num = sigdetection()
		print("Digital value: ", num)
		i = 0
		for j in range(0, int((num + 1)/30)):
			GPIO.output(LEDS[j], 1)
		time.sleep(0.005)
		GPIO.output(LEDS, 0)
except KeyboardInterrupt:
	print("\n############################################")
	print("# Программа была остановлена пользователем #")
	print("############################################\n")
	exit()
finally:
	GPIO.cleanup()
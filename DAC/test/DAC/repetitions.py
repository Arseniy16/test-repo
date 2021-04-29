#Second script

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

D = [10, 9, 11, 5, 6, 13, 19, 26]

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
    for i in range (0, num_bits):
        GPIO.output(D[i], bits[num_bits - (i + 1)])

def repetitions(num):
	for j in range(0, num, 1):
			for i in range(0, 256, 1):
				dac.num2dac(i)
				time.sleep(0.1)
			for i in range(256, 0, -1):
				dac.num2dac(i)
				time.sleep(0.1)
		time.sleep(0.1)

try:
	number = int(input("Введите число повторений: "))
	if(number < 0):
		print("Вы ввели некорректное число. Производится выход из программы")
		exit()
	repetitions(number)
except Exception:
	print("Вы ввели некорректный тип данных. Производится выход из программы")
except KeyboardInterrupt:
	print("\n############################################")
	print("# Программа была остановлена пользователем #")
	print("############################################\n")
finally:
	GPIO.cleanup()
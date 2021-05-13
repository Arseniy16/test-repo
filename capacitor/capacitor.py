

import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt

outstr = "Digital value: {digital}, analog value: {analog} V"

############################################
#----------CONST GLOBAL VARIABLES----------#
############################################
maxV = 3.3
num_bits = 8

comp = 4 #comparator
chan = 17
############################################
GPIO.cleanup()


#Initialization pins in RPi
dac_list = (26, 19, 13, 6, 5, 11, 9, 10)
led_list = (21, 20, 16, 12, 7, 8, 25, 24)
#led_list = (24, 25, 8, 7, 12, 16, 20, 21)

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac_list, GPIO.OUT)
GPIO.setup(led_list, GPIO.OUT)

GPIO.setup(chan, GPIO.OUT)
GPIO.setup(comp, GPIO.IN) 
 
#Converting decimal to binary
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
    GPIO.output(dac_list, tuple(bits))

def num2leds(value):
    bits = decToBinList(value)
    GPIO.output(led_list, tuple(bits))
'''
def bin_search():
    digit = 0
    i = 128
    while i >= 1:
        num2dac(int((digit + i) * 50 / 255))
        time.sleep(0.001)
        
        if GPIO.input(comp) == 1:
            digit += i

        i = int(i / 2)
    analog = maxV * digit / 255
    print(outstr.format(digital = digit, analog = analog))
    return digit
'''
'''
#binary search    
def adc():
    digit = 255
    i = 128
    while i >= 1:
        num2dac(digit-i)
        time.sleep(0.001)
        
        if GPIO.input(comp) == 0:
            digit -= i
        else: digit += i
        i = int(i / 2)
    return digit
'''

def adc():
	#num of bits - 1
	N = 7
	#middle amount between 0 and 256
	middle = 127
	#status of the comparatop
	#status = 1 -- value is higher
	#status = 0 -- value is lower
	while N > 0:
		num2pins(D,middle)
		t.sleep(0.001)
		if GPIO.input(4) == 0:
			middle -= 2**(N - 1)
		else:
			middle += 2**(N - 1)
		N -= 1
	if GPIO.input(4) == 0:
		middle -= 1
	else:
		middle += 1
	num2pins(LEDS,middle)
	return middle

listV = []
listT = []

#discharge
#while adc() > 0:
#   GPIO.output(chan, 0)
#    print('wait')
#    time.sleep(1)

t_start = time.time()

try:
    #GPIO.output(chan, 1)
    #digit = 0

    
    #charge
    GPIO.output(chan, 1)
    while True:
        listV.append(adc())
        listT.append(time.time() - t_start)
        time.sleep(0.0001)
        print(adc())
        if listV[-1] >= 211:
            break

    #discharge
    GPIO.output(chan, 0)
    while True:
        listV.append(adc())
        listT.append(time.time() - t_start)
        time.sleep(0.0001)
        print(adc())
        if listV[-1] <= 5:
            break

    for i in range(len(listV)): listV *= (3.29/210)
    plt.plot(listT, listV, 'r.')
    plt.show()
    print(len(listV)/10.0)
        
        #while(digit >= 1): digit = adc()

except KeyboardInterrupt:
    print("Stop program by user")
    GPIO.cleanup()

except Exception:
    print('Total Error...')
    GPIO.cleanup()

finally:
    print('Program is finished!')
    GPIO.cleanup()

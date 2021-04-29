###########################################
#----This is the fourth script for ADC----#
###########################################

import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import math
 
outstr = "Digital value: {digital}, analog value: {analog} V"

############################################
#----------CONST GLOBAL VARIABLES----------#
############################################
maxV = 3.3
num_bits = 8
comp = 4 #comparator
pot = 17
############################################
GPIO.cleanup()

#Initialization pins in RPi
out_list = (26, 19, 13, 6, 5, 11, 9, 10)
led_list = (24, 25, 8, 7, 12, 16, 20, 21)

GPIO.setmode(GPIO.BCM)
GPIO.setup(out_list, GPIO.OUT)
GPIO.setup(led_list, GPIO.OUT)
GPIO.setup(pot, GPIO.OUT)
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
 
def num2dac(value, list):
    bits = decToBinList(value)
    GPIO.output(list, tuple(bits))
 
def search():
    for digit in range(0, 256, 1):
        analog = maxV * digit / 255
        
        num2dac(int(j * 50 / 255))
        time.sleep(0.00001)

        if GPIO.input(comp) == 0:
            print(outstr.format(digital = digit, analog = analog))
            return digit

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


def shift():
    array = [0]
    for i in range(1, num_bits, 1):
        array.append((1 << int(int(i * 50 / 255) / 6)) - 1)
    return array

try:
    GPIO.output(pot, 1)
    while True:
        ndarray = shift();
        num2dac(ndarray[search()], led_list)

except KeyboardInterrupt:
    print("Stop program by user")
    GPIO.cleanup()

except:
     print('Total Error...')
    GPIO.cleanup()

finally:
    print('Program is finished!')
    GPIO.cleanup()

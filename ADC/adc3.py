###########################################
#-----This is the third script for ADC----#
###########################################

import RPi.GPIO as GPIO
import time

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

#Initialization pins in RPi to connect leds
GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
#-----------------------------------
GPIO.setup(pot, GPIO.OUT)
GPIO.setup(comp, GPIO.IN) 

#This array is for leds 
D = [10, 9, 11, 5, 6, 13, 19, 26]

#All leds are output
GPIO.output(D[:], 0)
 
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
    for i in range(0, num_bits):
        GPIO.output(D[i], bits[num_bits - (i + 1)])

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

try:
    GPIO.output(pot, 1)
    while True:
        bin_search()

except KeyboardInterrupt:
    print("Stop program by user")
    GPIO.cleanup()

except:
    print('Total Error...')
    GPIO.cleanup()

finally:
    print('Program is finished!')
    GPIO.cleanup()

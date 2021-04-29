############################################
#----This is the first script for ADC------#
############################################

import RPi.GPIO as GPIO
import time

############################################
#----------CONST GLOBAL VARIABLES----------#
############################################
num_bits = 8
maxV = 3.3
############################################

outstr = "{analog} = {voltage} V"

# Reset all firstly
GPIO.cleanup()

# Initialization pins in RPi to connect leds
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

# This array is for leds(DAC) 
D = [10, 9, 11, 5, 6, 13, 19, 26]

# All leds are output
GPIO.output(D[:], 0)

GPIO.output(17, 1)

# Converting decimal to binary
def num2dac(decNumber):
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

value = 0

try:
    while(value != -1):
        print('Enter number: ')
        value = int(input())
        number = float(value * maxV / 255)
        print(outstr.format(analog = value, voltage = number))

        bits = num2dac(value)
        for i in range(num_bits):
            GPIO.output(D[i], bits[num_bits - (i + 1)])                 
            
except KeyboardInterrupt:
    print("Stop program by user")
    GPIO.cleanup()

except ValueError:
    print('Total Error...')
    GPIO.cleanup()

finally:
    print('Program is finished!')
    GPIO.cleanup()
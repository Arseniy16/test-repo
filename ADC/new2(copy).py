###########################################
#----This is the second script for ADC----#
###########################################

import RPi.GPIO as GPIO
import time


outstr = "Digital value: {digital}, analog value: {analog} V"


maxV = 3.3

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

GPIO.setup(17, GPIO.OUT)

comp = 4 #comparator
pot = 17

GPIO.setup(comp, GPIO.IN) 

# This array is for leds(DAC) 
D = [10, 9, 11, 5, 6, 13, 19, 26]

# All leds are output
GPIO.output(D[:], 0)

GPIO.output(comp, 1)

#Converting decimal to binary
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

def search():
    for digit in range (0, 256, 1):
        analog = maxV * digit / 255
        
        bits = num2dac(int(j * 50 / 255))
        for i in range(num_bits):
            GPIO.output(D[i], bits[num_bits - (i + 1)])

        time.sleep (0.00001)
        if GPIO.input (comp) == 0:
            print(outstr.format(digital = digit, analog = analog))
            return digit

try:
    GPIO.output(pot, 1)
    while True:
        search()

except KeyboardInterrupt:
    print("Stop program by user")
    exit()

except:
    print('Total Error...')
    exit()

finally:
    print('Program is finished!')
    GPIO.cleanup()
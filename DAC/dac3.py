###############################################
#------This is the third script for DAC-------#
###############################################
import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt
import math
num_bits = 8

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

#This array is for leds(DAC) 
D = [10, 9, 11, 5, 6, 13, 19, 26]

#All leds are output
GPIO.output(D[:], 0)

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

#print('Write samplingFrequency: ')
samplingFrequency = 20000
#samplingFrequency = input()
#print('Write frequency: ')
frequency = 440
#frequency = input()

timer = np.arange(0, 20, 1/samplingFrequency)

amplitude = np.sin(timer*2*math.pi)

plt.plot(timer, amplitude)
plt.title('Sin')
plt.xlabel('time')
plt.ylabel('amplitude sin(time)')
plt.show()

value = 0

try:
    for value in timer:

        ampl = math.sin(value)*256

        if(ampl < 0): continue

        bits = num2dac(int(ampl))

        for i in range(num_bits):
            GPIO.output(D[i], bits[num_bits - (i + 1)])
        
        value += 1/samplingFrequency
        
        time.sleep(1/samplingFrequency)

except KeyboardInterrupt:
    print('Total Error...')
    GPIO.cleanup()

finally:
    print('Program is finished!')
    GPIO.cleanup()

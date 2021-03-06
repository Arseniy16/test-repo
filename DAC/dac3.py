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

#Output number in DAC
def num2dac(value):
    bits = decToBinList(value)
    for i in range (0, num_bits):
        GPIO.output(D[i], bits[num_bits - (i + 1)])

#plot the graphic of signal and create the waveform of signal 
def create_sin(timer, freq, samplingFrequency):
    step = 1 / samplingFrequency
    npoints = int (timer * samplingFrequency + 0.5)
    value = [0 for i in range(npoints)]
    cords = [0 for i in range(npoints)]
    times = [0 for i in range(npoints)]
    for i in range(0, npoints, 1):
        value[i]  = freq * step * 2 * np.pi * i
        cords[i] = (int(128 * (math.sin(value[i]) + 1)))
        times[i] = step * i
    plt.plot(times, cords)
    plt.title ('Sinus')
    plt.xlabel('Time, sec')
    plt.ylabel('Value of voltage')
    plt.show()
    return cords

try:
    timer = float(input('Enter the time: '))
    freq = float(input('Enter the frequency: '))
    samplingFrequency = int(input('Enter the samplingFrequency: '))
    samplingPeriod = 1 / samplingFrequency
    
    while(True):
        if freq <= 0 or timer <= 0 or samplingFrequency <= 0:
            print('Incorrect value. Try again')
        else break

    array = create_sin(timer, freq, samplingFrequency)
    for i in range(0, int(timer * samplingFrequency + 0.5), 1):
        num2dac(array[i])
        time.sleep(samplingPeriod)

except Exception:
    print('Total Error...')
    GPIO.cleanup()

except KeyboardInterrupt:
    print('Stop program by user')
    GPIO.cleanup()

finally:
    print('Program is finished!')
    GPIO.cleanup()


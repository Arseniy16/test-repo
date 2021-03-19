#------------------------------
#This program RPI_GPIO for leds 
#______________________________  

import RPi.GPIO as GPIO
import time

num_bits = 8

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

D = [24, 25, 8, 7, 12, 16, 20, 21]

GPIO.output(D[:], 0)

def lightUp(ledNumber, period):
    GPIO.output(D[ledNumber], 1)
    time.sleep(period)
    GPIO.output(D[ledNumber], 0)

def lightDown(ledNumber, period):
    GPIO.output(D[ledNumber], 0)
    time.sleep(period)
    GPIO.output(D[ledNumber], 1)

def blink(ledNumber, blinkCount, blinkPeriod):
    for i in range(0,blinkCount):
        GPIO.output(D[ledNumber], 1)
        time.sleep(blinkPeriod)
        GPIO.output(D[ledNumber], 0)
        time.sleep(blinkPeriod)        

def runningLight(count, period):
    for j in range(0, count):
        for i in range(0, num_bits):
            lightUp(i % num_bits, period)

def runningDark(count, period):
    GPIO.output(D[:], 1)
    for j in range(0, count):
        for i in range(0, num_bits):
            lightDown(i % num_bits, period)


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

def lightNumber(number):
    bits = decToBinList(number)
    for i in range (0, num_bits):
        GPIO.output(D[i], bits[num_bits - (i + 1)])

def runningPattern(pattern, direction):
    if(direction == -1):
        while True:
            lightNumber(pattern)
            pattern = (pattern << 1) % 255
            time.sleep(1)
    if(direction == 1):
        while True:
            lightNumber(pattern)
            if((pattern // 2)*2 != pattern):
                pattern += 2**num_bits
            pattern = pattern >> 1
            time.sleep(1)

def PWM(ledNumber, freq):            
    p = GPIO.PWM(D[ledNumber], frec)
    p.start(0)
    while True:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
    p.stop()

#runningPattern(15, -1)
#lightUp(3, 2)
#lightNumber(127)
#time.sleep(2)
#runningDark(2, 0.5)
#blink(3, 3, 1)
#runningLight(4, 0.5)


GPIO.cleanup()

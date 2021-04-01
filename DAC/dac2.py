#
#This is the second script for DAC
#
import RPi.GPIO as GPIO
import time

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

print('Write a number of repetitions')
repetitionsNumber = input()

try:
    for num in range(repetitionsNumber):
        for value in range(256):
            bits = num2dac(value)
            for i in range(num_bits):
                GPIO.output(D[i], bits[num_bits - (i + 1)])
            time.sleep(0.02)

        for value in range(255,-1, -1):
            bits = num2dac(value)
            for i in range(num_bits):
                GPIO.output(D[i], bits[num_bits - (i + 1)])
            time.sleep(0.02)

except Exception:
    print('Total Error...')
    GPIO.cleanup()

finally:
    print('Program is finished!')
    GPIO.cleanup()




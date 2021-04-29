#
#This is the second script for ADC
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

GPIO.setup(17, GPIO.OUT)

comp = 4 #comparator
pot = 17

GPIO.setup(comp, GPIO.IN) 

#This array is for leds(DAC) 
D = [10, 9, 11, 5, 6, 13, 19, 26]

#All leds are output
GPIO.output(D[:], 0)

# 
GPIO.output(pot, 1)

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

value = 0

try:    
    while True:
        for j in range(0, 255):
            time.sleep(0.00001)
            if(GPIO.input(comp) == 0): 

                analog = j / 255 * 3.3
                print('Digital value: ', j, 'Analog value: ', analog, ' V')
                
                bits = num2dac(int(j*50/255))
                for i in range(num_bits):
                    GPIO.output(D[i], bits[num_bits - (i + 1)])

                
                break    

            
except KeyboardInterrupt:
    print("Stop program by user")
    exit()
except ValueError:
    print('Total Error...')
    exit()
finally:
    print('Program is finished!')
    GPIO.cleanup()
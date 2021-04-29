###########################################
#-----This is the third script for ADC----#
###########################################

import RPi.GPIO as GPIO
import time

 
outstr = "Digital value: {digital}, analog value: {analog} V"
maxV = 3.3
try:
    out_list = (26, 19, 13, 6, 5, 11, 9, 10)
    in_ch = 4
    pot = 17
    GPIO.setmode (GPIO.BCM)
    GPIO.setup (out_list, GPIO.OUT)
    GPIO.setup (pot, GPIO.OUT)
    GPIO.setup (in_ch, GPIO.IN)
except:
    print ("GPIO Initialization error!")
    raise SystemExit
 
 
def decToBinList (decNumber):
    if decNumber < 0 or decNumber > 255:
        raise ValueError
    return [(decNumber & (1 << i)) >> i for i in range (7, -1, -1)]
 
def num2dac (value):
    x = decToBinList (value)
    GPIO.output (out_list, tuple (x))

 
def search ():
    for dg in range (0, 256, 1):
        an = maxV * dg / 255
        num2dac(int(dg * 50 / 255))
        time.sleep (0.001)
        if GPIO.input (in_ch) == 0:
            print(outstr.format(digital = dg, analog = an))
            return dg

def bin_search ():
    dg = 0
    i = 128
    while i >= 1:
        num2dac(int((dg + i) * 50 / 255))
        time.sleep (0.001)
        if GPIO.input (in_ch) == 1:
            dg += i
        i = int(i / 2)
    an = maxV * dg / 255
    print(outstr.format(digital = dg, analog = an))
    return dg

try:
    GPIO.output (pot, 1)
    while True:
        bin_search()
except:
     print('Total Error...')
     exit()
finally:
    GPIO.output (out_list, 0)
    GPIO.output (pot, 0)
    GPIO.cleanup (out_list)
    GPIO.cleanup (pot)
    GPIO.cleanup (in_ch)
    print('Program is finished!')
    

import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt
import math
 
outstr = "Digital value: {digital}, analog value: {analog} V"
maxV = 3.3
try:
    out_list = (26, 19, 13, 6, 5, 11, 9, 10)
    led_list = (24, 25, 8, 7, 12, 16, 20, 21)
    in_ch = 4
    pot = 17
    GPIO.setmode (GPIO.BCM)
    GPIO.setup (out_list, GPIO.OUT)
    GPIO.setup (led_list, GPIO.OUT)
    GPIO.setup (pot, GPIO.OUT)
    GPIO.setup (in_ch, GPIO.IN)
except:
    print ("GPIO Initialization error!")
    raise SystemExit
 
 
def decToBinList (decNumber):
    if decNumber < 0 or decNumber > 255:
        raise ValueError
    return [(decNumber & (1 << i)) >> i for i in range (7, -1, -1)]
 
def num2dac (value, clist):
    x = decToBinList (value)
    GPIO.output (clist, tuple (x))
 
def search ():
    dg = 0
    i = 128
    while i >= 1:
        num2dac(int((dg + i) * 50 / 255), out_list)
        time.sleep (0.001)
        if GPIO.input (in_ch) == 1:
            dg += i
        i = int(i / 2)
    an = maxV * dg / 255
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

array = [0]
for i in range (1, 256, 1):
    array.append ((1 << int(int (i * 50 / 255) / 6)) - 1)

try:
    GPIO.output (pot, 1)
    while True:
        num2dac(array[search()], led_list)
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
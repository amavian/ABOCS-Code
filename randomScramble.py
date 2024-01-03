'''
@author: amavian

This code is for scrambling the system to make it easier to test the code. 

This code is written for local feedback.

'''

#General Imports
import time
import random

#Device Imports
import piplates.DAQC2plate as DAQ
import RPi.GPIO as GPIO

#Stepper Motor Configuration
PUL1 = 17
DIR1 = 27
ENA1 = 22

PUL2 = 6
DIR2 = 13
ENA2 = 26

PUL3 = 4
DIR3 = 5
ENA3 = 12

PUL4 = 16
DIR4 = 20
ENA4 = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(PUL1, GPIO.OUT)
GPIO.setup(DIR1, GPIO.OUT)
GPIO.setup(ENA1, GPIO.OUT)

GPIO.setup(PUL2, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(ENA2, GPIO.OUT)

GPIO.setup(PUL3, GPIO.OUT)
GPIO.setup(DIR3, GPIO.OUT)
GPIO.setup(ENA3, GPIO.OUT)

GPIO.setup(PUL4, GPIO.OUT)
GPIO.setup(DIR4, GPIO.OUT)
GPIO.setup(ENA4, GPIO.OUT)

print('Initialization Completed')

delay = 0.001 #This changes the speed of the motors

#Functions
'''
getPower() takes the parameter, n, and returns the average of n photodetector measurements. I have found the n = 100 works well.
The function reads the data aquisition plate channel which converts the signal from analog to digital. At the end of the loop,
the function converts the voltage measurement to milliwats in optical power and rounds it to 4 decimal places.
'''
def getPower(n):
    power = 0
    for i in range(n):
        power+=DAQ.getADC(0,0) #(addr, channel) – returns voltage from single channel
    power/=n
    return round(((power-0.016)/1.02),4) #Calibration of the photodiode voltage to milliwats in optical power

'''
moveBy() takes parameters motor, duration, and direction and sends electrical signals to the driver to rotate the stepper motor 
appropriately. Changing the variable, delay, will change the speed of the motors.
'''
def moveBy(motor, duration, direction):
    
    if motor == 1:
        PUL = PUL1
        DIR = DIR1
        ENA = ENA1
    
    if motor == 2:
        PUL = PUL2
        DIR = DIR2
        ENA = ENA2
      
    if motor == 3:
        PUL = PUL3
        DIR = DIR3
        ENA = ENA3
        
    if motor == 4:
        PUL = PUL4
        DIR = DIR4
        ENA = ENA4
    
    GPIO.output(ENA, GPIO.HIGH)
    
    time.sleep(.1)
    
    if direction == 1:
        GPIO.output(DIR, GPIO.LOW)
        
    elif direction == -1:
        GPIO.output(DIR, GPIO.HIGH)
    
    else:
        print("ERROR: Direction Unknown")
        return
   
    for x in range(duration): 
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(delay)
    '''
    I have commented out the line below so that the motors will be locked in place at all times unless the motor is moving.
    '''
    #GPIO.output(ENA, GPIO.LOW)
    
    time.sleep(.1)
    return

'''
randomScramble() takes an upper bound parameter and scrambles the system so the optical power is below that upper bound 
power (or around that power). The function selects a random motor and a random step size. It runs a loop until its below
the upper bound.
'''
def randomScramble(upperBound):
    while True:
        motor = random.randint(1,4)
        stepSize = random.randint(-50,50)
        
        duration = stepSize
        direction = int(abs(duration)/duration)            
        moveBy(motor,abs(duration),direction)
        
        time.sleep(0.1) 
        if getPower(100) < upperBound: 
            moveBy(motor,abs(duration),-direction)
            break 
        time.sleep(0.5)		
    return getPower(100)
	
if __name__ == "__main__":

    try:
	    print(randomScramble(0.5))

    finally:
        GPIO.output(ENA1, GPIO.LOW)
        GPIO.output(ENA2, GPIO.LOW)
        GPIO.output(ENA3, GPIO.LOW)
        GPIO.output(ENA4, GPIO.LOW)
        GPIO.cleanup()
        print("Done")
	
	

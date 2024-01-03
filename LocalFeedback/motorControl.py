'''
@author: amavian

This code is for precise electronic alignment and is meant to be used before the automatic alignment to attain initial coupling using 
feedback from the photodetector (or ThorLabs powermeter by eye). This program allows you to type in commands (in the form "motor, stepSize") 
and it will make the corresponding adjustment. 

'''

#General Imports
import time

#Device Imports
import RPi.GPIO as GPIO
import piplates.DAQC2plate as DAQ

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

if __name__ == "__main__":
    
    # 1 and 3 = vertical
    # 2 amd 4 = horizontal
    
    try:
        print("Commands are entered in the form \"motor, stepSize\" and \"break\" is used to end the program.")
        while True:
            command = input("Enter Command: ")
            if command == "break":
                break
            motor = int(command.split(",")[0])
            duration = int(command.split(",")[1])
            direction = int(abs(duration)/duration)            
            moveBy(motor,abs(duration),direction)
            print(getPower(100))

    finally:
        GPIO.output(ENA1, GPIO.LOW)
        GPIO.output(ENA2, GPIO.LOW)
        GPIO.output(ENA3, GPIO.LOW)
        GPIO.output(ENA4, GPIO.LOW)
        GPIO.cleanup()
        print("Done")

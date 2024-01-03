'''
@author: amavian

This code is for fiber coupling using the motorized steering mirrors with remote feedback. 

It is nearly identical to fiberCoupler.py, except with the initial connection to the downstairs server and
the getPower() function acting as the request for power measurements.

The other functions are described in detail below.

All plotting code was removed.

'''

#General Imports
import time
import socket
import struct

#Device Imports
import RPi.GPIO as GPIO

#Client Code
host = '127.0.0.1' #Downstairs IP address
#host = '10.2.241.21' #Raspberry Pi IP address
port = 5560 #Arbitrarily high number chosen

#Server Functions
def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def getPower(n):
    s = setupSocket()
    message = 'POWER'
    s.send(str.encode(message))
    reply = s.recv(1024)
    power = struct.unpack('d', reply)[0]
    s.close()
    return power

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
I found that the power distribution across each degree of freedom (under ideal laboratory conditions) is approximately Gaussian.
Therefore, a simple hill climbing algorithm can be used to optimize any given degree of freedom.

findMax() takes  the parameter,  motor, and optimizes its position to maximize the coupling efficiency. It returns the final power 
measurement. The function begins with large step sizes and makes coarse adjustments mapping out the power distribution. When the 
function detects it is going in the wrong direction, it will turn around and decrease its step size, making finer adjustments until 
it converges on the maximum power. 

Unfortunately, the hardware issues resulted in the motors occasionally skipping steps. This effect, and hysteresis in the motors in 
general, were more pronounced at larger step sizes. To combat this, I implemented a "catch mechanism." The findMax() function maps
out the power distribution, finding the approximate maximum. It then goes back with a finer comb and stops when it gets within a 
certain margin of the recorded approximate maximum. In this way, we can assure that the program doesn't over shoot the maximum.
'''
def findMax(motor):
	
    n = 0
    k = 0
    i = 0
    j = -1
    
    stepList = [40,20,10,2,1]
    nStop = 2
    catchFactor = 1.05
    
    powerNew = getPower(100)
    powerMax = powerNew
	
    initialPower = powerNew
    	
    while True:
        d = stepList[i]
		
        if i == 2:
            nStop = 3
		
        else:
            nStop = 2
		
        powerOld = powerNew
        moveBy(motor, d, j)
		
        time.sleep(0.05)
        powerNew = getPower(100)
		
        if powerNew < powerOld:
            n+=1

        else:
            n=0

        if powerNew > powerMax:
            powerMax = powerNew

        print("Power Old: {:.3f}, Power New: {:.3f}, Power Max: {:.3f}".format(powerOld, powerNew, powerMax))
        print(n,k,d,j)

    	#Change direction?
        if n == nStop:
			
            j*=-1
            n=0
            k+=1
			
            if i == 0 and (powerMax == initialPower):
                continue
            else:
                i+=1
                
		#Catch mechanism
        if i == 2 and powerNew*catchFactor > powerMax:
            j*=-1
            n=0
            k+=1
            i+=1	
            
		#Stopping condition
        if i == 5:
            break
        
    return getPower(100)

''' 
singleMotorOptimization() takes the parameter, fundamental, and runs the findMax() function on all four motors. It prints some
helpful metrics and returns the final efficiency.
'''
def singleMotorOptimization(fundamental):
	tick = time.time()
	
	print("Servo 1:")
	findMax(1)
	print("Servo 2:")
	findMax(2)
	print("Servo 3:")
	findMax(3)
	print("Servo 4:")
	findMax(4)
	
	tock = time.time()
	power = getPower(100)
	efficiency = power/fundamental * 100
	
	print("Power: {:.3f} milliwatts".format(power))
	print("Time: {:.1f} seconds".format(tock-tick))
	print("Efficiency: {:.0f}%".format(efficiency), end = "\n\n")
		
	return efficiency

'''
walkBeam() takes the parameter, motors, and mimics the process of "walking the beam" through an iterative method of perturbations 
and compensation. The parameter, motors, is a list of either the two horizontal or two vertical degrees of freedom. The function
works by detuning one mirror and running the findMax() function on the other mirror. If the resulting power is greater, it continues
in that direction. If it is less, it changes direction. Over time the step sizes get smaller and the system converges on the global maximum.
'''
def walkBeam(motors):
	s1 = motors[0]
	s2 = motors[1]
	
	j = 1
	n = 0
	i = 0
	
	stepList = [120,80,40,20,10]
	
	newPower = getPower(100)
	
	while True:
		d = stepList[i]
		oldPower = newPower
		moveBy(s1,d,j) #Detune
		newPower = findMax(s2) #Climb hill
				
		if newPower < oldPower: #Change direction?
			j*=-1
			
			if n != 0 and n < 4:
				i+=1
			
			n+=1
			
		if n == 5:
			break
			
	return getPower(100)
	
'''
continuousOptimization() currently takes the parameter, n, and attempts to stabilize the power over n iterations. However, the idea 
is for it to run indefinitely once perfected. This function is fairly rudimentary. It works by rotating through each motor and makes
adjustments looking for improvements in power. If it detects a "significant" drop in power, then it will run the findMax() functions
to return to high coupling.
'''
def continuousOptimization(n):
    motors = [1,2,3,4]
    m = 0
    dropCatch = 1.1
	
    for i in range(n):
        motor = motors[m]
        n = 0
        j = -1
        d = 1
        k = 0
        
        nStop = 2
        powerNew = getPower(100)
		
        while True:
            powerOld = powerNew
            moveBy(motor, d, j)
            time.sleep(0.05)
            powerNew = getPower(100)
			
            if powerNew < powerOld:
                n+=1
                
                if powerNew * dropCatch < powerOld:
                    findMax(1)
                    findMax(2)
            else:
                n=0
		
            print("Power Old: {:.3f}, Power New: {:.3f}".format(powerOld, powerNew))
			
			#Change direction?
            if n == nStop:
                k+=1
                j*=-1
                n=0
                
			#Stopping condition
            if k == 2:
                break
				
        m+=1
        
        if m ==4:
            m = 0

if __name__ == "__main__":
    
    # 1 and 3 = vertical
    # 2 amd 4 = horizontal
    
    try:
	    fundamental = 16 #Measure incoming beam power and assign value here
	    
	    #Greedy Algorithm (with catch mechanism)
	    print("Commence Single Motor Optimization")
	    singleMotorOptimization(fundamental)
        
	    '''
	    #Finer Gradient Descent
	    print("Initate Beam Walking")
	
	    vert = [3,1]
	    horiz = [4,2]
	
	    tick = time.time()
	    power1 = walkBeam(vert)
	    tock = time.time()
	    eff1 = power1/fundamental * 100
	
	    print("Power: {:.3f} milliwatts".format(power1))
	    print("Time: {:.1f} seconds".format(tock-tick))
	    print("Efficiency: {:.0f}%".format(eff1, end = "\n\n"))
	    
	    tick = time.time()
	    power2 = walkBeam(horiz)
	    tock = time.time()
	    eff2 = power2/fundamental * 100
	    
	    print("Power: {:.3f} milliwatts".format(power2))
	    print("Time: {:.1f} seconds".format(tock-tick))
	    print("Efficiency: {:.0f}%".format(eff2, end = "\n\n"))
	    '''
        
        #continuousOptimization(20)
        
    finally:
        GPIO.output(ENA1, GPIO.LOW)
        GPIO.output(ENA2, GPIO.LOW)
        GPIO.output(ENA3, GPIO.LOW)
        GPIO.output(ENA4, GPIO.LOW)
        GPIO.cleanup()
        print("Done")

'''
@author: amavian

This code can be run to easily test the local photodetector power.

'''

#General Imports
import numpy as np

#Device Imports
import piplates.DAQC2plate as DAQ

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

if __name__ == "__main__":
    
    #Test photodetector
    powers = []

    for i in range(100):
        p = getPower(100)
        powers.append(p)
        print(p)

    print("Average:", np.average(powers))
    print("STDV:", np.std(powers))

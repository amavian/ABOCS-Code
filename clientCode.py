'''
@author: amavian

This code is for the upstairs Raspberry Pi to connect to the downstairs Raspberry Pi and test the power retrieval. 
It works by connecting to the downstairs server using the socket module. To request a power measurement, it sends a message, "POWER", 
and waits for the reply. Strings are encoded/decoded with 'utf-8' and doubles are encode/decoded using the struct module.

'''

#Import Packages
import socket
import time
import struct
import numpy as np

host = '127.0.0.1' #Downstairs IP address
#host = '10.2.241.21' #Raspberry Pi IP address

port = 5560 #Arbitrarily high number chosen

#Server Functions
def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def receivePower():
    s = setupSocket()
    message = 'POWER'
    s.send(str.encode(message))
    reply = s.recv(1024)
    power = struct.unpack('d', reply)[0]
    s.close()
    return power

#Below is a test of power retrieval
L = []
tick = time.time()

for i in range(100):
    p = receivePower()
    L.append(p)
    print("{:.4f}".format(p))
 
tock = time.time()

print("Time: ", tock-tick)
print("Average: ", np.average(L))
print("STDV: ", np.std(L))

'''
@author: amavian

This code is for the downstairs Raspberry Pi that provides the feedback power measurements from the remote location.
It works by setting up a server using the socket module. It listens and waits for a client to connect. Once a client is connected,
the server begins a data transfer loop. If the client sends the command, "POWER", the server will reply with the power measurement.
Strings are encoded/decoded with 'utf-8' and doubles are encode/decoded using the struct module.

'''

#Import Packages
import socket
import struct
import piplates.DAQC2plate as DAQ

#Data Aquisition Function
def getPower(n):
    power = 0
    for i in range(n):
        power+=DAQ.getADC(0,0)
    return round((power-0.01)/2.45/n, 4) #Calibration of the photodiode voltage to miliwatts in optical power

host = '' #Not needed for server
port = 5560 #Arbitrarily high number chosen

#Server Functions
def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    return s

def setupConnection():
    s.listen(1) # Allows one connection at a time.
    conn, address = s.accept()
    #print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn

def dataTransfer(conn):
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        command = conn.recv(1024) # receive the request
        command = command.decode('utf-8')
        if command == 'POWER':
            reply = getPower(100)
        else:
            break
        # Send the reply back to the client
        conn.sendall(struct.pack('d', reply))

    conn.close()

#Start Server
s = setupServer()

while True:
    try:
        conn = setupConnection()
        dataTransfer(conn)
    except:
        break

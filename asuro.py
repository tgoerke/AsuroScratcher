# AsuroScratcher
# Connects Scratch to Asuro; use control-C to quit

from array import array
import socket
import time

import sys, os, serial, threading



HOST = '127.0.0.1'
PORT = 42001

# First parameter corresponds to COM port number minus 1
# if the Asuro USB IR Transceiver is connected to COM8 set 7 here
ser = serial.Serial(4, 2400)

print("connecting...")
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("connected! waiting for data...")

# print incoming data forever
while 1:
    #time.sleep(0.01)
    data = scratchSock.recv(1024)
    if data:
		cmd=data.replace(' ', '').replace('"', '').partition("Asuro-")[2]
		print(cmd)
		ser.write(cmd) 
	
	
	
	
	
	
	

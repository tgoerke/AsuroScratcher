# Scratch client test program
# sends 10 "beat" broadcasts to Scratch

from array import array
import socket
import time

HOST = '127.0.0.1'
PORT = 42001

def sendScratchCommand(cmd):
    n = len(cmd)
    a = array('c')
    a.append(chr((n >> 24) & 0xFF))
    a.append(chr((n >> 16) & 0xFF))
    a.append(chr((n >>  8) & 0xFF))
    a.append(chr(n & 0xFF))
    scratchSock.send(a.tostring() + cmd)
    print a.tostring() 

print("connecting...")
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("connected")

for i in xrange(10):
    sendScratchCommand('sensor-update note ' + str(60 + (2 * i)) + ' beats 0.4')
    sendScratchCommand('broadcast "beat"')
    print("beat!")
    time.sleep(0.5)

print("closing socket...")
scratchSock.close()
print("done")

# Scratch client test program
# Demonstrates the Scratch Network Connection Functionality
# http://scratch.mit.edu/forums/viewtopic.php?id=43522


from array import array
import socket
import time

HOST = '127.0.0.1'      # IP address of the remote host (in this case, the local machine)
                              # to connect to Scratch on a different computer, just put in its IP address
PORT = 42001            # The same port as used by the server

# sendScratchCommand(cmd)
# this function packages a message according the Scratch Networking Protocol
# and then sends it off
def sendScratchCommand(cmd):
        n = len(cmd)
        a = array('c')
        a.append(chr((n >> 24) & 0xFF))
        a.append(chr((n >> 16) & 0xFF))
        a.append(chr((n >>  8) & 0xFF))
        a.append(chr(n & 0xFF))
        scratchSock.send(a.tostring() + cmd)

# Make a connection to Scratch
print("connecting...")
scratchSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
scratchSock.connect((HOST, PORT))
print("connected!")
# Emulate the green flag being clicked (optional)
sendScratchCommand('broadcast "scratch-startclicked"')
print("manually starting up Scratch")

# Display broadcasts and global var changes
while 1:
        data = scratchSock.recv(1024)
        if not data: break
        print(data)

scratchSock.close()
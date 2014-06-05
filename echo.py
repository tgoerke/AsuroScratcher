#!/usr/bin/env python

"""
An echo server that uses threads to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys
import threading
from array import array
import time
import re


# Parse Data Definitions
def parseData(str):
    #Check for a broadcast
    e = re.search('broadcast\s\"(.*)\"',str)
    if e:
        #We have a broadcast!
        return 'parsed = broadcastIn("'+e.group(1)+'")'
    #Check for a sensor-update with quoted second value (string)
    e = re.search('sensor-update\s\"(.*?)\"\s\"(.*?)\"',str)
    if e:
        #Got one!
        return 'parsed = sensorUpdateIn("'+e.group(1)+'","'+e.group(2)+'")'
    #Look for a sensor-update with a numeric second value
    e = re.search('sensor-update\s\"(.*?)\"\s([-|\d|.]+)',str)
    if e:
        #Success!
        return 'parsed = sensorUpdateIn("'+e.group(1)+'","'+e.group(2)+'")'

def sensorUpdateIn(var,value):
    #print "Scratch changed "+var+" to: "+value
    return 'sensor-update '+value
    
    
def broadcastIn(broadcast):
    #print "Scratch broadcasted: "+broadcast
    return 'broadcast '+broadcast
# End

class Server:
    def __init__(self):
        self.host = ''
        self.port = 42002
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def run(self):
        self.open_socket()
        input = [self.server,sys.stdin]
        running = 1
        while running:
            inputready,outputready,exceptready = select.select(input,[],[])

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads

        self.server.close()
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        lcs.append([0,0])
        #print lcs
        self.ids = len(lcs)-1
        #print self.ids

    def run(self):
        #print self.address,'has connected.'
        running = 1
        while running:
            data = self.client.recv(self.size)
            if data:
                exec parseData(data)
                if parsed == 'broadcast start': # Start/Setup
                    exe = '''sendScratchCommand('sensor-update "x" "'''+str(lcs[self.ids][0])+'''"')
sendScratchCommand('sensor-update "y" "'''+str(lcs[self.ids][1])+'''"')
'''
                # Movement Start
                elif parsed == 'broadcast up': # Move Up
                    lcs[self.ids][1] += 1
                    #print lcs
                    exe = '''sendScratchCommand('sensor-update "y" "'''+str(lcs[self.ids][1])+'''"')'''
                elif parsed == 'broadcast down': # Move Down
                    lcs[self.ids][1] -= 1
                    #print lcs
                    exe = '''sendScratchCommand('sensor-update "y" "'''+str(lcs[self.ids][1])+'''"')'''
                elif parsed == 'broadcast left': # Move Left
                    lcs[self.ids][0] -= 1
                    #print lcs
                    exe = '''sendScratchCommand('sensor-update "x" "'''+str(lcs[self.ids][0])+'''"')'''
                elif parsed == 'broadcast right': # Move Right
                    lcs[self.ids][0] += 1
                    #print lcs
                    exe = '''sendScratchCommand('sensor-update "x" "'''+str(lcs[self.ids][0])+'''"')'''
                # Movement End

                else: # Unknown Command
                    exe = 'print "Error, no such command."'
                self.client.send(exe)
            else:
                self.client.close()
                running = 0

if __name__ == "__main__":
    lcs = []
    s = Server()
    s.run()

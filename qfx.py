#!c:\Python31\python.exe
import sys, os, serial, threading

ser = serial.Serial(4, 2400)
print ser.portstr  
ser.write(" qflfrflx") 
ser.close()

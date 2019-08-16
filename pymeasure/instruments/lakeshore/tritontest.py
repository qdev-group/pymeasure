"""
This driver is used to controll and measure the temperature via the Lakeshore 370 using the Triton controll software
"""
import time
import socket
import numpy as np

class TritonLakeshore():
    
    """ Allows user to control Lakeshore370 via the Triton control software"""
    
    def connect(self):
        edsIP = "localhost"
        edsPORT = 33576
        MESSAGE = b'SET:DEV:UID:TEMP:MEAS:ENAB:\r\n'
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.settimeout(20) # 3 second timeout on commands
        self.srvsock.connect((edsIP, edsPORT))
        
    def initalize_measure_T8(self):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:MODE:ON\r\n')
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:MEAS:ENAB:ON\r\n')
        data = self.srvsock.recv(4096)
        return(data)
        
    def get_temp_T8(self):
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
        data = self.srvsock.recv(4096)
        return (data)
    
    def get_temp_T8_test(self):
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
        
    def get_temp_T5(self):
        self.srvsock.sendall(b'READ:DEV:T5:TEMP:SIG:TEMP\r\n')
        data = self.srvsock.recv(4096)
        return (data)

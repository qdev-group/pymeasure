import time
import socket
import numpy as np

class Oxford():
    
    """ Allows user to control Magnet power supply via the Triton control software"""
    
    def connect(self):
        edsIP = "localhost"
        edsPORT = 33576
        MESSAGE = b'SET:DEV:UID:VRM:MEAS:ENAB:\r\n'
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.settimeout(20) # 3 second timeout on commands
        self.srvsock.connect((edsIP, edsPORT))
        
    def get_Bfield(self): #This will get the magnetic field in xyz coordinates, will output float of z magnetic field#
        self.srvsock.sendall(b'READ:SYS:VRM:VECT\r\n')
        data = self.srvsock.recv(4096)
        #data = float(data[35:-3])
        return (data)
        
    def get_temp_T8(self): #This will get the temperature reading from the RuO thermometer, for use below 1.2K#
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
        data = self.srvsock.recv(4096)
        data = float(data[26:-2])
        return (data)

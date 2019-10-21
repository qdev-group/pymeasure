"""
This file is used to control the magnet power supply through the triton software

Note that there are no safety interlocks. Make sure you know what you are doing and the fridge is in a safe place to turn 
the magnet on.

TODO add errors and safety 
    check if it automatically matches current when persistent mode is turned off. Does is automatically wind down the current if persistent mode is on. 

"""

import time
import socket
import numpy as np

class Mercuryips():
    
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
        data = float(data[35:-3])
        return (data)
    
    def get_swprate(self): #This will get the sweep rate#
        self.srvsock.sendall(b'READ:SYS:VRM:RFST\r\n')
        data = self.srvsock.recv(4096)
        return (data)
    
    def get_current(self): #This returns the instanteous current in vrm#
        self.srvsock.sendall(b'READ:SYS:VRM:MCUR\r\n')
        data = self.srvsock.recv(4096)
        return (data)
    
    def set_poc_on(self): #Turns persistent on completion on
        self.srvsock.sendall(b'SET:SYS:VRM:POC:ON\r\n')
        data = self.srvsock.recv(4096)
        
    def set_poc_off(self): #Turns persistent on completion mode off
        self.srvsock.sendall(b'SET:SYS:VRM:POC:OFF\r\n')
        data = self.srvsock.recv(4096)
        
    def set_swpto_asap(self,bf): #sets sweep rate to asap#
        self.srvsock.sendall(b'SET:SYS:VRM:RVST:MODE:ASAP:VSET[0 0 %a]\r\n' % bf )
        data = self.srvsock.recv(4096)
        
    def set_swprate_rate(self,rate,bf):
        self.srvsock.sendall(b'SET:SYS:VRM:RVST:MODE:RATE:RATE:%a:VSET[0 0 %a]\r\n' % rate, bf )
        data = self.srvsock.recv(4096)
        
    def set_swprate_time(self,time,bf):
        self.srvsock.sendall(b'SET:SYS:VRM:RVST:MODE:TIME:TIME:%a:VSET[0 0 %a]\r\n' % time, bf )
        data = self.srvsock.recv(4096)
        
    def set_bfield(self,bf):
        self.srvsock.sendall(b'SET:SYS:VRM:VSET:[0 0 %a]\r\n' % bf)
        data = self.srvsock.recv(4096)
        
    def goto_set(self):
        self.srvsock.sendall(b'SET:SYS:VRM:ACTN:RTOS\r\n')
        data = self.srvsock.recv(4096)
        
    def goto_zero(self):
        self.srvsock.sendall(b'SET:SYS:VRM:ACTN:RTOZ\r\n')
        data = self.srvsock.recv(4096)

    def set_persistent_on(self):
        self.srvsock.sendall(b'SET:SYS:ACTN:PERS\r\n')
        data = self.srvsock.recv(4096)
       
    def set_persistent_off(self):
        self.srvsock.sendall(b'SET:SYS:ACTN:NPERS\r\n')

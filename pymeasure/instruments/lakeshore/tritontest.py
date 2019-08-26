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
        data2 = self.srvsock.recv(4096)
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
        return(data2)
    
    def get_temp_T8_test(self):
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
    
    def get_temp_T8(self):
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
        data = self.srvsock.recv(4096)
        data = float(data[26:-2])
        return (data)
        
    def get_temp_T5(self):
        self.srvsock.sendall(b'READ:DEV:T5:TEMP:SIG:TEMP\r\n')
        data = self.srvsock.recv(4096)
        data = float(data[26:-2])
        return (data)
    
    def get_tset_T8(self):
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:LOOP:TSET\r\n')
        
    def get_sweeprate(self):
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:RAMP:RATE\r\n')
        
    def set_temp_channel(self,channel):
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:LOOP:CHAN:{}\r\n'.format(channel))
                             
    def intialize_tempset_default(self,maxtemp):
        #PID Settings
        if maxtemp < 1.2:
            self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:P:15\r\n')
            self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:I:120\r\n')
            self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:D:0\r\n')
        else:
            self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:P:3\r\n')
            self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:I:10\r\n')
            self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:D:0\r\n')
        #Heater range
        if maxtemp < 1:
            self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RANGE:10\r\n')
        else:
            self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RANGE:3.16\r\n')
        if maxtemp > 2:
            print('Switch off the turbo, switch off the still heater, close V9, open V4, change channel to T5')

    def set_PID_on(self):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:MODE:ON\r\n')
    
    def set_PID_off(self):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:MODE:OFF\r\n')
    
    def set_heater_range(self,htrrange):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:MODE:ON\r\n')
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RANGE:{}\r\n'.format(htrrange))
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:MODE:OFF\r\n')
    
    def set_temp_T8(self,tset):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:{}\r\n'.format(tset))
        
    def set_temp_T8_wait(self,tset,delta = 0.01):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:{}\r\n'.format(tset))
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
        temp = self.srvsock.recv(4096)
        temp = float(data[26:-2])
        if (temp < tset-delta or temp > tset+delta):
            sleep(5)
            self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
            temp = self.srvsock.recv(4096)
            temp = float(temp[26:-2])
        sleep(60)

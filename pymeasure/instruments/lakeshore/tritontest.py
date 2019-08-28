"""
This driver is used to controll and measure the temperature via the Lakeshore 370 using the Triton controll software.

Users must understand how to control the fridge as this program does not switch thermometers or sensors. Additional 
precautions must be taken if scanning above 2K. Look at 5-14 in the oxford manual.

"""
import time
import socket
import numpy as np

class TritonLakeshore():
    
    """ Allows user to control Lakeshore370 via the Triton control software"""
    
    ### Get functions ###
    
    def connect(self): #Opens up socket connection between Triton and Python#
        edsIP = "localhost"
        edsPORT = 33576
        MESSAGE = b'SET:DEV:UID:TEMP:MEAS:ENAB:\r\n'
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.settimeout(20) # 3 second timeout on commands
        self.srvsock.connect((edsIP, edsPORT))
        
    def initalize_measure_T8(self): #Usually not needed to run a measurement as this should be the default state anyway#
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:MODE:ON\r\n')
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:MEAS:ENAB:ON\r\n')
        data2 = self.srvsock.recv(4096)
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
        return(data2)
    
    def get_temp_T8(self): #This will get the temperature reading from the RuO thermometer, for use below 1.2K#
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
        data = self.srvsock.recv(4096)
        data = float(data[26:-2])
        return (data)
        
    def get_temp_T5(self): #This will get the temmperature reading from the Cernox thermometer, for use above 1.2K#
        self.srvsock.sendall(b'READ:DEV:T5:TEMP:SIG:TEMP\r\n')
        data = self.srvsock.recv(4096)
        data = float(data[26:-2])
        return (data)
    
    def get_tset_T8(self): #This will get the temperature set point#
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:LOOP:TSET\r\n')
        
    def get_sweeprate(self): #Temperature sweep rate, to use must also turn on the rate#
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:RAMP:RATE\r\n')
        
        ### Set Functions ###
        
    def set_temp_channel(self,channel): #used to manually change the channel used in the PID feedback loop, this will automatically change at 1.2 to the channel 5#
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:LOOP:CHAN:{}\r\n'.format(channel))

    def set_PID_on(self):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:MODE:ON\r\n')
    
    def set_PID_off(self):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:MODE:OFF\r\n')
    
    def set_heater_range(self,htrrange):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RANGE:{}\r\n'.format(htrrange))
        
    def set_temp(self,tset):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:TSET:%s\r\n' %tset)
        
    def set_ramprate(self,ramprate):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RAMP:RATE:{}\r\n'.format(ramprate))
    
    def set_ramp_on(self):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RAMP:ENAB:ON\r\n')
        
    def set_ramp_off(self):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RAMP:ENAB:OFF\r\n')
        
    ### Multi step functions ###
    
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
        
    def set_temp_wait_1(self,tset,delta = 0.01):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:TSET:{}\r\n'.format(tset))
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
        temp = self.srvsock.recv(4096)
        temp = float(data[26:-2])
        if (temp < tset-delta or temp > tset+delta):
            sleep(5)
            self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
            temp = self.srvsock.recv(4096)
            temp = float(temp[26:-2])
        sleep(60)
        
    def set_temp_wait_2(self,tset,delta = 0.01):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:TSET:{}\r\n'.format(tset))
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
        temp1 = self.srvsock.recv(4096)
        temp1 = float(data[26:-2])
        sleep(30)
        self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
        temp2 = self.srvsock.recv(4096)
        temp2 = float(data[26:-2])
        if (abs(temp1 - temp2) > delta):
            temp2 = temp1
            sleep(30)
            self.srvsock.sendall(b'READ:DEV:T8:TEMP:SIG:TEMP\r\n')
            temp1 = self.srvsock.recv(4096)
            temp1 = float(data[26:-2])
    
    def to_base(self):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RAMP:ENAB:OFF\r\n')
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RANGE:0\r\n')
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:MODE:OFF\r\n')
        
    def init_temp_swp(self,tempi,ramprate,hrt):
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:MODE:OFF\r\n')
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:TSET:{}\r\n'.format(tempi))
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RAMP:RATE:{}\r\n'.format(ramprate))
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RAMP:ENAB:ON\r\n')
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:RANGE:{}\r\n'.format(htr))
        self.srvsock.sendall(b'SET:DEV:T8:TEMP:LOOP:MODE:ON\r\n')
        
        

"""
This file is used to control the magnet power supply through the triton software

Note that there are no safety interlocks. Make sure you know what you are doing and the fridge is in a safe place to turn 
the magnet on.

"""

import time
import socket
import numpy as np

class Mercuryips():
    
    """ Allows user to control Lakeshore370 via the Triton control software"""
    
    def connect(self):
        edsIP = "localhost"
        edsPORT = 33576
        MESSAGE = b'SET:DEV:UID:TEMP:MEAS:ENAB:\r\n'
        self.srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvsock.settimeout(20) # 3 second timeout on commands
        self.srvsock.connect((edsIP, edsPORT))

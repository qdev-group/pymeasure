##This is a generic code to measure resistance using DC Keithley 2400 and nvm, it does not record any other values
## It will sweep a current from the set min current to the set max current with the given steps

"""

### Import ###

#Required packages
import numpy as np
import time

#Drivers
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.instruments.keithley import Keithley2000

nvm = Keithley2000("GPIB::15")
source = Keithley2400("GPIB::21")

### Setup nvm ###

### Setup 2400 ###

currentmax = 1e-6
currentmin = 0
currentstep = 1e-8
currentrange =  int((currentmax-currentmin)/currentstep+1)

source.apply_current()
print(nvm.voltage) #Test the nvm connection
nvm.beep_state = 'disabled'

source.source_current = .1e-6
source.source_current = 0

## initalize array ##
current = []
voltage = []
setcurrent = currentmin

## IV sweep ##
for i in range(currentrange):
    source.source_current = setcurrent
    current = np.append(current, float(source.source_current))
    voltage = np.append(voltage, float(nvm.voltage))
    setcurrent = setcurrent + currentstep

## save the data ##
IVsweep = np.asarray([current,voltage])
IVsweep = np.transpose(IVsweep)

np.savetxt("C2S10_IV_7_3.txt", IVsweep, fmt='%.18e', delimiter=' ', newline=';\r\n')

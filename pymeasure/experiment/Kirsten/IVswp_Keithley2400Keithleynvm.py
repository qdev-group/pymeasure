his is a generic code to measure resistance using DC Keithley 2400 and nvm

"""

### Import ###

import numpy as np
import time

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
print(nvm.voltage)
print(nvm.beep_state)
nvm.beep_state = 'disabled'

source.source_current = .1e-6
source.source_current = 0

## initalize array ##
current = []
voltage = []
setcurrent = currentmin

for i in range(currentrange):
    source.source_current = setcurrent
    current = np.append(current, float(source.source_current))
    voltage = np.append(voltage, float(nvm.voltage))
    setcurrent = setcurrent + currentstep


IVsweep = np.asarray([current,voltage])
IVsweep = np.transpose(IVsweep)

np.savetxt("C2S10_IV_7_3.txt", IVsweep, fmt='%.18e', delimiter=' ', newline=';\r\n')

from pymeasure.instruments import Instrument, discreteTruncate
from pymeasure.instruments.validators import strict_discrete_set, \
    truncated_discrete_set, truncated_range

import numpy as np
import time
import re


class SR560(Instrument):


    """
    This is the qcodes driver for the SR 560 Voltage-preamplifier.

    This is a virtual driver only and will not talk to your instrument.

    Note:

    - The ``cutoff_lo`` and ``cutoff_hi`` parameters will interact with
      each other on the instrument (hi cannot be <= lo) but this is not
      managed here, you must ensure yourself that both are correct whenever
      you change one of them.

    - ``gain`` has a vernier setting, which does not yield a well-defined
      output. We restrict this driver to only the predefined gain values.

    """

  CUTOFF_FREQUENCIES = ['DC', 0.03, 0.1, 0.3, 1, 3, 10, 30, 100, 300, 1000,
                   3000, 10000, 30000, 100000, 300000, 1000000]

  GAINS = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000,
                 10000, 20000, 50000]
               
  coupling = Instrument.control(
    "CPLG?", "CPLG")
  
  cutoff_lo = Instrument.control()


   cutoff_hi = 


   invert = 
                         

   gain = 


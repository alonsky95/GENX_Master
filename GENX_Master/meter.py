## meter.py is an abstract class that specifies the Meter interface to be passed as Ref or Dut
# it should implement the PSU interface in order to work with FST scripts

from abc import ABC, abstractmethod
from device_dut import Dut
from psu import PSU

class Meter(PSU):
    @abstractmethod
    def fn1(self):
        pass

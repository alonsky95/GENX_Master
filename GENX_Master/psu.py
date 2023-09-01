## psu.py is an abstract class that specifies the PowerSupplyUnit type to be used to validate conformity to FST tests
# this should be used to type check Dut to validate that it can be run with FST tests

from abc import ABC, abstractmethod
from device import Device

class PSU(Device):
    @abstractmethod
    def fn1(self):
        """  """
        pass
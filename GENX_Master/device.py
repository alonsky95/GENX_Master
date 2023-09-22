## device.py is an abstract class that specifies the Device interface for use by dut.py and ref.py

from util.logger import Log
from util.comm import Comm
from abc import ABC, abstractmethod

class Device(ABC):
    def __init__(self ,log: Log, comm: Comm):
        self.connect()
        self.get_properties()

        ## Critical properties of Dut (safety limits)
        # self.operating_voltage
        # self.operating_current?
        # 

    @abstractmethod
    def connect(self):
        """ Initializing the dut requires checking the connection; Should handle exception if fails to establish connection """
        pass

    @abstractmethod
    def init_properties(self):
        """ Each dut should be populated with essential properties to function """
        pass
## nic.py is an abstract class that specifies the Nic interface to be passed as Ref() or Dut()
# it should implement the Radio interface in order to work with EVT scripts

from abc import ABC, abstractmethod
from radio import Radio

class Nic(Radio):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def connect(self):
        """ Initializing the dut requires checking the connection; Should handle exception if fails to establish connection """
        pass

    @abstractmethod
    def _query_properties(self):
        """ Locate appropriate nic properties from librarian.py """
        pass

    @abstractmethod
    def init_properties(self):
        """ Try to obtain device properties from the Nic; proceed to query_properties() for remainder """
        pass

    @abstractmethod
    def get_properties(self):
        """ Each dut should be populated with essential properties to function """
        pass

    @abstractmethod
    def get_device_type(self):
        """ Get the device type of the Nic """
        pass
    
    @abstractmethod
    def set_device_type(self, device_type):
        """ Set the device type of the Nic """
        pass

    @abstractmethod
    def get_mac_address(self):
        """ Get the mac address of the Nic """
        pass

    @abstractmethod
    def set_mac_address(self, mac_address):
        """ Set the mac address of the Nic """
        pass

    @abstractmethod
    def get_mac_address(self):
        """ Get the mac address of the Nic """
        pass

    @abstractmethod
    def set_mac_address(self, mac_address):
        """ Set the mac address of the Nic """
        pass
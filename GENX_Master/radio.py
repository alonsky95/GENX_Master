## radio.py is an abstract class that specifies the Radio type to be used to validate conformity to EVT tests
# this should be used to type check Dut to validate that it can be run with EVT tests

from abc import ABC, abstractmethod
from device import Device

class Radio(Device):
    """ Make this generic enough to work with FHSS and MUTT mode; aka use country_codes, phy_modes, and a lookup table 
    
        Restrict setting specific modulation and frequency ranges to the channel_plan/mode_plan tables
    """
    @abstractmethod
    def get_mode(self) -> int:
        """ Returns the phy mode of the radio """
        pass


    @abstractmethod
    def set_mode(self, modulation: int):
        """ Sets the phy mode of the radio """
        pass


    @abstractmethod
    def get_power_level(self) -> int:
        """ Returns the power level of the radio """
        pass


    @abstractmethod
    def set_power_level(self, power_level: int):
        """ Sets the power level of the radio """
        pass


    @abstractmethod
    def set_country_code(self, country_code: int):
        """ Sets the country code of the radio """


    @abstractmethod
    def transmit_cw(self):
        """ Initialize radio transmission using cw signal """
        pass


    @abstractmethod
    def transmit_packets(self):
        """ Initialize radio transmission to send packets """
        pass


    @abstractmethod
    def receive_packets(self):
        """ Initialize radio reception """
        pass
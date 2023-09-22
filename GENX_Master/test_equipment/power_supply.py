## power_supply.py is an abstract class that specifies what is required to function as a PowerSupply
# this should be abstract methods that specify the minimum operations required by a power supply (i.e. measure the frequency)

from abc import ABC, abstractmethod

class PowerSupply(ABC):
    @abstractmethod
    def set_output():
        pass

    @abstractmethod
    def get_output():
        pass

    @abstractmethod
    def set_voltage(self, voltage):
        pass

    @abstractmethod
    def get_voltage(self):
        pass

    @abstractmethod
    def set_current(self, current):
        pass

    @abstractmethod
    def get_current(self):
        pass
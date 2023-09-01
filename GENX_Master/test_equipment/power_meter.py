## power_meter.py is an abstract class that specifies what is required to function as a PowerMeter
# this should be abstract methods that specify the minimum operations required by a power meter (i.e. read the power)

from abc import ABC, abstractmethod

class PowerMeter(ABC):
    @abstractmethod
    def read_power():
        pass
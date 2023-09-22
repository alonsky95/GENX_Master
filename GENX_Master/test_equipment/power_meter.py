## power_meter.py is an abstract class that specifies what is required to function as a PowerMeter
# this should be abstract methods that specify the minimum operations required by a power meter (i.e. read the power)

from abc import ABC, abstractmethod

class PowerMeter(ABC):
    @abstractmethod
    def set_cal_level(self, level):
        pass
       
    @abstractmethod
    def set_frequency(self, freq):
        pass

    @abstractmethod
    def read_peak_power_level(self):
        pass

    @abstractmethod
    def read_average_power_level(self):
        pass
    
    @abstractmethod
    def read_outputpower(self,channel):
        pass

    @abstractmethod
    def read_trigger_count(self):
        pass
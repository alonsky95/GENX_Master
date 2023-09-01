## spectrum_analyzer.py is an abstract class that specifies what is required to function as a SpectrumAnalyzer
# a spectrum_analyzer can actually serve the role of power_meter and frequency_counter, with additional functionality

from abc import abstractmethod
from frequency_counter import FrequencyCounter
from power_meter import PowerMeter

class SpectrumAnalyzer(FrequencyCounter, PowerMeter):
    @abstractmethod
    def read_frequency():
        pass

    @abstractmethod
    def read_power():
        pass
## frequency_counter.py is an abstract class that specifies what is required to function as a FrequencyCounter
# this should be abstract methods that specify the minimum operations required by a frequency counter (i.e. measure the frequency)

from abc import ABC, abstractmethod

class FrequencyCounter(ABC):
    @abstractmethod
    def read_frequency():
        pass
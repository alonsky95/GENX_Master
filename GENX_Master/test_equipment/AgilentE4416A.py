from .test_equipment import TestEquipment
import time
class AgilentE4416A(TestEquipment):
    """Agilent E4416A Power Meter"""
    def __init__(self, *args, **kwargs): #<--- need kwargs?
        self.name='Agilent E4416A'
        TestEquipment.__init__(self, *args, **kwargs)

    def set_cal_level(self, level):
        pass
    
    def set_gates(self):
        pass
       
    def set_frequency(self, freq):
        pass

    def read_peak_power_level(self):
        pass

    def read_average_power_level(self):
        pass
    
    def read_outputpower(self,channel):
        pass

    def read_trigger_count(self):
        pass
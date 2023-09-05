## test_transmit_power.py is a child class of test.py which specifies the specfic test to run
# requires a dut = type(Radio)

from test import Test
from testparams import TestParams
from station import Station
from util.logger import Log
from result import Result
from typing import List
from device import Device

class TransmitPower(Test):
    """ Test plan available at https://confluence.itron.com/display/HW/Transmit+Power+EVT+Test+Procedure 
    
    """
    def __init__(self, testparams: TestParams, station: Station, duts: List(Device), log: Log): # allow for multi-dut <-- SHOULD ALSO VALIDATE IF VOLTAGES TO HIGH FOR DUT, AND IF STATION COMPATIBLE
        super().__init__(testparams, station, duts, log)


    def _validate_station_equipment(self):
        """ Checks station equipment against required equipment for test """
        pass


    def _validate_testparams_for_device_compatibility(self):
        """ Check to see that testparams aren't outside of safe limits for device """
        pass


    def calculate_runtime(self):
        """ Useful testrun statistic """
        pass


    def _single(self):
        """ Runs a single power level transmit and returns measurements """
        expected_frequency = self.get_current_channel_freq(dut)
        
        dut.transmit()
        
        time.sleep(0.1)
        
        current_draw = station.power_supply.get_current()
        
        output_power = self.test_lab.power_meter.read_peak_power_level()

        if read_freq_cntr:
            if float(output_power) >= 20.0:
                frequency = self.test_lab.frequency_counter.read_frequency(
                                                                           freq_range_hz = expected_frequency,
                                                                           average_samples = FREQUENCY_COUNTER_AVERAGE_SAMPLES
                                                                           )
                #frequency = self.test_lab.frequency_counter.read_frequency(BASE_FREQUENCY[self.modes.current]*1000)
                # should test for unusually high PPM here
            else:
                frequency = '0'
                self.log.warning("Frequency was not read because output power < 20dBm")
        else:
            frequency = '0'

        #frequency = self.get_current_channel_freq(dut)
        dut.idle()
        time.sleep(0.1)
        
        return {'output_power_dbm' : output_power, 'current_draw_amps' : current_draw, 'frequency_hz' : frequency} 


    def _sweep(self):
        """ Runs multiple power levels """
        self._single()
        pass 


    def run(self) -> List(Result):
        """ Executes the test; Will return a record of Result objects for each dut """
        self._sweep()
        pass


## test_transmit_power.py is a child class of test.py which specifies the specfic test to run
# requires a dut = type(Radio)

from test import Test
from testparams import TestParams
from station import Station
from device_dut import Dut
from util.logger import Log
from result import Result
from typing import List

class TransmitPower(Test):
    """ Test plan available at https://confluence.itron.com/display/HW/Transmit+Power+EVT+Test+Procedure 
    
    """
    def __init__(self, testparams: TestParams, station: Station, duts: List(Dut), log: Log): # allow for multi-dut <-- SHOULD ALSO VALIDATE IF VOLTAGES TO HIGH FOR DUT, AND IF STATION COMPATIBLE
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
        pass


    def _sweep(self):
        """ Runs multiple power levels """
        self._single()
        pass 


    def run(self) -> List(Result):
        """ Executes the test; Will return a record of Result objects for each dut """
        self._sweep()
        pass


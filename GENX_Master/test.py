## test.py is an semi-abstract class that specifies the Test interface for use by testbed.py

from abc import ABC, abstractmethod
from testparams import TestParams
from station import Station
from device import Device
from util.logger import Log
from typing import List

class Test(ABC):
    ## Sub-module that is run by testbed.py
    # equipment & dut setup: could retain test-tree (or better yet create an abstract test_params_struct for iterating through) and keep within test.py; then testbed.py loop through test.test_params
    # single() and run_sweep() should be refactored <--- these are the only concerns test should have;
    # -> perhaps it makes sense to have them where run_sweep() doesn't mess with results_file configuration
    # -> instead, run_power_levels() or equivalent return a json (or other datastruct like result()) to be captured in testbed() <- MUCH BETTER SOC enabling unittest development

    def __init__(self, testparams: TestParams, station: Station, duts: List(Device), log: Log): # allow for multi-dut <-- SHOULD ALSO VALIDATE IF VOLTAGES TO HIGH FOR DUT, AND IF STATION COMPATIBLE
        self.testparams = testparams
        self.station = station
        self.duts = duts
        self.log = log
        self._validate_station_equipment()
        self._validate_testparams_for_device_compatibility()


    @abstractmethod
    def _validate_station_equipment(self):
        """ Checks station equipment against required equipment for test """
        pass

    @abstractmethod
    def _validate_testparams_for_device_compatibility(self):
        """ Check to see that testparams aren't outside of safe limits for device """
        pass

    @abstractmethod
    def calculate_runtime(self):
        """ Useful testrun statistic """
        pass

    @abstractmethod
    def _single(self):
        """ Helper function that facilitates better separation of concerns with Test classes """
        pass

    @abstractmethod
    def _sweep(self):
        """ Helper function that facilitates better separation of concerns with Test classes """
        pass 

    @abstractmethod
    def run(self) -> List:
        """ Executes the test; Will return a record of Result objects for each dut """
        pass


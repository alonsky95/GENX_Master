## Serves as the main insertion point into the program
# Works similar to GEN5_Master/test.py, the difference being that it uses a 'test' interface to utilize composition (as opposed to inheritence)
from test import Test
from station import Station
from device_dut import Dut
from util.logger import Log
from typing import List
from testparams import TestParams

# NOTE: SOC entails having each object resposible for checking compatibility of their dependencies (checking if test() and station() are compatible, prompting if test has been run with dut(), etc.)
class TestSuite:
    ## Top-level module: should be the main test loop
    # 1) connects all components together
    # 2) validates if station() can run test()
    #  a) could extend to multi-test, checking/skipping tests that aren't supported
    # 3) additional features that support runnning test (statistics, email_notifications, etc.)

    def __init__(self, testparams: List(TestParams), station: Station, duts: List(Dut), log: Log): # List(TestParams) will be unpacked to build the multi-test
        pass # specfic TestParams types will inform factory function what test to build, constructing test queue
    

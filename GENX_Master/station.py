## station.py is an concrete class that specifies the Station for use by testbed.py
# based off of GEN5_Master/lab.py
import test_equipment
from test_equipment.test_equipment_factory import TestEquipmentConfig, TestEquipmentFactory
from util.logger import Log
from device import Device
from typing import List
from util.dummy_logger import DummyLogger
from dataclasses import dataclass

@dataclass
class Calibration:
    dut1_powermeter: int
    dut2_powermeter: int
    dut3_powermeter: int
    dut1_ref: int
    dut2_ref: int
    dut3_ref: int

@dataclass
class TestDeviceConfig:
    name: str
    power_supply_channel: str
    address: str
    baudrate: int

# it makes sense (to me) that a program should use dataclasses for data/config since it clearly states the parameters required by the program
# dynamic datatypes such as dicts and lists can be used for dynamic algorithms/objects
@dataclass
class Config:
    test_instrument_definitions: List[TestEquipmentConfig]
    test_device_definitions: List[TestDeviceConfig]

class Station():
    def __init__(self, log: Log, config: Config, calibration: Calibration, duts: Device):
        self.log = log
        self.calibration = calibration
        self.test_equipment = self._init_test_equipment(config.test_instrument_definitions)
        self.duts = self._init_duts(config)
        self.refs = self._init_refs(config)

    def _init_test_equipment(self, test_instrument_definitions): # if it's a private method, might as well access the object attributes themselves
        """ Calls TestEquipmentFactory to create the test_equipment specified in the config """
        test_equipment_list = []
        for test_instrument_definition in test_instrument_definitions:
            test_equipment_list.append(TestEquipmentFactory.new_test_equipment(test_instrument_definition))
        return test_equipment_list

    def _init_refs(config):
        """ Creates a tuple of refs and initializes them? """
        return tuple(ref)

    def _init_duts(config):
        """ Creates a tuple of duts to associate dut with position in station """
        return tuple(dut1, dut2, dut3)


if __name__ == '__main__':
    conf = Config([TestEquipmentConfig('power_meter', 'GPIB0::13::INSTR', 'AgilentE4416A')], [])
    stn = Station(DummyLogger(), conf, None, None)
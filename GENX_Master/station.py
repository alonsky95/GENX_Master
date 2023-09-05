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


@dataclass
class StationTestEquipment:
    power_meter: test_equipment.power_meter.PowerMeter
    power_supply: test_equipment.power_supply.PowerSupply
    frequency_counter: test_equipment.frequency_counter.FrequencyCounter
    spectrum_analyzer: test_equipment.spectrum_analyzer.SpectrumAnalyzer
    variable_attentuator: test_equipment.variable_attenuator.VariableAttenuator


# it makes sense (to me) that a program should use dataclasses for data/config since it clearly states the parameters required by the program
## HERE'S WHAT IT IS: Dataclasses are an interface, while dicts/lists/etc are an implementation; If you forsee a need to change the implementation, dataclasses keep things abstract
# dynamic datatypes such as dicts and lists can be used for dynamic algorithms/objects


@dataclass
class Config:
    test_instrument_definitions: List[TestEquipmentConfig]
    test_device_definitions: List[TestDeviceConfig]


class Station():
    def __init__(self, log: Log, config: Config, calibration: Calibration):
        self.log = log
        self.calibration = calibration
        self.test_equipment = self._init_test_equipment(config.test_instrument_definitions)
        self.refs = self._init_refs(config.test_device_definitions) # number of refs known to station 


    def _init_test_equipment(self, test_instrument_definitions):
        """ Calls TestEquipmentFactory to create the test_equipment specified in the config """
        test_equipment_list = []
        for test_instrument_definition in test_instrument_definitions:
            test_equipment_list.append(TestEquipmentFactory.new_test_equipment(test_instrument_definition))
        return test_equipment_list


    def _init_refs(test_device_definitions):
        """ Creates a tuple of refs and initializes them? """
        return tuple(ref)


    def init_duts(duts_to_test: List[DutConfig]):
        """ PUBLIC METHOD (dut shouldn't be property of station) 
        Checks to see if duts can be run at station and then creates dut objects with associated position 
        """
        DeviceFactory(duts_to_test)
        return tuple(dut1, dut2, dut3)


if __name__ == '__main__':
    conf = Config([TestEquipmentConfig('power_meter', 'GPIB0::13::INSTR', 'AgilentE4416A')], [])
    stn = Station(DummyLogger(), conf, None, None)
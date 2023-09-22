## station.py is an concrete class that specifies the Station for use by testbed.py
# based off of GEN5_Master/lab.py
from test_equipment import power_meter, power_supply, frequency_counter, spectrum_analyzer
from test_equipment.test_equipment_factory import TestEquipmentConfig, TestEquipmentFactory
from station_device_factory import StationDeviceFactory, StationDeviceConfig, DeviceConfig, OpMode, DeviceRole
from util.logger import Log
from typing import List
from util.dummy_logger import DummyLogger
from dataclasses import dataclass
from enum import Enum

@dataclass
class Calibration:
    dut1_powermeter: int
    dut2_powermeter: int
    dut3_powermeter: int
    dut1_ref: int
    dut2_ref: int
    dut3_ref: int


@dataclass
class StationTestEquipment:
    power_meter: power_meter.PowerMeter
    power_supply: power_supply.PowerSupply
    frequency_counter: frequency_counter.FrequencyCounter
    spectrum_analyzer: spectrum_analyzer.SpectrumAnalyzer
    # variable_attentuator: test_equipment.variable_attenuator.VariableAttenuator


# it makes sense (to me) that a program should use dataclasses for data/config since it clearly states the parameters required by the program
## HERE'S WHAT IT IS: Dataclasses are an interface, while dicts/lists/etc are an implementation; If you forsee a need to change the implementation, dataclasses keep things abstract
# dynamic datatypes such as dicts and lists can be used for dynamic algorithms/objects


@dataclass
class Config:
    """ Data struct that specifies the configuration for the Station; A new config file should be created if ever the station changes """
    test_instrument_definitions: List[TestEquipmentConfig]
    station_device_definitions: List[StationDeviceConfig]


class Station():
    def __init__(self, log: Log, config: Config, calibration: Calibration):
        self.log = log
        self.config = config
        self.calibration = calibration
        self.test_equipment = self._init_test_equipment()
        self.refs = self._init_refs() # number of refs known to station 


    def _init_test_equipment(self) -> StationTestEquipment:
        """ Calls TestEquipmentFactory to create the test_equipment specified in the config """
        station_test_equipment = StationTestEquipment(
            power_meter = None,
            power_supply = None,
            frequency_counter = None,
            spectrum_analyzer = None
        )

        for test_instrument_definition in self.config.test_instrument_definitions:
            setattr(station_test_equipment, test_instrument_definition.test_equipment, TestEquipmentFactory.new_test_equipment(self.log, test_instrument_definition))

        return station_test_equipment


    def _init_refs(self) -> tuple:
        """ Creates a tuple of refs and initializes them? """
        return tuple(StationDeviceFactory.new_device(self.log, station_ref) for station_ref in sorted(self.config.station_device_definitions) if station_ref.role == DeviceRole.REF)


    def _build_station_devices_from_dut_configs(self, dut_configs: List[DeviceConfig]):
        """ Associates station device config with device config for init_duts() """
        dut_station_device_definitions = [test_device for test_device in sorted(self.config.station_device_definitions) if test_device.role == DeviceRole.DUT]
        if not len(dut_configs) == len(dut_station_device_definitions):
            raise ValueError("Number of dut configs does not match number of station duts")
        
        for station_device_def, dut_config in zip(dut_station_device_definitions, dut_configs):
            station_device_def.device_conf = dut_config

        return dut_station_device_definitions


    def init_duts(self, duts_config: List[DeviceConfig]) -> tuple:
        """ PUBLIC METHOD (dut shouldn't be property of station) 
        Checks to see if duts can be run at station and then creates dut objects with associated position 
        """
        station_duts = self._build_station_devices_from_dut_configs(duts_config)
        return tuple(StationDeviceFactory.new_device(self.log, station_dut) for station_dut in station_duts)


if __name__ == '__main__':
    dummy_equipment_conf = TestEquipmentConfig('power_meter', 'GPIB0::13::INSTR', 'AgilentE4416A')
    dummy_device_conf = DeviceConfig('Prion', OpMode.FHSS, 115200)
    dummy_station_device_conf1 = StationDeviceConfig(dummy_device_conf, DeviceRole.REF, 1, 1, 'COM5')
    dummy_station_device_conf2 = StationDeviceConfig(None, DeviceRole.DUT, 2, 2, 'COM6')
    dummy_conf = Config([dummy_equipment_conf], [dummy_station_device_conf1, dummy_station_device_conf2])
    
    stn = Station(DummyLogger(), dummy_conf, None)
    print(stn.test_equipment)
    #assert (conditional, explaination) <---- good practice (use multiple for granular condition checking)
    duts = stn.init_duts([dummy_device_conf])
    duts[0].get_mac_address()
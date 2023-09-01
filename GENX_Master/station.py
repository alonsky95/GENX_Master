## station.py is an concrete class that specifies the Station for use by testbed.py
# based off of GEN5_Master/lab.py
import test_equipment
from util.logger import Log
from device import Device
from typing import List

@dataclass
class Calibration:
    dut1_powermeter: int
    dut2_powermeter: int
    dut3_powermeter: int
    dut1_ref: int
    dut2_ref: int
    dut3_ref: int

@dataclass
class TestEquipmentConfig:
    test_equipment: str
    instrument_address: str
    make_model: str

@dataclass
class TestDeviceConfig:
    name: str
    power_supply_channel: str
    address: str
    baudrate: int

@dataclass
class Config:
    test_instrument_definitions: List(TestEquipmentConfig)
    test_device_definitions: List(TestDeviceConfig)

class Station():
    def __init__(self, log: Log, config: Config, calibration: Calibration, duts: Device):
        self.calibration = calibration
        self.test_equipment = self.init_test_equipment()
        self.duts = self.init_duts()
        self.refs = self.init_refs()

    def init_test_equipment():
        pass

    def init_refs():
        pass

    def init_duts():
        pass

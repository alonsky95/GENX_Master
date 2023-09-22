## device_factory.py is a utility object that specifies how device objects are to be created
from dataclasses import dataclass
from enum import Enum
from prion_fhss import PrionFHSS
from GENX_Master.util.comm_serial_prion_fhss import FHSSPrionSerialComm
from GENX_Master.util.logger import Log


class OpMode(Enum):
    FHSS = 1
    MUTT = 2
    PROD = 3

    def __eq__(self, other):
        return self.value == other.value


class DeviceRole(Enum):
    """ Defines the two roles that a device can take (and no others)"""
    DUT = 1
    REF = 2

    def __eq__(self, other):
        return self.value == other.value


@dataclass
class DeviceConfig:
    """ Device config independent of station """
    device: str
    mode: OpMode
    baudrate: int
    # something else?


@dataclass #<--- how do I associate a DeviceConfig with the address from station?
class StationDeviceConfig:
    device_conf: DeviceConfig # config objs make sense to save the object without pickling
    role: DeviceRole
    position: int
    power_supply_channel: int
    address: str

    def __lt__(self, other):
        if self.role.value == other.role.value:
            return self.position < other.position
        else:
            return self.role.value < other.role.value


class StationDeviceFactory:
    @staticmethod
    def new_device(log: Log, config: StationDeviceConfig):
        if config.device_conf.device == 'Prion':
            if config.device_conf.mode == OpMode.FHSS:
                device_name = ''.join([config.role.name, str(config.position)])
                comm = FHSSPrionSerialComm(log, device_name, config.address, config.device_conf.baudrate)
                return PrionFHSS(log, comm) # auto-detect specific Prion product
        if config.device_conf.device == 'Itron500m':
            return Itron500M()
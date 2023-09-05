## test_equipment.py is a base class that specifies the methods general to all test_equipment
# this is an interface to the common SCPI commands

from GENX_Master.util.comm import Comm
from GENX_Master.util.logger import Log
from enum import Enum, auto

# class TestEquipmentType(Enum):
#     power_meter: auto()
#     power_supply: auto()
#     spectrum_analyzer: auto()
#     frequency_counter: auto()

class TestEquipment:
    def __init__(self, log: Log, comm: Comm):
        self._comm = comm


    def reset(self):
        """ Standard SCPI command """
        return self._comm.write_get('*RST')


    def get_id(self):
        """ Standard SCPI command """
        return self._comm.write_get('*IDN?')
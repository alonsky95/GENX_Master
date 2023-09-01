## test_equipment.py is a base class that specifies the methods general to all test_equipment
# this is an interface to the common SCPI commands

from util.comm import Comm

class TestEquipment:
    def __init__(self, comm: Comm):
        self._comm = comm

    def get_id(self):
        """ Standard SCPI command """
        return self.comm.write_get('*IDN?')
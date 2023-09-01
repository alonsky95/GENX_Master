## comm_visa.py is a concrete class that specifies the Comm module for facilitating serial communication
# should allow for unittesting of visa communication link

from comm import Comm
import pyvisa

class VisaComm(Comm):
    def __init__(self):
        pass
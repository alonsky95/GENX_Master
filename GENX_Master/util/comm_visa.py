## comm_visa.py is a concrete class that specifies the Comm module for facilitating serial communication
# should allow for unittesting of visa communication link

from .comm import Comm
from pyvisa import ResourceManager
from .logger import Log

class VisaComm(Comm):
    def __init__(self, log: Log, name, address):
        self.instrument_name = name
        self.instrument_address = address
        super().__init__(log)


    def open(self):
        """ Tries to open the communication link and returns exception if failure occurs """
        try:
            rm = ResourceManager()
            self._inst = rm.open_resource(self.instrument_address, timeout=30)

        except Exception as err:
            err_str = 'Unable to open instrument %s on %s.\n' % (self.instrument_name, self.instrument_address)
            err_str += str(err)
            self.log.error(err_str)
            self._inst = None
        
        else:
            self.log.info('Connected to instrument: ' + self.instrument_name + ' : ' + self.instrument_address)


    def communications_check(self):
        """ Sends a command to ensure device/instrument is communicating properly """
        pass


    def close(self):
        """ Closes connection, releasing resource """
        pass


    def read(self):
        """ Helper function to be used by write_set() and write_get() """
        return self._inst.read()


    def write_set(self, command):
        """ Sends command to device and return a status message """
        self._inst.write(command)


    def write_get(self, command):
        """ Queries the device for a response """
        return self._inst.query(command)
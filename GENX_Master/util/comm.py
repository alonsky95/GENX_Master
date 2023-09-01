## comm.py is a concrete class that specifies the Comm module for facilitating communication
# should allow for unittesting of communication link

from logger import Log
from abc import ABC, abstractmethod

class Comm(ABC):
    def __init__(self, log: Log):
        self.log = log
        self.command_history = [] # history of commands issued
        self.open()
        self.communications_check()


    @abstractmethod
    def open(self):
        """ Tries to open the communication link and returns exception if failure occurs """
        pass

    @abstractmethod
    def communications_check(self):
        """ Sends a command to ensure device/instrument is communicating properly """
        pass

    @abstractmethod
    def close(self):
        """ Closes connection, releasing resource """
        pass

    @abstractmethod
    def read(self, timeout=15, extra_read_time_ms=5):
        """ Helper function to be used by write_set() and write_get() """
        pass

    @abstractmethod
    def _write(self, command, character_delay_ms=0):
        """ Helper function to be used by write_set() and write_get() """
        pass

    @abstractmethod
    def write_set(self, command_list, extra_read_time_ms=5):
        """ Sends command to device and return a status message """
        pass

    @abstractmethod
    def write_get(self, command, extra_read_time_ms=5, character_delay_ms=0):
        """ Queries the device for a response """
        pass
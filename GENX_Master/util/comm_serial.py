## comm_serial.py is a concrete class that specifies the Comm module for facilitating serial communication
# should allow for unittesting of serial communication link

from abc import abstractmethod
from comm import Comm
import serial
import time
from logger import Log

## Constants
DEFAULT_TIMEOUT = 10
DEFAULT_BAUDRATE = 115200
DEFAULT_TERMINATOR = '\r\n'

class SerialComm(Comm):
    def __init__(self, log:Log, com_port, baudrate=DEFAULT_BAUDRATE, terminator=DEFAULT_TERMINATOR, timeout=DEFAULT_TIMEOUT):
        self.com_port = com_port
        self.baudrate = baudrate
        self.terminator = terminator
        self.timeout = timeout
        self.extra_read_wait = 0 # legacy code
        super().__init__(log)


    def open(self):
        """ Tries to open the communication link and returns exception if failure occurs """
        try:
            self._ser = serial.Serial(self.com_port, baudrate=self.baudrate, timeout=DEFAULT_TIMEOUT)
        
        except serial.SerialException:
            self.log.critical('Cannot connect to device %s on %s' % (self.name, self.com_port))
            self.log.critical('Exiting program.')    
            exit()
            
        self.log.info('Connected to device: %s %s %s' % (self.name, self._ser.port, self._ser.baudrate)) 


    def communications_check(self):
        """ Sends a command to ensure device/instrument is communicating properly """
        self.log.exception("For comm check only - Method should be overriden in child class")


    def close(self):
        """ Closes connection, releasing resource """
        self._ser.close()


    def _read_buffer(self, timeout=15, extra_read_time_ms=5):
        """ Helper function to be used by read() """
        #extra_read_time_ms is a command by command delay
        # Waits for serial buffer to contain characters, then
        # reads raw input from the serial buffer
        raw_input = ''
        time_started = time.time()
        time.sleep(0.1 + self.extra_read_wait + extra_read_time_ms/1000)
        
        #self.log.debug('read timeout = '+ str(timeout))
        #self.log.debug('extra read time in ms = '+ str(extra_read_time_ms))
        
        #wait for something to be available - or a read timeout to expire
        while (not self._ser.inWaiting()) and (time.time() - time_started < timeout):
            time.sleep(0.1 + self.extra_read_wait + extra_read_time_ms/1000)

        #if there are characters to read, then let's read them.
        while self._ser.inWaiting():
            chars_in_waiting = self._ser.inWaiting()
            #self.log.debug('Characters to read from the serial port: ' + str(chars_in_waiting))
            read_chars = self._ser.read(chars_in_waiting)
            read_chars = read_chars.decode()
            raw_input = raw_input + read_chars
            time.sleep(0.1 + self.extra_read_wait + extra_read_time_ms/1000)

        if not raw_input:
            #we didn't read anything from the serial port
            self.log.critical('Serial read for device %s on %s timed out.' %
                (self.name, self.com_port))
            raise Exception('Serial read for device %s on %s timed out.' %
                (self.name, self.com_port))
        else:
            #We read something from the serial port
            #self.log.debug('[%s] raw<- %s' % (self.name, raw_input))
            #self.log.debug('Characters read: ' + str([raw_input])) #the list around raw_input allows you to easily see string
            return raw_input
        

    @abstractmethod
    def read(self, timeout=15, extra_read_time_ms=0):
        pass


    def _write(self, command, character_delay_ms = 0):
        #Flushes serial input buffer, writes command and reads result.
        self._ser.flush()
        time.sleep(0.05)

        self.log.debug('[%s] <- %s' % (self.name, command))

        if character_delay_ms == 0:
            serialcmd = command + self.terminator
            self._ser.write(serialcmd.encode()) #need newline for ARM base products
            #self._ser.write(''.join([command, '\r']))
        else:
            for i in command:
                #self._ser.write(''.join([command, '\r\n']))
                self._ser.write(i.encode())
                time.sleep(character_delay_ms / 1000.0)
            self._ser.write(self.terminator.encode())

        self.command_history.append(''.join([command, '\r']))
        #any smaller of a delay and read/write doesn't always work
        #0.1 was too fast to get the full return input of at~phy
        time.sleep(0.05)
        time.sleep(self.extra_read_wait)
        #return self.read()


    @abstractmethod
    def write_set(self, command, extra_read_time_ms=5):
        """ Sends command to device and return a status message """
        pass


    @abstractmethod
    def write_get(self, command, extra_read_time_ms=5, character_delay_ms=0):
        """ writes the command, reads and returns the response """
        pass
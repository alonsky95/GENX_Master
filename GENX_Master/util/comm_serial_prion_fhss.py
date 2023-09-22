from GENX_Master.util.comm_serial import SerialComm
import re
from GENX_Master.util.logger import Log
from GENX_Master.util.dummy_logger import DummyLogger

## Constants
DEFAULT_TIMEOUT = 10
DEFAULT_BAUDRATE = 115200
DEFAULT_TERMINATOR = '\r\n'

class FHSSPrionSerialComm(SerialComm):
    def __init__(self, log:Log, device_name:str, com_port:str, baudrate:int=DEFAULT_BAUDRATE, terminator:str=DEFAULT_TERMINATOR, timeout=DEFAULT_TIMEOUT):
        self.name = device_name
        self.character_delay_ms = 0 # legacy code
        super().__init__(log, com_port, baudrate, terminator, timeout)
        self.communications_check()


    def communications_check(self):
        """ Checks communication with NIC """
        for tries in range(5):
            # try:
            self._write('aat', 100) #to overcome a bug in the UART code
            status = self.write_set('at')
            # except:
            #     continue
            if status == 'OK':
                break    


    def read(self, timeout=15, extra_read_time_ms=0):
        # reads standard command, response and status from serial buffer
        raw_input = self._read_buffer(timeout, extra_read_time_ms)

        # if only one line in buffer, it's probably the command echoed back
        #  and we are still waiting for the full response\

        #this is probably not that helpful - jhowarth 20/9/2011
        # the following lines were used to handle arm as well as
        # akio FHSS firmware:
        #if raw_input.count('\x00') < 2:
        #    raw_input = raw_input + self.read_buffer(timeout)

        #seperating the response

        raw_input = raw_input.strip('\x00')
        split_input = re.split(r'\x00+', raw_input)

        clean_string_1 = []
        for item in split_input:
            #print 'item: ' + str(item)
            stripped_item = item.strip('\x00')
            stripped_item = [stripped_item]
            clean_string_1 = clean_string_1 + stripped_item
            #print 'clean_string_1: ' + str(clean_string_1)
            
        split_input = clean_string_1

        clean_string_3 = []
        for line in split_input:
            split_line = line.replace('\r','\n').split('\n')
            clean_string_2 = []
            if len(split_line) > 1:
                for new_item in split_line:
                    clean_new_item = new_item.strip('\x00')
                    clean_new_item = [clean_new_item]
                    clean_string_2 = clean_string_2 + clean_new_item
                    #print "clean_string_2: " + str(clean_string_2)
            else:
                clean_new_item= split_line.strip('\x00')
                clean_new_item = [clean_new_item]
                clean_string_2 = clean_string_2 + clean_new_item
                #print "clean_string_2: " + str(clean_string_2)
            clean_string_3 = clean_string_3 + clean_string_2
        split_input = clean_string_3


        split_input = [_f for _f in split_input if _f]
        # print '\nFinal stripped and split input is'



        #there are three/five parts to the response once \x00 stripped
        #
        #if not asking for data back e.g. 'ats112=60'
        #[0] = command sent
        #[1] = status OK/ERROR '\r\nOK\r\n'
        #[2] = status OK/ERROR  (with newline character preceeding it)
        #
        #if requiring data back e.g. 'ats114?'
        #[0] =  command sent e.g. 'ats101?\r'
        #[1] =  value/s e.g. '1\r\n'
        #[2] = empty string = ''
        #[3] = status OK/ERROR '\r\nOK\r\n'
        #[4] = empty string = ''
        #
        #so we have three pieces of information we care about: command, response(if one), status(OK/ERROR)

        #command is always in the same position
        #command = re.split('\r', split_input[0])[0]
        command = split_input[0].strip()
        #print '\ncommand is'
        #print command

        # status is always last
        # strip it and replace extraneous newlines
        status = re.sub(r'[\n\r]+', '\n', split_input[-1].strip())

        #print '\nstatus is'
        #print status
        
        response = None
        if len(split_input) == 3:
            response = split_input[1].strip()
            if response == None:
                raise Exception('No response from device %s on %s\n%s' %
                            (self.name, self.com_port, raw_input))
        if len(split_input) > 3:
            response = '\n'.join(split_input[1:-1])
        if response:
            response_info = '[%s] -> %s' % (self.name, response)
            self.log.debug(response_info)
                
        if status:
            status_info = '[%s] -> %s' % (self.name, status)
            if re.search(r'assert', status, re.IGNORECASE):
                if re.search(r'Crystal value not written', status, re.IGNORECASE):
                    status_info += ('\nYou must write a crystal value to use this NIC.\n' +
                                    'For 19.2: atflxa 0x30082 4=0x01 0x24 0xF8 0x00\n' +
                                    'For 26.0: atflxa 0x30082 4=0x01 0x8C 0xBA 0x80')
                self.log.critical(status_info)
                raise Exception(status_info)
            else:
                self.log.debug(status_info)
                
        return {'command': command, 'response': response, 'status': status}        # status is always last
    

    def write_set(self, command, extra_read_time_ms=5):
        """ Sends command to device and return a status message """
        nic_response = self.write_get(command, extra_read_time_ms=extra_read_time_ms)
        #if self.verbose:
        #self.log.debug('[%s] <- %s' % (self.name, nic_response['status']))
            #print nic_response['status']
        if nic_response['status'] == 'ERROR':
            self.log.warning('NIC ' + self.name + ' did not accept command: ' + str(command))        
        return nic_response['status']


    def write_get(self, command, extra_read_time_ms=5, character_delay_ms=0):
        """ writes the command, reads and returns the response """
        if not character_delay_ms:
            character_delay_ms = self.character_delay_ms

        self._write(command, character_delay_ms)
        return self.read(extra_read_time_ms=extra_read_time_ms)


# unit-test
if __name__ == '__main__':
    dummy_log = DummyLogger()
    ser = FHSSPrionSerialComm(dummy_log, "Generic", "COM5")
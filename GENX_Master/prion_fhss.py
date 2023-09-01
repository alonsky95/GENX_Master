## prion_fhss.py is a concrete class that specifies the Prion which implements the Nic interface
# this encapsulates the FHSS commands to conform to the Nic interface

from nic import Nic
from comm_serial import SerialComm

class PrionFHSS(Nic):
    def __init__(self, Comm):
        pass

    def get_nic_data_from_terminal(self, data_type):
        if data_type == "mac_address":
            text = "MAC address"
            example = "00135001000B1234"
        elif data_type == "hardware_version":
            text = "hardware version"
            example = "17.1"
        elif data_type == "part_number":
            text = "part number"
            example = "174-000114r6 or 174-0263-00r01"
        elif data_type == "device_type":
            text = "device type"
            example = "15 (for generic NIC - most common)"     
        elif data_type == "stuffing_options":
            text = "stuffing options"
            example = "0xfc 1"
        elif data_type == "disease_name":
            text = "disease name"
            example = "eLaBrea or WestNile"
        elif data_type == "cpu_clock":
            text = "cpu_clock"
            example = "19200000 or 26000000"
        else:
            raise Exception('%s has not been defined.' % (data_type))
        
        print("\n\n")
        self.log.critical( self.name + " on " + self.com_port + ": " + text + " has not been programmed.")
        self.log.critical( "1. Program " + text)
        self.log.critical( "2. Continue")
        self.log.critical( "3. Exit")
        choice = input()
        
        while not re.match(r'^[123]$',choice):
            self.log.critical( "Please enter a number between 1 and 3.")
            choice = input("> ")
        
        #loop that makes sure we get an 'ok' back from our command
        new_value = None
        while True: 
            
            #we have reached the point where a number is either 1,2 or 3.   
            if choice == '1':
                self.log.critical("Please enter the new value in the format: " + example)
                new_value = input("> ")
      
                #now have to program it
                return_code = eval("self.set_"+ data_type+ "(new_value)")    
                
                #now check that the operation was 'ok'
                #print 'return code is : ' + str(return_code)
                if return_code.lower() == 'ok':
                    #self.nic_data[data_type] = new_value
                    #print str(data_type) + ' is: ' + self.nic_data[data_type] + '\n\n'
                    break
                
            elif choice == '2':
                break
            elif choice == '3':
                exit()
               
        if new_value:
            return new_value
        else:
            return None


    def get_wan_type(self):
        wan_type = self.write_get('atflxa 0x3000C 1?',extra_read_time_ms=2000)
        print(wan_type,type(wan_type))
        if wan_type['response'] == '0x24':
            print('NA1')
            return('NA1')
        elif wan_type['response'] == '0x25':
            print('NAG')
            return'NAG'
        elif wan_type['response'] == '0x26':
            print('SV1')
            return'SV1'           


    def get_architecture(self):
        #we don't change the cpuclk on ARM products, so if 'atcpuclk' is in 'at?', then it is akio
        self.write('at?')
        at_command_options = self.read_buffer(extra_read_time_ms=100)
        #selfprint at_command_options
        if 'atcpuclk' in at_command_options:
            self.log.debug('found atcpuclk - architecture is akio')
            return('akio')
        else:
            self.log.debug('did not find atcpuclk - architecture is arm')
            return('arm')
    
    '''        
    def set_firmware(self, firmware):
        self.nic_data['running_firmware'] = firmware
    '''
    

    def set_baudrate(self, baudrate):
        self.baud_rate = baudrate
        self._ser.baudrate = baudrate
        #ser_settings = self._ser.getSettingsDict()
        #self._ser.close()
        #self._ser = serial.Serial(self.com_port, baudrate = self.baud_rate, timeout=1)


    def dump_port_settings(self):
        sys.stderr.write("\n--- Settings: %s  %s,%s,%s,%s\n" % (
                self._ser.portstr,
                self._ser.baudrate,
                self._ser.bytesize,
                self._ser.parity,
                self._ser.stopbits))
        #sys.stderr.write('--- RTS: %-8s  DTR: %-8s  BREAK: %-8s\n' % (
        #        (self.rts_state and 'active' or 'inactive'),
        #        (self.dtr_state and 'active' or 'inactive'),
        #        (self.break_state and 'active' or 'inactive')))
        try:
            sys.stderr.write('--- CTS: %-8s  DSR: %-8s  RI: %-8s  CD: %-8s\n' % (
                    (self._ser.getCTS() and 'active' or 'inactive'),
                    (self._ser.getDSR() and 'active' or 'inactive'),
                    (self._ser.getRI() and 'active' or 'inactive'),
                    (self._ser.getCD() and 'active' or 'inactive')))
        except serial.SerialException:
            # on RFC 2217 ports it can happen to no modem state notification was
            # yet received. ignore this error.
            pass
        sys.stderr.write('--- software flow control: %s\n' % (self._ser.xonxoff and 'active' or 'inactive'))
        sys.stderr.write('--- hardware flow control: %s\n' % (self._ser.rtscts and 'active' or 'inactive'))
        #sys.stderr.write('--- data escaping: %s  linefeed: %s\n' % (
        #        REPR_MODES[self.repr_mode],
        #        LF_MODES[self.convert_outgoing]))


    def dump_registers(self, min_hex, max_hex, command = 'atmx', num_bytes = ''):
        #Takes a range register and returns their curent values.
        #Input registers in string e.g. '0x30000'
        #First converts to integer, loops through numbers and then back to hex.
        out_str = []
        min_int = int(min_hex, 16)
        max_int = int(max_hex, 16)
        
        #check to see if min is greater than max
        if min_int > max_int:
            tmp = min_int
            min_int = max_int
            max_int = tmp
        
        #loop through registers
        for i in range(min_int, max_int + 1):
            word = command + ' ' + hex(i) +  num_bytes + '?'
            nic_response = self.write_get(word)['response']
            self.log.info(nic_response)
            out_str.append(nic_response['command'])
            out_str.append(' : ')
            
            #check to make sure we get a response
            if nic_response['response']:                
                out_str.append(nic_response['response'])
            else: #if not, append the status
                out_str.append(nic_response['status'])
            out_str.append('\n')    
            self.log(out_str)
        return ''.join(out_str)
        

    def get_mac_address(self):
        #returns the MAC address
        tmp = self.write_get('atflxa 0x30000 8?')
        #print tmp
        if tmp['response'].count('0xFF') == 8: 
            return None
        else:
            self.log.debug('mac response : ' + str(tmp))
    
            #strip out the whitespace
            array3 = re.split(' ', tmp['response'])
            
            #popping last white space at end
            #array3.pop() 
            
            stuffed = []
            for unstuffed in array3 : # Loop for changing unpadded hex to zero-padded string of hex
                stuffed.append('%0.2X' % int(unstuffed,16))
            mac = ''.join(stuffed)
            return mac
    

    def set_mac_address(self, mac_address):
        #writes a mac address to flash. mac_address is a 16-character string represent
        self.mac = mac_address
        regex = r'(..)'
        replace_string = r"0x\1 "
        hex_values = re.sub(regex, replace_string, mac_address)
        hex_values = hex_values[:len(hex_values)-1]
        return self.write_set('atflxa 0x30000 8=' + hex_values)    
 

    def get_cpu_clock(self):
        #returns the cpu_clock address
        tmp = self.write_get('atflxa 0x30082 4?')
        #print tmp
        if tmp['response'].count('0xFF') == 4: 
            return None
        else:
            self.log.debug('cpu_clock response : ' + str(tmp))
    
            #strip out the whitespace
            array3 = re.split(' ', tmp['response'])
    
            stuffed = []
            for unstuffed in array3 : # Loop for changing unpadded hex to zero-padded string of hex
                stuffed.append('%0.2X' % int(unstuffed,16))
            cpu_clock = ''.join(stuffed)
            cpu_clock_int = str(int(cpu_clock,16))
            return cpu_clock_int
    

    def set_cpu_clock(self, cpu_clock):
        #writes a cpu_clock address to flash. cpu_clock is a 16-character string represent
        if cpu_clock == '26000000':
            return self.write_set('atflxa 0x30082 4=0x1 0x8c 0xba 0x80')
        elif cpu_clock == '19200000':
            return self.write_set('atflxa 0x30082 4=0x1 0x24 0xf8 0x00')
        

    def get_device_type(self):
        raw_part_number = self.write_get('atflxa 0x30008 1?')['response']
        if raw_part_number.count('0xFF') == 1: 
            return None
        else:
            return str(int(raw_part_number, 16))
    

    def set_device_type(self, device_type):
        self.device_type = str(device_type)
        return self.write_set('atflxa 0x30008 1=' + str(device_type))
    

    def get_stuffing_options(self):
        stuffing_options = self.write_get('atflxa 0x30030 8?')['response']
        if stuffing_options.count('0xFF') == 8: 
            return None
        else:
            return stuffing_options
        

    def get_rf_info(self):
        return self.write_get('at~rf?')['response']
        

    def set_stuffing_options(self, stuffing_options):
        #may have to fill in the blanks
        #print 'entered set stuffing options routine'
        #print stuffing_options
        split_stuff_options = re.split('\s', stuffing_options)
        #print split_stuff_options
        
        stuffing_options_set_string = ''
        for i in range(8):
            if i< len(split_stuff_options):
                stuffing_options_set_string += split_stuff_options[i]
            else:
                stuffing_options_set_string += '0'
            
            if i < 7:
                stuffing_options_set_string += ' '
                
        #print [stuffing_options_set_string]    
        
        return self.write_set('atflxa 0x30030 8=' + stuffing_options_set_string)
     

    def get_running_firmware(self):
        #returns current firmware in use
        #looks at a pointer to the running firmware
        #going to have to try two different address, for firmware.
        #running firmware pointer location depends on memory size
        #https://zoo.silverspringnet.com/display/FwEng/Flash+Layout+16MB
        #for 2/4/8MB flash, running firmware pointer is at 0x4008
        #for 16MB flash, running firmware pointer is at 0x20008
        
        #sometimes takes longer to respond than usual so added extra read wait - jhowarth 27/9/11
        #going to check 0x20008 first because it is most likely to be an unprogrammed bit of memory if 
        #2/4/8MB flash because sysvars shouldn't fill up that location
        for address in ['0x4e0108', '0x4008']:
            tmp = self.write_get('atflxa '+ address +' 4?', extra_read_time_ms=400)
            
            #we want to check to see if all 0xFF (unprogrammed flash)
            if tmp['response'].count('0xFF') != 4:
                break #we have some data!
            
        #deals with completely failing for both firmware locations    
        if tmp['response'].count('0xFF') == 4:
            return None
        
        #now parse the firmware and make sense of it
        array3 = re.split(' ', tmp['response'])

        stuffed = []
        for i in range(len(array3)):
            # Loop for changing unpadded hex to zero-padded string of hex
            stuffed.append('%0.2X' % int(array3[i],16))
            if i < 2:
                stuffed.append('.')

        firmware = ''.join(stuffed) 
        return firmware        


    def get_raw_register_from_flash(self, reg_offset, reg_length):
        #reg_offset is in hex e.g. 0x3000D
        #reg_length is the integer length of bytes
        
        #returns arena product number
        tmp = self.write_get('atflxa ' + str(reg_offset) + ' ' + str(reg_length) + '?', extra_read_time_ms=200)
        
        #strip out the whitespace
        array3 = re.split(' ', tmp['response'])
        
        #popping last white space at end
        #array3.pop() 
        
        #print 'array 3 is'
        #print array3
        '''
        PN_string = []
        for i in array3:
            PN_string.append(chr(int(i, 16)))
        '''
        return array3
        

    def get_part_number(self):
        
        #there are two methods of storing the arena part number in memory that I know of
        #10 charcacters e.g. 174-000191 rev 5 is stored as a continuos block in 0x3000D
        #11 charcters e.g. 174-0242-01 rev 02 is stored in 0x3000D (7 bytes), 0x30043 (4 bytes)
        
        #assuming that the arena PN has been programmed as this is check on initial connection.
               
        raw_part_number = self.write_get('atflxa 0x3000D 10?', extra_read_time_ms=2000)['response']
        #print raw_part_number
        if raw_part_number.count('0xFF') == 3: 
            #this location hasn't been programmend, then it's going to be the new method
            #so easiest way is to get these two bytes again
            first_place = self.write_get('atflxa 0x3000D 7?')['response']
            second_place = self.write_get('atflxa 0x30042 4?')['response']
            raw_part_number = first_place + ' ' + second_place
        
        #now need to return none if raw_part_number is full of f's going to be 10 or ll bytes, so > 9
        #print [raw_part_number]
        if raw_part_number.count('0xFF') >9: 
            return None
        else:
        
            #convert array to string
            split_raw_part_number = re.split(' ', raw_part_number)
            part_number_string = []
            for i in split_raw_part_number:
                part_number_string.append(chr(int(i, 16)))
            
            #now to add dashes and 'r'
            if len(part_number_string) == 10:
                #old part numbering method
                part_number_string.insert(3,'-')
                part_number_string.insert(10,'r')
                
            else: #going to assume it is the new string of length 10
                #new arena part number scheme 
                part_number_string.insert(3,'-')
                part_number_string.insert(8,'-')
                part_number_string.insert(11,'r')
            
            return ''.join(part_number_string)
    

    def set_part_number(self, part_number_string):
        #input arena pn as string you see it on the board
        #e.g. '174-000191r5' (12 characters) or '174-0263-00r1' (14 characters)
        self.log.debug('Entering set_part_number')
        self.part_number = part_number_string
        
        #check input - expecting 12 or 14 characters
        if len(part_number_string) not in (12,14):
            self.log.debug('Arena PN :'+ str(part_number_string)+ ' : is incorrect length. Length: '+ str(len(part_number_string)))
            return 'Error - invalid string length'
        
        self.log.debug('Arena PN is correct length')        
        #remove '-' and 'r' in input string
        for char in part_number_string:
            if char in "-r":
                part_number_string = part_number_string.replace(char,'')
        
        #now the part_number_string could be 10 or 11 characters
        #depending on length, we need to put the data in different memory locations, but we still         
        if len(part_number_string) == 10:
            command = 'atflxa 0x3000D 10='
            for i in range(10):
                command = command + str(hex(ord(part_number_string[:1]))) + ' ' 
                part_number_string = part_number_string[1:]
            command = command[:-1]# to pop off the last bit of whitespace      
            self.log.debug('Command is : ' + command)
            self.write_set(command)
        
        elif len(part_number_string) == 11:
            command = 'atflxa 0x3000D 7='
            for i in range(7):
                command = command + str(hex(ord(part_number_string[:1]))) + ' ' 
                part_number_string = part_number_string[1:]
            command = command[:-1]# to pop off the last bit of whitespace       
            self.log.debug('Command is : ' + command)
            self.write_set(command)
               
            command = 'atflxa 0x30042 2='
            for i in range(2):
                command = command + str(hex(ord(part_number_string[:1]))) + ' ' 
                part_number_string = part_number_string[1:]
            command = command[:-1]# to pop off the last bit of whitespace
            self.log.debug('Command is : ' + command)
            self.write_set(command)
            
            command = 'atflxa 0x30044 2='
            for i in range(2):
                command = command + str(hex(ord(part_number_string[:1]))) + ' ' 
                part_number_string = part_number_string[1:]
            command = command[:-1]# to pop off the last bit of whitespace
            self.log.debug('Command is : ' + command)
            self.write_set(command)    
        
        return 'Ok'
        

    def get_hardware_version(self):
        tmp = self.write_get('atflxa 0x30009 2?')
        if tmp['response'].count('0xFF') == 2: 
            return None
        else:
            #strip out the whitespace
            array3 = re.split(' ', tmp['response'])
            hw_type = str(int(array3[1], 16)) + '.' + str(int(array3[0], 16)) 
            return hw_type


    def set_hardware_version(self, hardware_version_sting):
        #hardware version as a dotted decimal sting, e.g. '17.1'
        #assumes either a 2/4 length sting e.g. '17.1' or '14'
        #hardware version is stored in firmare as 0x01 0x11 for 17.1
        self.hardware_version = hardware_version_sting
        
        command = 'atflxa 0x30009 2='
        
        #strings can either be 2 or 4 in length
        if len(hardware_version_sting) == 2:
            #no decimal place is there
            command = command + '0x00' + ' ' + hex(int(hardware_version_sting))
        else:
            #decimal place is there
            split_input = re.split('\.', hardware_version_sting)
            command = command + hex(int(split_input[1])) + ' ' + hex(int(split_input[0]))
        
        return self.write_set(command)
    

    def get_disease_name_and_voltage(self):
        """
        Tries to determine disease name of nic based on self.nic_data
        Need to have hardware version in self.nic_data dictionary before can run this.
        Doesn't return anything.
        Also determines voltage.
        """
        self.log.debug('Entering get_disease_name()')
        self.log.debug('nic_data:' + str(self.nic_data))
        
        try:
            hardware_version = int(float(self.nic_data['hardware_version']))
            #for now assume only one entry per hardware_version (deal with later)
            disease_name_voltage_architecture_list = nic_lookup_table.get(hardware_version)
        except:
            self.log.critical("\n\n                   Can not determine nic type, exiting.......   ")
            self.log.critical('self.nic_data is: ')
            self.log.critical(str(self.nic_data))
            exit()
        
        if len(disease_name_voltage_architecture_list) == 1:
            disease_name_voltage_architecture = disease_name_voltage_architecture_list[0]
        else:
            #need to work out which one is correct from architecture
            if disease_name_voltage_architecture_list[0]['architecture'] == self.nic_data['architecture']:
                disease_name_voltage_architecture = disease_name_voltage_architecture_list[0]
            else:
                disease_name_voltage_architecture = disease_name_voltage_architecture_list[1]
        
        #only get voltage and disease name if they havne't been passed in
        if self.nic_data['disease_name'] is None:    
            self.nic_data['disease_name'] = disease_name_voltage_architecture['name']
        if self.nic_data['voltage'] is None: 
            self.nic_data['voltage'] = disease_name_voltage_architecture['voltage']
        

    def get_frame_length(self):
        return self.write_get('ats100?')['response']
    

    def set_frame_length(self, value):
        return self.write_set(['ats100=', str(value)])        
    

    def get_number_frames(self):
        return self.write_get('ats101?')['response']


    def set_number_frames(self, value):
        return self.write_set(['ats101=', str(value)])
    

    def get_frame_gap(self):
        return self.write_get('ats102?')['response']
    

    def set_frame_gap(self, value):
        return self.write_set(['ats102=', str(value)])
    

    def set_tx_pattern_start(self, value):
        return self.write_set(['ats103=', str(value)])
    

    def get_tx_pattern_start(self):
        return self.write_get('ats103?')['response']
    

    def get_tx_pattern_end(self):
        return self.write_get('ats104?')['response']
    

    def get_tx_pattern_step(self):
        return self.write_get('ats105?')['response']
    

    def set_tx_mode(self, mode):
        return self.write_set(['ats106=', str(mode)])
    

    def get_tx_mode(self):
        return self.write_get('ats106?')['response']
    

    def set_channel(self, channel):
        return self.write_set(['ats107=', str(channel)])


    def get_channel(self):
        #returns the channel number 
        return self.write_get('ats107?')['response']
      

    def set_preamble_char(self, preamble):
        return self.write_set('ats108=' + str(preamble))
    

    def get_preamble_char(self):
        return self.write_get('ats108?')['response']
    

    def set_preamble_length(self, preamble_length):
        return self.write_set('ats109=' + str(preamble_length))
    

    def get_preamble_length(self):
        return self.write_get('ats109?')['response']
    

    def set_channel_id(self, channel):
        return self.write_set('ats110=' + channel)
    

    def get_channel_id(self):
        return self.write_get('ats110?')['response']
        

    def set_modulation(self, modulation):
        #Accepts input of FSK,GFSK,OFDM,QPSK types.
        if modulation == 'FSK':
            mod = 0
        elif modulation == 'GFSK':
            mod = 1
        elif modulation == 'OFDM':
            mod = 3
        elif modulation == 'QPSK':
            mod = 4     
        #return self.write_set(['ats111=', str(mod)]) 
    

    def set_option(self,option):
        if option == 1:
            opt=1094
        elif option ==2:
            opt=552
        elif option == 3:
            opt=281        
        elif option == 4:
            opt=156
        #return self.write_set(['ats131=',str(opt)])  
         

    def set_phy_mode(self,phy_mode):
        s = self.write_set(['ats121=', str(phy_mode)])
        #self.write('attest=1')
       # self.write('attest=0')
        return s   
          

    def get_modulation(self):
        return self.write_get('ats111?')['response']
        

    def set_power_level(self, level):
        return self.write_set(['ats112=', str(level)])
    

    def get_power_level(self):
        return self.write_get('ats112?')['response']
    

    def set_channel_spacing(self, spacing):
        s = self.write_set(['ats113=', str(spacing)])
        self.channel_spacing = self.get_channel_spacing()   # set an instance variable to avoid having to do a serial read
        return s
    

    def get_channel_spacing(self):
        return float(self.write_get('ats113?')['response'])#*1000 this has to be fixed sergio #to put in Hz
        

    def set_datarate(self, rate_in_bps):
        #input is rate in bps
        #because we used to set datarate in kbps not bps
        if int(self.nic_data['running_firmware'][:2]) < 83:
            rate_in_bps = rate_in_bps
        return_status = self.write_set(['ats114=', str(rate_in_bps)])
     
        #now need to also set frequency deviation as this is no longer changed in custom phy modes
        if int(rate_in_bps) in list(frequency_deviation_table.keys()):
            #self.set_frequency_deviation(frequency_deviation_table[int(rate_in_bps)])
            pass
        #now need to set preamble length as well in custom phy modes
        if int(rate_in_bps) in list(preamble_length_table.keys()):
            
            #self.set_preamble_length(preamble_length_table[int(rate_in_bps)])
            pass
        return return_status 
        

    def get_datarate(self):
        return self.write_get('ats114?')['response']
    

    def get_rf_xcvr(self):
        return self.write_get('ats115?')['response']    


    def set_sysvar(self, sysvar, value):
        self.write_set('atsysvar %d 1=%d' % (sysvar, value))
    

    def get_sysvar(self, sysvar):
        return self.write_get('atsysvar %d?' % sysvar)['response']


    def disable_overtemp_patch(self):
        self.set_sysvar(775, 1)
        

    def get_all(self):
        out_data = []
        for i in range(100, 119, 1):
            word = 'ats' + str(i) + '?'
            out_data.append([word , self.write_get(word)['response']])
        #print out_data
        out_data.append(['firmware', self.get_firmware(self.running_firmware_pointer)])
        out_data.append(['start word', self.get_start_word()])
        return out_data
    

    def set_start_word(self, start_word):
        return self.write_set(['ats117=', str(start_word)])        
        

    def get_start_word(self):
        return self.write_get('atmfe 17?')['response']
    

    def set_itron_serial_number(self, serial):
        # for communicating with Itron NICs(newer fw ~3.1.x)
        self.write_set('ats119=' + str(serial))
    

    def idle(self):
        if self.cell_status in ('idle', 'transmitting'):
            self.write_set('atwan--') #make sure we are disconnected from cell modem
        return self.write_set('attest=0')
    

    def transmit(self):
        self.time_of_last_transmit = time.time()
        #self.write_set('attest=0')       # do we still need this?
        if self.attest_mode == 'normal':        
#            self.write_set('attest=15')\
            #self.write_set('atmx 0x212=0x80')
            #self.write_set('atmx 0x212?')
            return self.write_set('attest=1')
        elif self.attest_mode == 'slc':
            return self.write_set('attest=6')
        

    def transmit_dual(self):
        self.time_of_last_transmit = time.time()
        return self.write_set('attest=13')


    def set_cell_status(self, status):
        if status in ('off', 'idle', 'transmitting'):
            self.cell_status=status
            self.log.info('Cell status set to: ' + status + '.')
        else:
            self.log.warning('Cell status: ' + ' , not recognized.')


    def activate_cell_mode(self, mode):
        if mode == 'transmitting':
            self.write_set('AT+WPOW=1,128,5', extra_read_time_ms=1000) #$2C maps to ',' as a string
        elif mode == 'idle':
            self.write_set('AT+WPOW=2', extra_read_time_ms=1000)


    def receive(self):
        #self.write_set('attest=0')    # do we still need this?
        if self.attest_mode == 'normal':  
            self.write_set('atxy')
            #self.write_set('atmx 0x212=0x80')
            #self.write_set('atmx 0x212?')      
            return self.write_set('attest=2')
        elif self.attest_mode == 'slc':
            return self.write_set('attest=9')
        
        if self.cell_status != 'off':
            self.write_set('atwan##', extra_read_time_ms=5000) #needs a long time to initialize
            if self.cell_status == 'transmitting':
                self.activate_cell_mode(self.cell_status)
            elif self.cell_status == 'idle':
                self.activate_cell_mode(self.cell_status)
       

    def begin_memory_torture(self, memory_type):
        """Start a memory torture test
        memory_type can be 'psram', 'sram', or 'flash'.
        'flash' test can destroy flash.
        Note you must continually read the buffer after issuing this command
        to obtain the results.
        Test does not stop until power cycle."""
        self.write('atorture=%s' % (memory_type))


    def ddr_memory_torture(self, memory_type):
        """Start a memory torture test
        memory_type can be 'psram', 'sram', or 'flash'.
        'flash' test can destroy flash.
        Note you must continually read the buffer after issuing this command
        to obtain the results.
        Test does not stop until power cycle."""
        if memory_type == 'ddr-k:0x40a00000:0x40c00000:2:0:100':
            print("slow test wait 25secs")
            return self.write_get('atorture=%s' % (memory_type),25000)
        elif memory_type == 'ddr-k:0x40a00000:0x40c00000:5:0:100':
            print("slow test wait 25secs")
            return self.write_get('atorture=%s' % (memory_type),25000)
        elif memory_type == 'ddr-k:0x40a00000:0x40c00000:3:0:100':
            print("slow test wait 10secs")
            return self.write_get('atorture=%s' % (memory_type),12000)        
        else:
            print("test wait 6secs")
            return self.write_get('atorture=%s' % (memory_type),6000)
        
       
        


    def get_phy_stats(self):
        return self.write_get('at~phy?')['response']
    
    def reset_phy_stats(self):
        return self.write_set('at~phy=0')
        
    def parse_phy_stats(self, phy_stats, value):
        #sometimes you just want to parse the statsf
        #as each communication with the nic may take 0.2 seconds
        #returns the value associated with the string
        line = re.findall('[\+|\-]*[0-9]+.*' + value, phy_stats)
        #return int(re.findall('[\+|\-]*[0-9]+', line[0])[0])     
        integer_string =  re.findall('[\+|\-]*[0-9]+[\+|\-]*', line[0]) #to get last one in one case
        #print integer_string
        if (integer_string[0][-1]=='+') or (integer_string[0][-1]=='-'):
            #need to put sign at front so take it off the back and put it on the front
            fixed_integer_string = integer_string[0][-1] + integer_string[0][0:len(integer_string[0])-1]
        else:
            fixed_integer_string = integer_string[0]
        #print fixed_integer_string
        return int(fixed_integer_string)   
    
    def get_phy_value(self, value):
        ##get the stat associated with the value
        phy_stats = self.get_phy_stats()
        return self.parse_phy_stats(phy_stats, value)    
        
    def get_frames_transmitted(self):
        return self.get_phy_value('frames transmitted')
    
    def get_received_frames(self):
        #returns the value as an integer
        return self.get_phy_value('received frames')        
    
    def get_crypto_key(self, key_number):
        return self.write_get('atcrypto ECCK' + str(key_number) + ' MUL?')['response']
    
    def set_country_code(self, country_code):
        self.write('atcc=' + str(country_code))
    
    def get_country_code(self):
        return self.write_get('atcc?')['response']
    
    def set_dac0(self, dac0_setting):
        self.write_set('atdac0=' + str(dac0_setting))
    
    def get_dac0(self):
        return self.write_get('atdac0?')['respnose']
    
    def get_frequency_zero(self):
        return self.write_get('ats123?')['response']
    
    def set_frequency_zero(self, frequency_zero):
        return self.write_set('ats123='+ str(frequency_zero))
       
    
    def power_cycle(self):
        ### Default value for wait after it power cycles is 5 seconds
        hardware_version = int(float(self.nic_data['hardware_version']))
        if hardware_version == 24:
            waiting_time=22
        else:
            waiting_time=10
        
        if self.power_supply is None:
            self.log.info('No power supply connected to nic, power-cycle manually') 
            self.write_set('atrestart')
            self.time_of_power_cycle = time.time()
            time.sleep(waiting_time)#wait for device to wakeup  
        else:
            if  self.power_supply.power_supply.__class__.__name__ ==  'DummyPinSupply':
                self.write_set('atrestart') 
                time.sleep(waiting_time)#wait for device to wakeup                 
            self.log.info('Power-cycling NIC: ' + self.name)
            self.power_supply.power_cycle()
            self.time_of_power_cycle = time.time()
            time.sleep(waiting_time)#wait for device to wakeup
        self.communications_check()        ### Default value for wait after it power cycles is 5 seconds
    
    def set_frequency_deviation(self, deviation):
        return self.write_set('ats130='+ str(deviation))
    
    def get_frequency_deviation(self):
        return self.write_get('ats130?')['response']
        
    def set_atmx_register(self, register, value, value_base=16, value_length_in_bits=8, offset=0, register_length_in_bits=8):    
    #writes to ATMX register and then commits to BBRAM
    #register is a hex string, otherwise all inputs are in integers
    #offset is where the value starts, i.e. offset '7' is 8th bit in bit-sequence
        if register_length_in_bits == value_length_in_bits:
            new_register_setting = int(value, value_base)
        else:
            #get current register setting
            command = 'atmx ' + str(register) + '?'
            reg_initial_setting = int(self.write_get(command)['response'], 16)#converts to hex
            
            #mask out the current values from that offset
            #three steps to this algorithm
            bitmask = (2**register_length_in_bits - 1)
            bitmask = bitmask - (2**(offset + value_length_in_bits) -1)
            bitmask = bitmask + 2**offset - 1       
            
            #get masked value of register so can load new-setting in
            masked_value = reg_initial_setting & bitmask
            
            #shift new-value to where it should be
            new_value = int(value, value_base) << offset
            
            #add new value to masked value to get full register setting
            new_register_setting = masked_value | new_value

        #convert the new value to hex
        hex_new_register_setting = hex(new_register_setting)
        hex_new_register_setting = hex_new_register_setting.strip('L')
        
        #write in the new register value
        command = 'atmx ' + str(register) + '=' + hex_new_register_setting     
        self.write_set(command)
        
        #commit the write to bbram
        return self.write_set('atbbram')    
    
    def set_antenna(self, antenna_status):     
        """antenna is either 'external' or 'internal'
        For firmware >= 2.12, we have the atant command for all devices.
        Before firmware 2.12, have to use atmemw commands.
        See https://zoo.silverspringnet.com/display/FwEng/AT+commands+for+Akio+SOC#ATcommandsforAkioSOC-ATcommandsforsettingexternalantenna%28PriortoFW2.12%29 """
       
        #work out if have to use atmemw commands if firmware < 82.12.xxxx
#        if int(self.nic_data['running_firmware'][:2]) < 83 and int(self.nic_data['running_firmware'][3:5])<12:
#            use_atmemw = True
#        else:
#            use_atmemw = False
                
        if antenna_status == 'external':
#            if use_atmemw:
#                if self.nic_data['disease_name'] == 'WestNile_Zoonosis':
#                    #sets for 900MHz
#                    self.write_set("atmemw 0xefffa010 1=0x4000")
#                    self.write_set("atmemw 0xefffa01C 1=0x4000")
#                else:
#                    self.log.error('Please define atmemw commands for ' + self.nic_data['disease_name'])
#            else:
                self.write_set('atant=3')
                
        elif antenna_status == 'internal':
#            if use_atmemw:
#                if self.nic_data['disease_name'] == 'WestNile_Zoonosis':
#                    #sets for 900MHz
#                    self.write_set("atmemw 0xefffa010 1=0x4000")
#                    self.write_set("atmemw 0xefffa018 1=0x4000 ")
#                else:
#                    self.log.error('Please define atmemw commands for ' + self.nic_data['disease_name'])
#            else:
                self.write_set('atant=0')
   
    def initialize(self):
        self.log.info('Initializing NIC: ' + self.name)
        self.write_set('atv2')
        self.write_set('atstuff 8=' + self.nic_data['stuffing_options'])       
        wan_type = self.get_wan_type()
#         if wan_type == 'NAG':#is a cellbrea
#             self.write_set('atwan=0x25') # for Gen5 it is same as 2G
# #            self.write_set('atwan=0x20') #will take 10seconds to respond
#         elif wan_type == 'NA1':#is a cellbrea
#             self.write_set('atwan=0x24') #will take 10seconds to respond
#         elif wan_type == 'SV1':#is a cellbrea
#             self.write_set('atwan=0x26') #will take 10seconds to respond 
#             
        self.write_set(('ath=' + str(self.nic_data['hardware_version'])))
        self.write_set('atx0')
        
#        self.write_set('ats120=0xff')
#        if self.phy_mode:
#            self.write_set('ats121=' + str(self.phy_mode))
#        else:
#            self.write_set('ats121=0xff') #for custom phy-mode
        
        # required sometimes when transmitting 2.4HAN
#        self.set_tx_pattern_start(255)

        if self.attest_mode=='slc':
            self.write_set('ats118=4')
    
        if self.antenna:
             self.set_antenna(self.antenna)
        
        if self.country_code:
            self.set_country_code(self.country_code)
        #for custom setup functions
       # self.write_set('ats123=865100000')
#        self.write_set('atmx 0x12d=0x4e') #disable temp patch
#        self.write_set('atmx 0x12e=0x20')
        
#         if self.get_wan_type() == 'NAG':#is a cellbrea
#             print" Enter 2G to enter atwan##"
#             self.write_set('atwan##') #will take 10seconds to respond
#             time.sleep(25)#wait for xcvr to initialize
#             self.write_set('atwan--') #will take 10seconds to respond
#             
        
    def _initialize_863MHz(self):
        self.write_set('atx0')
        #self.write_set('atx3') #5/27/2015 Jason King: Doing both atx0 and atx3 is causing issues on first transmission. Include again later.
        time.sleep(3)#wait for xcvr to initialize
        self.write_set('ats115=0')
        self.write_set('atDAC0=750')
        self.write_set('ats112=15')
        self.write('ats123=863100000')  
        
    def _initialize_865MHz(self):
        self.write_set('atx0')
        #self.write_set('atx3') #5/27/2015 Jason King: Doing both atx0 and atx3 is causing issues on first transmission. Include again later.
        time.sleep(3)#wait for xcvr to initialize
        self.write_set('ats115=0')
        self.write_set('atDAC0=750')
        self.write_set('ats112=15')
        self.write('ats123=865100000')
        
    def _initialize_870mhz_fhss(self):
        self._initialize_900MHz()
        
    def _initialize_870MHz(self):
        self.write_set('atx0')
        #self.write_set('atx3') #5/27/2015 Jason King: Doing both atx0 and atx3 is causing issues on first transmission. Include again later.
        time.sleep(3)#wait for xcvr to initialize
        self.write_set('ats115=0')
        self.write_set('atDAC0=750')
        self.write_set('ats112=15')
        self.write('ats123=870200000')
        
    def _initialize_900mhz_fhss(self):
        self.write_set('atx0')
        time.sleep(3)#wait for xcvr to initialize
        self.write_set('ats115=0')
        self.write_set('ats112=25')   # different range for GEn5: 0-30
        
        

        #self.write_set('ats102=1') #hack for uber
    def _initialize_900MHz(self):
        self.write_set('atx0')
        #self.write_set('atx3') #5/27/2015 Jason King: Doing both atx0 and atx3 is causing issues on first transmission. Include again later.
        time.sleep(3)#wait for xcvr to initialize
        self.write_set('ats115=0')
        self.write_set('atDAC0=750')
        self.write_set('ats112=15')#change this back
        #self.set_frequency_zero(self.frequency_zero)
#        self.write_set('atorture=ddr-s:50:0:6:9')
#         self.write_set('atdmac0 0x40000000:0x40900000:8:0x2000')
#         self.write_set('atdmac1 0x40000000:0x40903000:16:0x3000')
#         self.write_set('atdmac1 0x40000000:0x40800000:32:0x5000')

        
        
        
    def _initialize_2400MHz(self):
        #self.write_set('atx0')
        self.write_set('atx3')
        time.sleep(3)#wait for xcvr to initialize
        self.write_set('ats115=3') 
        self.write_set('ats112=15')
        
             
    def _initialize_2400mhz_fhss(self):
        self.write_set('atx0')
        self.write_set('atx3')
        time.sleep(2)#wait for xcvr to initialize
        self.write_set('ats115=3')
        self.write_set('ats112=15')
   
                                   
    def _initialize_2400mhz_han(self):
        # NOTE: the below hack is commented out. New board hardware should
        # have fixed this problem. If this problem is found(low transmit on 2.4),
        # file a Jira ticket. /NOTE
        # hack to get around hardware issue on some 'Brea boards with old firmware
        #self._initialize_2400mhz_fhss()
        #self.transmit()
        #time.sleep(1)
        #self.idle()
        # end hack
        #=======================================================================
        # if self.nic_data['disease_name'] in ['WestNile_Zoonosis', 'Hendra', 'Nipah']:
        #     # 2.4 is initialized slightly differently on WestNile/Zoonosis
        #     self.write_set('atx0')
        #     self.write_set('atx1')
        #     time.sleep(2)    #wait for xcvr to initialize
        #     self.write_set('ats115=1')
        #     self.write_set('ats112=0')      # 0 is highest level on 2.4HAN WestNile
        # else:
        #=======================================================================
        self.write_set('atx0')
        self.write_set('atx3')  #atx1 no longer works
        time.sleep(2)#wait for xcvr to initialize
        self.write_set('ats115=1')
        self.write_set('ats112=15')
        self.set_frame_length(10) #if packet size is too large then won't transmit - not even CW.    
        self.set_channel(18) #need to set the channel to something between 11 and 26.
        #=======================================================================
        # if self.antenna == 'external':
        #     self.set_antenna('external')
        #     self.write_set('atant=3')
        #=======================================================================
            
    def _initialize_dual(self):
        #900MHz Init
        self.write_set('atx3')
#        time.sleep(3)#wait for xcvr to initialize
        self.write_set('ats115=0')
        self.write_set('ats121=21')
        self.write_set('ats112=22')
        self.write_set('ats106=5')

        #2400MHz Init
        self.write_set('ats115=3')
        self.write_set('ats121=1')
        self.write_set('ats112=20')
        self.write_set('ats106=5')
       
        #Switch Back to 900MHz radio for remainder of test.
        self.write_set('ats115=0')
        self.write_set('ats121=21')
        self.write_set('ats106=8')
                             
    def set_mode(self, mode):
        if mode == '863MHz':
            self._initialize_863MHz()
        elif mode == '865MHz':
            self._initialize_865MHz()
        elif mode == '870MHz':
            self._initialize_870MHz()
        elif mode == '870MESH':
            self._initialize_870mhz_fhss()
        elif mode == '900MESH':
            self._initialize_900mhz_fhss()
        elif mode == '900MHz':
            self._initialize_900MHz()  
           # self.set_frequency_zero(self.frequency_zero)         
        elif mode == '2400MESH':
            self._initialize_2400mhz_fhss()    
        elif mode == '2400HAN':
            self._initialize_2400mhz_han()
        elif mode == '2400MHz':
            self._initialize_2400MHz()
        elif mode == 'Dual':
            self._initialize_dual() 
        else:
            self.log.critical('Invalid mode: %s' % (mode))
            raise Exception('Invalid mode: %s' % (mode))
#        self.set_channel_spacing(DEFAULT_CHANNEL_SPACING[mode])
        if self.frequency_zero:
            self.set_frequency_zero(self.frequency_zero)               
        
        if self.custom_initialization_commands:
            for command in self.custom_initialization_commands:
                self.write_set(command)

    def initialize_dual_running(self, high_band_channel, high_band_channel_spacing, high_band_power_level, high_band_mode, high_band_datarate, high_band_modulation, high_band_phy_mode):
        #init
        if high_band_modulation == 'FSK':
            mod = 0
        elif high_band_modulation == 'GFSK':
            mod = 1
        elif high_band_modulation == 'OFDM':
            mod = 3
        elif high_band_modulation == 'QPSK':
            mod = 4
        
        #900MHz Init
#        self.write_set('atx3')
#        time.sleep(3) #wait for xcvr to initialize
#        self.write_set('ats115=0')
#        self.write_set('atDAC0=750')
#        self.write_set('ats121=21')
#        self.write_set('ats112=22')
#        self.write_set('ats106=8')
        print(self.get_rf_info())
        #2400MHz Init
        high_band_mode
        self.write_set('ats115=3')
        self.write_set('ats112='+str(high_band_power_level))
        self.write_set('ats113='+str(high_band_channel_spacing))
        self.write_set('ats107='+str(high_band_channel))

        
        #Switch Back to 900MHz radio for remainder of test.
        self.write_set('ats115=0')
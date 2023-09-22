## test_transmit_power.py is a child class of test.py which specifies the specfic test to run
# requires a dut = type(Radio)

from test import Test
from testparams import TestParams
from station import Station, StationTestEquipment
import test_equipment
from util.logger import Log
from result import TxPwrResult
from typing import List
from radio import Radio
import time


class TransmitPower(Test):
    """ Test plan available at https://confluence.itron.com/display/HW/Transmit+Power+EVT+Test+Procedure 
    
    """
    def __init__(self, testparams: TestParams, station: Station, duts: List(Radio), log: Log): # allow for multi-dut <-- SHOULD ALSO VALIDATE IF VOLTAGES TO HIGH FOR DUT, AND IF STATION COMPATIBLE
        super().__init__(testparams, station, duts, log)


    def _validate_station_equipment(self) -> bool:
        """ Checks station equipment against required equipment for test """
        pass


    def _validate_testparams_for_device_compatibility(self):
        """ Check to see that testparams aren't outside of safe limits for device """
        pass


    def calculate_runtime(self):
        """ Useful testrun statistic """
        pass


    def _single(self, dut, read_frequency_counter=True):
        """ Runs a single power level transmit and returns measurements """
        expected_frequency = self.get_current_channel_freq(dut)
        
        dut.transmit()
        
        time.sleep(0.1)
        
        current_draw = self.station.power_supply.get_current()
        
        output_power = self.station.power_meter.read_peak_power_level()

        if read_frequency_counter:
            if float(output_power) >= 20.0:
                frequency = self.station.frequency_counter.read_frequency(
                                                                           freq_range_hz = expected_frequency,
                                                                           average_samples = FREQUENCY_COUNTER_AVERAGE_SAMPLES
                                                                           )
                #frequency = self.station.frequency_counter.read_frequency(BASE_FREQUENCY[self.modes.current]*1000)
                # should test for unusually high PPM here
            else:
                frequency = '0'
                self.log.warning("Frequency was not read because output power < 20dBm")
        else:
            frequency = '0'

        #frequency = self.get_current_channel_freq(dut)
        dut.idle()
        time.sleep(0.1)
        
        return {'output_power_dbm' : output_power, 'current_draw_amps' : current_draw, 'frequency_hz' : frequency} 


    def _sweep(self):
        """ Runs multiple power levels """
        frequency_readings = 0      # count frequency readings
        old_current_reading = None
        
        expected_frequency = self.get_current_channel_freq(dut)
        
        # calibrate frequency counter and power meter to expected frequency
        self.test_lab.frequency_counter.set_expected_frequency(expected_frequency)
        self.test_lab.power_meter.set_frequency(expected_frequency)
        #sweep through the dac0_settings and power levels
        for dac0_setting in self.dac0_settings:
            if dac0_setting:
                dut.set_dac0(dac0_setting)
                self.log.info('DAC0 setting is: ' + str(dac0_setting))
            
            for level in self.power_levels:
                #self.do_watchdog_workaround(dut)
                print('======================================')
                
                self.log.info('Transmit power setting is: ' + str(level))
                #run single transmission
                dut.set_power_level(level)

                # Why??? <------------------------ AL 2-10-2023
                if frequency_readings < 2:
                    read_freq_cntr = True
                    frequency_readings += 1
                else:
                    read_freq_cntr = False
                    
                if self.calibrate:
                    self.log.info('Calibration run, devices set up, ready to calibrate.')
                    read_freq_cntr = False # do not use frequency counter
                    # self.test_lab.ref_attenuator.set_attenuation(0)
                    # sys.exit() # sets up dut to run calibrate_station()?
                          
                single_result = self.single(dut, read_freq_cntr=read_freq_cntr)
                
                #grab the current
                if old_current_reading:
                    if (((float(old_current_reading)- float(single_result['current_draw_amps'])) / float(old_current_reading)) > 0.50) :
                        self.log.info("Current deviates from last reading by > 50%. Retrying...")
                        single_result = self.single(dut, read_freq_cntr=read_freq_cntr)
                
                old_current_reading = single_result['current_draw_amps']
                            
                self.log.info('Measured power output is: ' + str(single_result['output_power_dbm']) + 'dBm')
                
                #add data to results object
                sweep_results.add('Channel', self.get_test_param('channel'))
                if self.dac0_settings != [None]: sweep_results.add('DAC0 Setting', dac0_setting)
                sweep_results.add('Power Level Setting', level)
                sweep_results.add('RF Power (dBM)', single_result['output_power_dbm'])
                sweep_results.add('Current Draw (A)', single_result['current_draw_amps'])
                sweep_results.add('Frequency (Hz)', single_result['frequency_hz'])
                
                #print run stats to screen
                #print line_data
                print('=======================================')
                
                # if we're getting negative power readings, break out of the loop
                # if float(single_result['output_power_dbm']) < 0:
                #     self.log.info('Output power is less than 0dBm, moving on to next channel.')
                #     break
        
        return sweep_results


    def run(self) -> List:
        """ Executes the test; Will return a record of Result objects for each dut """
        self._sweep()
        pass


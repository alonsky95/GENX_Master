from GENX_Master.test_equipment.test_equipment import TestEquipment
from GENX_Master.util.comm_visa import VisaComm
from GENX_Master.util.logger import Log
from GENX_Master.util.dummy_logger import DummyLogger
import time


class AgilentE4416A(TestEquipment):
    """Agilent E4416A Power Meter"""
    def __init__(self, log: Log, address): #<--- different interface from TestEquipment a violation of LSP?
        name='Agilent E4416A'
        comm = VisaComm(log, name, address)
        super().__init__(log, comm) # all object properties to be initialized in base class


    def set_cal_level(self, level):
        #sets the calibration level of the power meter. the calibration value should be used as "level"
        #prints the command that is sent to the power meters
        self._comm.write_set("Calc1:Gain " + str(level))
        return self._comm.write_set("Calc2:Gain " + str(level))
    

    def set_gates(self):
        ''' Setting up gates for more accurate OFDM measurements'''
        self._comm.write_set("*CLS")
        self._comm.write_set("*RST")
        self._comm.write_set("SENS:BW:VID HIGH")
        self._comm.write_set("SENS:SWE1:OFFS:TIME 0.000630")
        self._comm.write_set("SENS:SWE1:TIME 0.000383")
        self._comm.write_set("INIT:CONT ON")
        self._comm.write_set("TRIG:SOUR INT")
        self._comm.write_set("TRIG:LEV:AUTO OFF")
        self._comm.write_set("TRIG:LEV -30.00DBM")
        self._comm.write_set("TRIG:DEL -0.000500")
        self._comm.write_set("TRIG:HOLD 0.00001")
        self._comm.write_set("DISP:WIND1:TRACE:LOW -80")
        self._comm.write_set("DISP:WIND1:TRACE:UPP 30")        
        self._comm.write_set("SENS:TRAC:OFFS:TIME 0.0000103")
        self._comm.write_set("SENS:TRAC:TIME 0.008")
        self._comm.write_set("DISP:WIND1:FORM SNUM")
        self._comm.write_set("DISP:WIND2:FORM TRACE")
       

    def set_frequency(self, freq):
        # set frequency range to freq(in Hz)
        return self._comm.write_set("SENS1:FREQ " + str(freq))


    def read_peak_power_level(self):
        #polls the powermeter and reads the power level
        self._comm.write_set("INITiate:CONTinuous OFF")
        self._comm.write_set("INITiate:CONTinuous ON")
        time.sleep(.05)
        # polls the powermeter and reads the power level
        # returns the power level in ???
        return self._comm.write_get("FETC1?")


    def read_average_power_level(self):
        #polls the powermeter and reads the power level
        self._comm.write_set("INITiate:CONTinuous OFF")
        self._comm.write_set("INITiate:CONTinuous ON")
        time.sleep(.05)
        # polls the powermeter and reads the power level
        # returns the power level in ???
        return self._comm.write_get("FETC2?")
    

    def read_outputpower(self,channel):
        #polls the powermeter and reads the power level
        #returns the power level in ???
        return self._comm.write_get("FETC" +str(channel)+":POW:AC?")


    def read_trigger_count(self):
        return self._comm.write_get("TRIG:SEQ1:COUN?")


    def set_mrate_fast(self):
        # set measurement rate to fast(1000 reads/second)
        self._comm.write_set("SENS1:MRATE FAST")


    def set_mrate_normal(self):
        # set measurement rate to normal(20 reads/second)
        self._comm.write_set("SENS1:MRATE NORMAL")


    def get_mrate(self):
        # read measurement rate
        self._comm.write_get("SENS1:MRATE?")
        
    
if __name__ == '__main__':
    pwrmtr = AgilentE4416A(DummyLogger(), "GPIB0::13::INSTR")
    print(pwrmtr.read_peak_power_level())
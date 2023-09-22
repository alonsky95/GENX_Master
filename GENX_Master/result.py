## result.py is an concrete base class that specifies the Result dataclass to be used by test.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Header:
    test_station: str
    time_and_date: datetime
    run_type: str
    dut_mac: str
    dut_firmware: str
    dut_hw_vers: str
    dut_part_num: str
    dut_disease_name: str
    antenna: str # or bool?
    temperature: float
    datarate: int
    modulation: str
    tx_mode: int
    phy_mode: int
    voltage: float
    mode: int #?
    channel: int
    frequency: int
    country_code: int
    dac0_setting: int


@dataclass
class TxPwrData:
    channel: int
    power_level_setting: int
    rf_power: float
    current_draw: float
    frequency: int


@dataclass
class TxPwrResult:
    header: Header
    data: TxPwrData

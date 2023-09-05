from enum import Enum, auto
from GENX_Master.test_equipment.AgilentE4416A import AgilentE4416A
from GENX_Master.util.logger import Log
from GENX_Master.util.dummy_logger import DummyLogger
from dataclasses import dataclass

# class TestEquipmentType(Enum):
#     power_meter: auto()
#     power_supply: auto()
#     spectrum_analyzer: auto()
#     frequency_counter: auto()

### OLD FACTORY METHOD - tighly coupled to the names of the classes to be created
# for instrument_type, instrument_kwargs in instrument_dict.items():
#     instrument_kwargs['log']=self.log
#     instrument_string = 'test_equipment.%s(**instrument_kwargs)' % instrument_kwargs['make_model']
#     new_instrument = eval(instrument_string)
#     setattr(self, instrument_type, new_instrument)

@dataclass
class TestEquipmentConfig:
    test_equipment: str
    instrument_address: str
    make_model: str

class TestEquipmentFactory:
    @staticmethod
    def new_test_equipment(log: Log, config: TestEquipmentConfig):
        if config.make_model == 'AgilentE4416A':
            return AgilentE4416A(log, config.instrument_address)

        # elif config.make_model == 'AgilentE4416A':
        #     return AgilentE4416A(log, config.instrument_address)


if __name__ == '__main__':
    pwrmtr = TestEquipmentFactory.new_test_equipment(DummyLogger(), TestEquipmentConfig('power_meter', 'GPIB0::13::INSTR', 'AgilentE4416A'))
    print(pwrmtr.read_peak_power_level())
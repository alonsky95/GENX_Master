## testparam.py is an concrete base class that specifies the TestParams to be used by test.py
# I had an idea to make these map to the Query() object since results should contain a lot (if not all) of the same information

@dataclass
class TestParams:
    temperature: int
    voltage: int
    phy_mode: int
    # ...

@dataclass
class TxPwrTestParams(TestParams):
    power_level_settings: int
    
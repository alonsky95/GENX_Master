## result.py is an concrete base class that specifies the Result dataclass to be used by test.py

class Header:
    def __init__(self):
        pass

    def fn1(self):
        pass

class Data:
    pass

@dataclass
class TxPwrData(Result):
    header: Header

@dataclass
class Result:
    header: Header
    data: Data

@dataclass
class TxPwrResult:
    header: Header
    data: TxPwrData

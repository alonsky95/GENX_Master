## prion_mutt.py is a concrete class that specifies the Prion which implements the Nic interface
# this encapsulates the MUTTS commands to conform to the Nic interface
# nic has to be in FSU mode to talk over serial

from nic import Nic

class PrionMUTT(Nic):
    # could convert PrionMUTT to PrionFHSS by setting device type and sysvar
    pass
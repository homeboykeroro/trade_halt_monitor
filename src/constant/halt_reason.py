from enum import Enum

class HaltReason(str, Enum):
    T1 = 'Pending Material News',
    LULD = 'Volatility Halt'

    def has_key(key):
        return key in HaltReason.__members__
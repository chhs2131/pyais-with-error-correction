from enum import Enum


class NmeaType(Enum):
    NORMAL = 1
    MULTI = 2
    E_FORMAT_WITH_CHECKSUM = 3
    E_FORMAT = 4
    TOO_SHORT = 0

from enum import Enum


class NmeaType(Enum):
    NORMAL = 1
    MULTI = 2
    ONLY_PAYLOAD = 3

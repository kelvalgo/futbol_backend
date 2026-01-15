from enum import Enum

class PositionEnum(str, Enum):
    GK = "goalkeeper"
    DF = "defender"
    MF = "midfielder"
    FW = "forward"
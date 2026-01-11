from enum import Enum

class PositionEnum(str, Enum):
    GK = "Goalkeeper"
    DF = "Defender"
    MF = "Midfielder"
    FW = "Forward"
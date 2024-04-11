from enum import Enum

class StringSizeEnum(int, Enum):
    S = 10
    M = 25
    L = 100
    XL = 200
    XXL = 1000
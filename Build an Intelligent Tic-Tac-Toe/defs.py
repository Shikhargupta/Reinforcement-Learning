from enum import Enum

class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

class game_status_rc(AutoNumber):
    GAME_IN_PROGRESS = ()
    GAME_OVER = ()
    GAME_DRAW = ()

class players(Enum):
    PLAYER_X = -1
    PLAYER_O = 1

class params:
    LENGTH = 3

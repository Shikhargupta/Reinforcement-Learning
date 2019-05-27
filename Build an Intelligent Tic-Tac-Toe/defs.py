from enum import Enum, auto

class game_status_rc(Enum):
    GAME_IN_PROGRESS = auto()
    GAME_OVER = auto()

class win_rc(Enum):
    WINNER_IS_X = auto()
    WINNER_IS_O = auto()

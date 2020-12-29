from enum import Enum, auto


class MessageType(Enum):
    GAME_REQUEST = 1,
    GAME_REPLY = auto(),
    ORDER = auto(),
    GUESS = auto(),
    RESULT = auto(),
    ERROR = auto(),


MAGIC = 'BS1p'

from enum import Enum, IntEnum


class DBType(str, Enum):
    SQLITE = 'sqlite'


class ResponseCode(IntEnum):
    SUCCESS = 0
    ERROR = 1

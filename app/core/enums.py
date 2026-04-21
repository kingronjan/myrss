from enum import Enum, IntEnum


class DBType(str, Enum):
    SQLITE = 'sqlite'


class ResponseCode(IntEnum):
    SUCCESS = 0
    ERROR = 1


class TaskStatus(IntEnum):
    PENDING = 0
    RUNNING = 1
    SUCCESS = 2
    FAILED = 3
    UNSET = 4

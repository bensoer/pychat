from enum import Enum


class CommandType(Enum):
    GiveFirstMessage = 1,
    GetInitializationMessage = 2,
    Decrypt = 3,
    Encrypt = 4
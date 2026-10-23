import re

from enum import Enum
from error import EnumError

EnumBackTick = Enum("BackTick", ["Single", "Triple"])


pattern = re.compile(r"[^`]")


def backtick(buffer):

    match = pattern.search(buffer)

    if match is None:
        return -1, EnumError.Error

    if match.start() != 3:
        return 0, EnumBackTick.Single

    return 2, EnumBackTick.Triple

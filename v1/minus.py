import re

from enum import Enum

EnumMinus = Enum("Minus", ["Single", "Double", "Triple"])

pattern = re.compile(r"[^-]")


def minus(buffer):
    if len(buffer) >= 3 and buffer[:3] == "---":
        return 2, EnumMinus.Triple

    if len(buffer) >= 2 and buffer[:2] == "--":
        return 1, EnumMinus.Double

    return 0, EnumMinus.Single

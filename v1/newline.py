import re

from enum import Enum

EnumNewLine = Enum("NewLine", ["SingleNewLine", "MultipleNewLine"])

pattern = re.compile(r"[^\n]")


def newline(buffer):
    match = pattern.search(buffer)

    if match is None or match.start() == 1:
        return 0, None

    return match.start() - 1, EnumNewLine.MultipleNewLine

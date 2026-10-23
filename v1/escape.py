import re

from enum import Enum
from error import EnumError

EnumEscape = Enum(
    "Escape",
    [
        "Exclamation",
        "SquareOpen",
        "SquareClose",
        "AtSign",
        "Carrot",
        "Asterisk",
        "Plus",
        "Tilde",
        "Minus",
        "LineBreak",
    ],
)
chars_escape = ["!", "[", "]", "@", "^", "*", "+", "~", "-", "\\"]

chars_escape = "".join(chars_escape)

pattern = re.compile("[" + re.escape(chars_escape) + "]")


def escape(buffer):
    if len(buffer) < 2:
        return 0, None

    match = pattern.search(buffer[1:])

    if match == None or match.start() > 0:
        return 0, None

    index_char_matched = chars_escape.find(buffer[1])

    return 1, EnumEscape(index_char_matched + 1)

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


def process(buffer, index_char, prev_token):
    if len(buffer) < 2:
        return buffer, index_char, index_char, None

    match = pattern.search(buffer[index_char + 1 :])

    if match == None or match.start() > 0:
        return buffer, index_char, index_char, None

    index_char_matched = chars_escape.find(buffer[index_char + 1])

    return buffer, index_char, index_char + 1, EnumEscape(index_char_matched + 1)

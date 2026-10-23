import re
from enum import Enum

EnumLink = Enum(
    "Link",
    [
        "SquareOpen",
        "SquareClose",
    ],
)

buffer_options = "[]"


def squareOpenProcess(buffer, index_char, _):
    return buffer, index_char, index_char, EnumLink.SquareOpen


def squareCloseProcess(buffer, index_char, _):
    return buffer, index_char, index_char, EnumLink.SquareClose

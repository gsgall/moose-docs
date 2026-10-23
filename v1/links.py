import re

from enum import Enum

EnumLink = Enum(
    "Link",
    [
        "SquareOpen",
        "SquareClose",
        "ParenthesisOpen",
        "ParenthesisClose",
    ],
)

buffer_options = "[]()"


def squareopen(buffer):
    return 0, EnumLink.SquareOpen


def squareclose(buffer):
    return 0, EnumLink.SquareClose


def parenthesisopen(buffer):
    return 0, EnumLink.ParenthesisOpen


def parenthesisclose(buffer):
    return 0, EnumLink.ParenthesisClose

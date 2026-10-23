import re

from enum import Enum
from error import EnumError

EnumFormatting = Enum(
    "Formatting",
    [
        "Underline",
        "Strong",
        "Emphasis",
        "Strikethrough",
        "Superscript",
        "Subscript",
    ],
)


def underline(buffer):
    return 0, EnumFormatting.Underline


def strong(buffer):
    return 0, EnumFormatting.Strong


def emphasis(buffer):
    return 0, EnumFormatting.Emphasis


def strikethrough(buffer):
    return 0, EnumFormatting.Strikethrough


def superscript(buffer):
    return 0, EnumFormatting.Superscript


def subscript(buffer):
    return 0, EnumFormatting.Subscript

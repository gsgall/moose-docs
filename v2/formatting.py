import re
from enum import Enum

from error import EnumError

EnumFormatting = Enum(
    "Formatting",
    [
        "UnderlineStart",
        "UnderlineEnd",
        "StrongStart",
        "StrongEnd",
        "EmphasisStart",
        "EmphasisEnd",
        "StrikethroughStart",
        "StrikethroughEnd",
        "SuperScript",
        "SubScript",
        "MonospaceStart",
        "MonospaceStop",
    ],
)

EnumSettings = Enum("Settings", ["Setting"])

formatt_keys = [
    "`",
    "=",
    "+",
    "*",
    "~",
    "^",
    "@",
]


def formatHelper(buffer, index_char, enum_start, enum_end):

    if index_char == 0:
        return buffer, index_char, index_char, enum_start

    char_prev = buffer[index_char - 1]
    char_curr = buffer[index_char]
    char_next = buffer[index_char + 1]

    if not char_next.isspace() and (
        char_prev.isspace() or (char_prev in formatt_keys and char_prev != char_curr)
    ):
        return buffer, index_char, index_char, enum_start

    if not char_prev.isspace() and (
        char_next.isspace() or (char_prev in formatt_keys and char_next != char_curr)
    ):
        return buffer, index_char, index_char, enum_end

    return buffer, index_char, index_char, None


def formatHelperSuperSub(buffer, index_char, enum_start, enum_end):
    if index_char == 0:
        return buffer, index_char, index_char, enum_start

    if buffer[index_char - 1] == "`" or buffer[index_char + 1] == "`":
        return buffer, index_char, index_char, None

    if not buffer[index_char - 1].isspace() and not buffer[index_char + 1].isspace():
        return buffer, index_char, index_char, enum_start

    if not buffer[index_char - 1].isspace() and buffer[index_char + 1].isspace():
        return buffer, index_char, index_char, enum_end

    return buffer, index_char, index_char, None


# NOTE: THis is include since the settings in the code block environment can come immediately after the ticks
pattern_whitespace_or_tick = re.compile(r"[\s`]")
pattern = re.compile(r"\s")


def underlineProcess(buffer, index_char, prev_token):
    return formatHelper(
        buffer, index_char, EnumFormatting.StrongStart, EnumFormatting.StrongEnd
    )


def strongProcess(buffer, index_char, prev_token):
    return formatHelper(
        buffer, index_char, EnumFormatting.StrongStart, EnumFormatting.StrongEnd
    )


def emphasisProcess(buffer, index_char, prev_token):
    return formatHelper(
        buffer, index_char, EnumFormatting.EmphasisStart, EnumFormatting.EmphasisEnd
    )


def strikethroughProcess(buffer, index_char, prev_token):
    return formatHelper(
        buffer,
        index_char,
        EnumFormatting.StrikethroughStart,
        EnumFormatting.StrikethroughEnd,
    )


def superscriptProcess(buffer, index_char, prev_token):
    return formatHelperSuperSub(
        buffer,
        index_char,
        EnumFormatting.SuperScript,
        EnumFormatting.SuperScript,
    )


def subscriptProcess(buffer, index_char, prev_token):
    return formatHelperSuperSub(
        buffer,
        index_char,
        EnumFormatting.SubScript,
        EnumFormatting.SubScript,
    )

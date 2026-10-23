import re
from enum import Enum

import formatting

EnumBackTick = Enum(
    "BackTick",
    ["Triple", "CodeBlockStart", "CodeBlockEnd"],
)


pattern_tick_end = re.compile(r"[^`]")


def process(buffer, index_char, prev_token):
    match = pattern_tick_end.search(buffer[index_char:])

    if match is None or match.start() != 3:
        return formatting.formatHelper(
            buffer,
            index_char,
            formatting.EnumFormatting.MonospaceStart,
            formatting.EnumFormatting.MonospaceStop,
        )

    index_newline = buffer[::-1].find("\n")

    # case for the first line
    if index_newline == -1:
        return buffer, index_char, index_char + match.start() - 1, EnumBackTick.Triple

    if not buffer[index_char - index_newline : index_char].isspace():
        return formatting.formatHelper(
            buffer,
            index_char,
            formatting.EnumFormatting.MonospaceStart,
            formatting.EnumFormatting.MonospaceStop,
        )

    return buffer, index_char, index_char + match.start() - 1, EnumBackTick.Triple

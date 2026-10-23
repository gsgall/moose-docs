import re
from enum import Enum
from error import EnumError

import newline
import token
import formatting

EnumBackTick = Enum(
    "BackTick",
    ["CodeBlock"],
)


pattern_tick_end = re.compile(r"[^`]")


def process(buffer, index_char, prev_token):
    if (
        prev_token.enum != token.EnumCentinal.BeginFile
        and prev_token.enum != newline.EnumNewLine.ParagraphBreak
    ):
        return index_char, None

    if index_char == 1 and buffer[0] != "\n":
        return index_char, None

    if index_char > 2 and buffer[index_char - 2 : index_char] != "\n\n":
        return index_char, None

    match = pattern_tick_end.search(buffer[index_char:])

    if match.start() != 3:
        return index_char, formatting.EnumFormatting.Monospace

    return index_char + match.start() - 1, EnumBackTick.CodeBlock

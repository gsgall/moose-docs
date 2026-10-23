import re

from enum import Enum

EnumNewLine = Enum("NewLine", ["NewLine", "ParagraphBreak"])

pattern = re.compile(r"[^\n]")


def process(buffer, index_char, prev_token):

    match = pattern.search(buffer[index_char:])

    if match is None or match.start() == 1:
        return buffer, index_char, index_char, None

    return (
        buffer,
        index_char,
        index_char + match.start() - 1,
        EnumNewLine.ParagraphBreak,
    )

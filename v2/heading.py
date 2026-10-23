import re
from enum import Enum
from error import EnumError

import newline
import token

import processTokens

EnumHeading = Enum(
    "Heading",
    [
        "Single",
        "Double",
        "Triple",
        "Quad",
        "Quint",
        "Sext",
    ],
)


pattern_pound_end = re.compile(r"[^#]")


def process(buffer, index_char, prev_token):
    if index_char == 1 and buffer[0] != "\n":
        return buffer, index_char, index_char, None

    if index_char > 2 and buffer[index_char - 2 : index_char] != "\n\n":
        return buffer, index_char, index_char, None

    match = pattern_pound_end.search(buffer[index_char:])

    if match is None:
        return buffer, len(buffer), EnumError.Error

    if match.start() > 6:
        return buffer, index_char, index_char, None

    index_match = match.start()
    index_end_of_heading_marker = index_char + index_match

    if buffer[index_end_of_heading_marker] != " ":
        return buffer, index_char, index_char, None

    return buffer, index_char, index_end_of_heading_marker, EnumHeading(index_match)

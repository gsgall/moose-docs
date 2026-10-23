import re
from enum import Enum

from my_token import Token

EnumHeadingStart = Enum(
    "HeadingStart",
    [
        "Single",
        "Double",
        "Triple",
        "Quad",
        "Quint",
        "Sext",
    ],
)

EnumHeadingEnd = Enum(
    "HeadingEnd",
    [
        "Single",
        "Double",
        "Triple",
        "Quad",
        "Quint",
        "Sext",
    ],
)

pattern = re.compile(r"[^#]")


def process(buffer: str, index_char: int) -> tuple[str, int, list[Token]]:

    match = pattern.search(buffer, pos=index_char)
    if match == None:
        return buffer, index_char, []

    index_end_of_heading_marker = match.start()

    if buffer[index_end_of_heading_marker] != " ":
        return buffer, index_char, []

    pound_count = index_end_of_heading_marker - index_char

    if pound_count > 6:
        return buffer, index_char, []

    index_paragraph_break = buffer.find("\n\n", index_end_of_heading_marker)

    return (
        buffer,
        index_end_of_heading_marker + 1,
        [
            Token(
                enum=EnumHeadingStart(pound_count),
                index_start=index_char,
                index_end=index_end_of_heading_marker,
                index_indent=0,
            ),
            Token(
                enum=EnumHeadingEnd(pound_count),
                index_start=index_paragraph_break,
                index_end=index_paragraph_break + 1,
                index_indent=0,
            ),
        ],
    )


def start(content_file: str, indent_level: int, token_curr: Token):
    return 4, " " * indent_level + str(token_curr.enum) + "\n"


def end(content_file: str, indent_level: int, token_curr: Token):
    return -4, " " * (indent_level - 4) + str(token_curr.enum) + "\n\n"

import re
import sys
from enum import Enum

from error import EnumError

import token

import newline

EnumPound = Enum(
    "Heading", ["Single", "Double", "Triple", "Quad", "Quint", "Sext", "End"]
)

pattern_link_end = re.compile(r"[)\]]")
pattern_pound_end = re.compile(r"[^#]")


def pound(buffer):
    match = pattern_pound_end.search(buffer)
    if match is None:
        return -1, EnumError.Error

    if match.start() > 6:
        return 6, EnumError.TooManyPound

    return match.start() - 1, EnumPound(match.start())


def process_tokens(token_stream: list[token.Token], index_start, buffer):

    token_current = token_stream[index_start]

    if (
        token_stream[index_start - 1].enum != newline.EnumNewLine.MultipleNewLine
        and token_stream[index_start - 1].enum != token.EnumCentinal.BeginFile
    ):
        return 0, []

    if buffer[token_current.index_end + 1] != " ":
        return 0, []

    list_token = []

    for token_potential in token_stream[index_start:]:
        list_token.append(token_potential)
        if (
            token_potential.enum == newline.EnumNewLine.MultipleNewLine
            or token_potential.enum == token.EnumCentinal.EndOfFile
        ):
            break

    return len(list_token), list_token

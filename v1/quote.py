from enum import Enum


EnumQuote = Enum("Quote", "Quote")


def quote(buffer):
    if buffer[1] == " ":
        return 1, EnumQuote.Quote

    return 0, None

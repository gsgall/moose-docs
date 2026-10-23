from enum import Enum

from backtick import EnumBackTick
from quote import EnumQuote

EnumCentinal = Enum("Centinal", ["BeginFile", "EndOfFile"])


class Token:
    enum = None
    index_start = None
    index_end = None
    index_indent = None
    # Creation counter, used to order tokens that share an index_start.
    index_appearance = None

    def __init__(self, enum, index_start, index_end, index_appearance):

        self.enum = enum
        self.index_start = index_start
        self.index_end = index_end
        self.index_appearance = index_appearance

    def __str__(self):
        return f"{self.enum} : {self.index_start} - {self.index_end}"

    def __repr__(self):
        return f"{self.enum} : {self.index_start} - {self.index_end}"

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return (
            self.enum == other.enum
            and self.index_start == other.index_start
            and self.index_end == other.index_end
            and self.index_appearance == other.index_appearance
        )

    def __lt__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        assert self.index_start is not None
        assert other.index_start is not None
        assert self.index_appearance is not None
        assert other.index_appearance is not None

        # NOTE: we do this so that when we have two tokens with the same start index
        # they are sorted in reverse appearance order.
        # This should only occur with section end tokens for nexted blocks
        if self.index_start == other.index_start:
            return self.index_appearance > other.index_appearance

        return self.index_start < other.index_start


if __name__ == "__main__":

    test_list = [
        Token(
            enum=EnumQuote.QuoteStart,
            index_start=1,
            index_end=2,
            index_appearance=1,
        ),
        Token(
            enum=EnumQuote.QuoteEnd,
            index_start=10,
            index_end=11,
            index_appearance=2,
        ),
        Token(
            enum=EnumQuote.QuoteStart,
            index_start=3,
            index_end=4,
            index_appearance=3,
        ),
        Token(
            enum=EnumQuote.QuoteEnd,
            index_start=10,
            index_end=11,
            index_appearance=4,
        ),
        Token(
            enum=EnumBackTick.CodeBlockStart,
            index_start=5,
            index_end=6,
            index_appearance=5,
        ),
        Token(
            enum=EnumBackTick.CodeBlockEnd,
            index_start=10,
            index_end=11,
            index_appearance=6,
        ),
    ]

    print(test_list)

    test_list.sort()

    print(test_list)

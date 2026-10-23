from enum import Enum

EnumCentinal = Enum("Centinal", ["StartFile", "EndFile"])


class Token:
    enum: Enum
    index_start: int
    index_end: int
    index_indent: int
    # Creation counter, used to order tokens that share an index_start.
    index_appearance: int

    def __init__(self, enum, index_start, index_end, index_indent, index_appearance=0):

        assert enum != None
        assert index_start >= 0
        assert index_end >= index_start
        assert index_indent >= 0
        assert index_appearance >= 0

        self.enum = enum
        self.index_start = index_start
        self.index_end = index_end
        self.index_indent = index_indent
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

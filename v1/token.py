from enum import Enum

EnumCentinal = Enum("Centinal", ["BeginFile", "EndOfFile"])


class Token:
    enum = None
    index_start = None
    index_end = None

    def __init__(self, enum, index_start, index_end):

        self.enum = enum
        self.index_start = index_start
        self.index_end = index_end

    def __str__(self):
        return f"{self.enum} : {self.index_start} - {self.index_end}"

    def __repr__(self):
        return f"{self.enum} : {self.index_start} - {self.index_end}"

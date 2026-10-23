from enum import Enum
from error import EnumError


EnumLink = Enum("EnumLink", ["StandardLink", "ShortCutLink"])


def link(file_content, index_start):

    index_square_close = file_content[index_start:].find("]")
    index_newline = file_content[index_start:].find("\n")

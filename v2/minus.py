from enum import Enum

import list

EnumPunctuation = Enum("Punctuation", ["EnDash", "EmDash"])


def process(buffer, index_char, prev_token):
    if len(buffer) >= 3 and buffer[index_char : index_char + 3] == "---":
        return buffer, index_char, index_char + 2, EnumPunctuation.EmDash

    if len(buffer) >= 2 and buffer[index_char : index_char + 2] == "--":
        return buffer, index_char, index_char + 1, EnumPunctuation.EnDash

    if index_char == len(buffer) - 1:
        return buffer, index_char, index_char, None

    if buffer[index_char + 1] != " ":
        return buffer, index_char, index_char, None

    return list.unorderedProcess(buffer, index_char, prev_token)

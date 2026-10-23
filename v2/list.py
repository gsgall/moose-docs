import re
import sys
from enum import Enum
from error import EnumError

EnumList = Enum("List", ["Ordered", "Unordered"])


def unorderedProcess(buffer, index_char, prev_token):

    index_paragraph_end = buffer[index_char:].find("\n\n")

    lines_list = buffer[index_char : index_char + index_paragraph_end].split("\n")

    edited_buffer = ""

    for line in lines_list:
        edited_buffer += line.replace("- ", "  ", 1) + "\n"

    buffer = (
        buffer[:index_char]
        + edited_buffer
        + buffer[index_char + index_paragraph_end + 1 :]
    )

    return buffer, index_char, index_char + 1, EnumList.Unordered


digit_pattern = re.compile(r"[\d+.]")


def orderedProcess(buffer, index_char, prev_token):

    if index_char == len(buffer) - 1:
        return buffer, index_char, index_char, None

    index_dot_find = buffer[index_char:].find(". ")

    if index_dot_find == -1:
        return buffer, index_char, index_char, None

    if not buffer[index_char : index_char + index_dot_find].isdigit():
        return buffer, index_char, index_char, None

    index_next_line = buffer[index_char:].find("\n")
    if index_next_line < index_dot_find:
        return buffer, index_char, index_char, None

    index_paragraph_end = buffer[index_char + index_dot_find :].find("\n\n")
    lines_list = buffer[
        index_char + index_dot_find + 1 : index_char + index_paragraph_end
    ].split("\n")

    edited_buffer = (
        buffer[index_char : index_char + index_dot_find + 1] + lines_list[0] + "\n"
    )
    for line in lines_list[1:]:
        index_dot_find_current = line.find(". ")
        if index_dot_find_current == -1:
            return buffer, index_char, index_char, EnumError.Error

        if not line[:index_dot_find_current].isdigit():
            return buffer, index_char, index_char, EnumError.Error

        edited_buffer += (
            " " * (index_dot_find_current + 1)
            + line[index_dot_find_current + 1 :]
            + "\n"
        )

    buffer = (
        buffer[:index_char] + edited_buffer + buffer[index_char + index_paragraph_end :]
    )

    return buffer, index_char, index_char + index_dot_find, EnumList.Ordered

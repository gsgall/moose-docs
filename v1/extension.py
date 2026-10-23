import re
from enum import Enum

from error import EnumError

EnumExtension = Enum(
    "Extensions",
    [
        "Devel",
        "DevelStart",
        "DevelEnd",
        "Alert",
    ],
)


buffer_search = " \n"
pattern = re.compile("[" + re.escape(buffer_search) + "]")


def extension(buffer):

    match = pattern.search(buffer)

    if match == None:
        return -1, EnumError.Error

    index_match_start = match.start()
    substr = buffer[:index_match_start]

    if substr == "!alert":
        return index_match_start, EnumExtension.Alert

    if substr == "!devel":
        return index_match_start, EnumExtension.Devel

    if substr == "!devel!":
        return index_match_start, EnumExtension.DevelStart

    if substr == "!devel-end!":
        return index_match_start, EnumExtension.DevelEnd

    return 0, None

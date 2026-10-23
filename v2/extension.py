import re
from enum import Enum

from error import EnumError

EnumExtension = Enum(
    "Extensions",
    [
        "Alert",
        "Devel",
        "DevelStart",
        "DevelEnd",
    ],
)


extension_syntax = [
    "alert ",
    "devel ",
    "devel! ",
    "devel-end!\n",
]


def process(buffer, index_char, prev_token):

    for i, extension in enumerate(extension_syntax):
        if buffer.startswith(extension, index_char + 1):
            return (
                buffer,
                index_char,
                index_char + len(extension) - 1,
                EnumExtension(i + 1),
            )

    return buffer, index_char, index_char, None

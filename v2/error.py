from enum import Enum

EnumError = Enum(
    "Error",
    [
        "Error",
        "UnclosedLink",
        "TooManyPound",
    ],
)

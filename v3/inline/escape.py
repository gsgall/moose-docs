import sys
import unittest
from enum import Enum

sys.path.append("../")

from my_token import Token

EnumEscape = Enum(
    "Escape",
    [
        "LineBreak",
        "Bang",
        "SquareOpen",
        "SquareClose",
        "At",
        "Carrot",
        "Star",
        "Plus",
        "Tilde",
        "Minus",
    ],
)

enumMap = {
    "\\": EnumEscape.LineBreak,
    "!": EnumEscape.Bang,
    "[": EnumEscape.SquareOpen,
    "]": EnumEscape.SquareClose,
    "@": EnumEscape.At,
    "^": EnumEscape.Carrot,
    "*": EnumEscape.Star,
    "+": EnumEscape.Plus,
    "~": EnumEscape.Tilde,
    "-": EnumEscape.Minus,
}


def process(
    buffer: str,
    index_char: int,
) -> tuple[int, list[Token]]:

    if index_char == len(buffer) - 1:
        return index_char, []

    try:
        return (
            index_char + 1,
            [
                Token(
                    enum=enumMap[buffer[index_char + 1]],
                    index_start=index_char,
                    index_end=index_char + 1,
                    index_indent=0,
                ),
            ],
        )
    except KeyError:
        return index_char, []


class TestPunctuation(unittest.TestCase):
    def testEscapes(self):

        chars = enumMap.keys()

        for char in chars:
            input = f"This is a test that has a \\{char} in it"

            index_end, token_list = process(
                input,
                input.find("\\"),
            )

            self.assertEqual(1, len(token_list))
            self.assertEqual(enumMap[char], token_list[0].enum)
            self.assertEqual(
                f"\\{char}",
                input[token_list[0].index_start : token_list[0].index_end + 1],
            )


if __name__ == "__main__":
    unittest.main()

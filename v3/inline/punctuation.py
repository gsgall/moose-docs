import sys
import unittest
from enum import Enum

sys.path.append("../")

from my_token import Token

EnumPunctation = Enum(
    "Punctuation",
    [
        "EmDash",
        "EnDash",
    ],
)


def process(
    buffer: str,
    index_char: int,
) -> tuple[int, list[Token]]:

    if index_char == len(buffer):
        return index_char, []

    if buffer.startswith("---", index_char):
        return (
            index_char + 2,
            [
                Token(
                    enum=EnumPunctation.EmDash,
                    index_start=index_char,
                    index_end=index_char + 2,
                    index_indent=0,
                ),
            ],
        )

    if buffer.startswith("--", index_char):
        return (
            index_char + 1,
            [
                Token(
                    enum=EnumPunctation.EnDash,
                    index_start=index_char,
                    index_end=index_char + 1,
                    index_indent=0,
                ),
            ],
        )

    return index_char, []


class TestPunctuation(unittest.TestCase):
    def testEmDash(self):
        input = "1. An empty line followed by a non-list marker---everything except a hyphen---will stop the"

        index_end, token_list = process(
            input,
            input.find("---"),
        )

        self.assertEqual(1, len(token_list))
        self.assertEqual(
            "---", input[token_list[0].index_start : token_list[0].index_end + 1]
        )

    def testEnDash(self):
        input = "1. An empty line followed by a non-list marker--everything except a hyphen--will stop the"

        index_end, token_list = process(
            input,
            input.find("--"),
        )

        self.assertEqual(1, len(token_list))
        self.assertEqual(
            "--", input[token_list[0].index_start : token_list[0].index_end + 1]
        )

    def testHyphen(self):
        input = "1. An empty line followed by a non-list marker--everything except a hyphen--will stop the"

        index_end, token_list = process(
            input,
            input.find("-"),
        )

        self.assertEqual(0, len(token_list))


if __name__ == "__main__":
    unittest.main()

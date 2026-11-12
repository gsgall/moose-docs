import sys
import unittest
from enum import Enum

sys.path.append("../")

from my_token import Token

EnumMonoSpace = Enum(
    "MonoSpace",
    [
        "Start",
        "End",
    ],
)


def process(
    buffer: str,
    index_char: int,
) -> tuple[int, list[Token]]:

    index_next_back_tick = buffer.find("`", index_char + 1)

    if index_next_back_tick == -1:
        return index_char, []

    assert index_next_back_tick > index_char

    if index_next_back_tick - index_char == 1:
        index_next_back_tick = buffer.find("`", index_next_back_tick + 1)

        if index_next_back_tick == -1:
            return index_char, []

    assert index_next_back_tick - index_char > 1

    return (
        index_char + 1,
        [
            Token(
                enum=EnumMonoSpace.Start,
                index_start=index_char,
                index_end=index_char,
                index_indent=0,
            ),
            Token(
                enum=EnumMonoSpace.End,
                index_start=index_next_back_tick,
                index_end=index_next_back_tick,
                index_indent=0,
            ),
        ],
    )


class MonoSpaceTests(unittest.TestCase):
    def testInvalid(self):
        input = "The following MooseDocs `[google] will show verbatim because it"

        index_end, token_list = process(
            input,
            input.find("`"),
        )

        self.assertEqual(0, len(token_list))

    def testValid(self):
        input = "The following MooseDocs `[google]` will show verbatim because it"

        index_end, token_list = process(
            input,
            input.find("`"),
        )

        token_first = token_list[0]
        token_second = token_list[1]

        self.assertEqual(2, len(token_list))
        self.assertEqual(
            "[google]", input[token_first.index_start + 1 : token_second.index_start]
        )

    def testTripleBackTick(self):
        input = "display in triple back-ticks (```), this is commonly referred to as fenced code blocks. Two"

        index_end, token_list = process(
            input,
            input.find("`"),
        )

        token_first = token_list[0]
        token_second = token_list[1]

        self.assertEqual(2, len(token_list))
        self.assertEqual(
            "`", input[token_first.index_start + 1 : token_second.index_start]
        )


if __name__ == "__main__":
    unittest.main()

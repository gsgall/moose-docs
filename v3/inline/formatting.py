import sys
import unittest
from enum import Enum

sys.path.append("../")

from my_token import Token

EnumUnderline = Enum(
    "Underline",
    [
        "Start",
        "End",
    ],
)

EnumSuperScript = Enum(
    "SuperScript",
    [
        "Start",
        "End",
    ],
)


EnumSubScript = Enum(
    "SubScript",
    [
        "Start",
        "End",
    ],
)


def processGeneral(
    buffer: str,
    index_char: int,
    delimiter_char: str,
    enum_start: Enum,
    enum_end: Enum,
) -> tuple[str, int, list[Token]]:

    assert len(delimiter_char) == 1

    if buffer[index_char + 1].isspace():
        return buffer, index_char, []

    if index_char != 0 and not buffer[index_char - 1].isspace():
        return buffer, index_char, []

    index_pattern_end = buffer.find(delimiter_char, index_char + 1)

    if index_pattern_end == -1:
        return buffer, index_char, []

    assert index_pattern_end > index_char

    if buffer[index_pattern_end - 1].isspace():
        return buffer, index_char, []

    return (
        buffer,
        index_char + 1,
        [
            Token(
                enum=enum_start,
                index_start=index_char,
                index_end=index_char,
                index_indent=0,
            ),
            Token(
                enum=enum_start,
                index_start=index_pattern_end,
                index_end=index_pattern_end,
                index_indent=0,
            ),
        ],
    )


def processSuperSub(
    buffer: str,
    index_char: int,
    delimiter_char: str,
    enum_start: Enum,
    enum_end: Enum,
) -> tuple[str, int, list[Token]]:

    assert len(delimiter_char) == 1

    if buffer[index_char + 1].isspace():
        return buffer, index_char, []

    if index_char != 0 and buffer[index_char - 1].isspace():
        return buffer, index_char, []

    index_pattern_end = buffer.find(delimiter_char, index_char + 1)

    if index_pattern_end == -1:
        return buffer, index_char, []

    assert index_pattern_end > index_char

    if buffer[index_pattern_end - 1].isspace():
        return buffer, index_char, []

    return (
        buffer,
        index_char + 1,
        [
            Token(
                enum=enum_start,
                index_start=index_char,
                index_end=index_char,
                index_indent=0,
            ),
            Token(
                enum=enum_end,
                index_start=index_pattern_end,
                index_end=index_pattern_end,
                index_indent=0,
            ),
        ],
    )


class UnderlineTests(unittest.TestCase):
    def testInvalid(self):
        input = "Yo, dawg I heard you like formatting, so I created =underline"

        buffer_updated, index_block_start_end, token_list = processGeneral(
            input,
            input.find("="),
            "=",
            EnumUnderline.Start,
            EnumUnderline.End,
        )
        self.assertEqual(0, len(token_list))

    def testValid(self):
        input = "Yo, dawg I heard you like formatting, so I created =underline="

        buffer_updated, index_block_start_end, token_list = processGeneral(
            input,
            input.find("="),
            "=",
            EnumUnderline.Start,
            EnumUnderline.End,
        )

        token_first = token_list[0]
        token_second = token_list[1]

        self.assertEqual(2, len(token_list))
        self.assertEqual(
            "underline", input[token_first.index_start + 1 : token_second.index_start]
        )

    def testComplexFormatting(self):
        input = "Yo, dawg I heard you like formatting, so I created =underline"
        input += "formatted text that contains text with ~strikethrough that"
        input += "contains +bold formatting with *emphasis that has some^superscript"
        input += "text with a@subscript@^*+~=, I hope you like it."

        buffer_updated, index_block_start_end, token_list = processGeneral(
            input,
            input.find("="),
            "=",
            EnumUnderline.Start,
            EnumUnderline.End,
        )

        self.assertEqual(2, len(token_list))


class SuperScriptTests(unittest.TestCase):
    def testInvalid(self):
        input = "Yo, dawg I heard you like formatting, so I created ^underline"

        buffer_updated, index_block_start_end, token_list = processSuperSub(
            input,
            input.find("^"),
            "^",
            EnumSuperScript.Start,
            EnumSuperScript.End,
        )
        self.assertEqual(0, len(token_list))

    def testValid(self):
        input = "Yo, dawg I heard you like formatting, so I created^superscript^"

        buffer_updated, index_block_start_end, token_list = processSuperSub(
            input,
            input.find("^"),
            "^",
            EnumSuperScript.Start,
            EnumSuperScript.End,
        )

        token_first = token_list[0]
        token_second = token_list[1]

        self.assertEqual(2, len(token_list))
        self.assertEqual(
            "superscript", input[token_first.index_start + 1 : token_second.index_start]
        )

    def testComplexFormatting(self):
        input = "Yo, dawg I heard you like formatting, so I created =underline"
        input += "formatted text that contains text with ~strikethrough that"
        input += "contains +bold formatting with *emphasis that has some^superscript"
        input += "text with a@subscript@^*+~=, I hope you like it."

        buffer_updated, index_block_start_end, token_list = processSuperSub(
            input,
            input.find("^"),
            "^",
            EnumSuperScript.Start,
            EnumSuperScript.End,
        )

        self.assertEqual(2, len(token_list))


if __name__ == "__main__":
    unittest.main()

import unittest
from enum import Enum

from my_token import Token

EnumAlert = Enum(
    "AlertExtension",
    ["Start", "End"],
)

EnumDevel = Enum(
    "DevelExtension",
    ["Start", "End"],
)


extension_syntax_open_close = {
    "alert ": "\n\n",
    "devel ": "\n\n",
    "devel! ": "!devel-end!\n",
}

extension_syntax_start_enum = {
    "alert ": EnumAlert.Start,
    "devel ": EnumDevel.Start,
    "devel! ": EnumDevel.Start,
}

extension_syntax_end_enum = {
    "alert ": EnumAlert.End,
    "devel ": EnumDevel.End,
    "devel! ": EnumDevel.End,
}


def process(buffer: str, index_char: int) -> tuple[str, int, list[Token]]:

    index_space = buffer.find(" ", index_char + 1)

    syntax_begin = buffer[index_char + 1 : index_space + 1]

    if syntax_begin not in extension_syntax_open_close:
        return buffer, index_char, []

    syntax_close = extension_syntax_open_close[syntax_begin]
    index_syntax_close = buffer.find(syntax_close, index_char + len(syntax_begin))

    if index_syntax_close == -1 and syntax_close == "\n\n":
        index_syntax_close = len(buffer) - 1

    return (
        buffer,
        index_char + len(syntax_begin) + 1,
        [
            Token(
                enum=extension_syntax_start_enum[syntax_begin],
                index_start=index_char,
                index_end=index_char + len(syntax_begin),
                index_indent=0,
            ),
            Token(
                enum=extension_syntax_end_enum[syntax_begin],
                index_start=index_syntax_close,
                index_end=index_syntax_close + len(syntax_close) - 1,
                index_indent=0,
            ),
        ],
    )


class TestExtension(unittest.TestCase):
    def testAlert(self):

        input = "!alert note title=MooseDown is a restricted version of [markdown].\n"
        input += "To unify content and to create a fast parser a strict, limited set of markdown is being used to\n"
        input += (
            "define the MooseDocs syntax. The following sections detail the syntax.\n\n"
        )

        _, index_block_start_end, token_list = process(input, 0)

        self.assertEqual(2, len(token_list))
        self.assertEqual(len("!alert "), index_block_start_end)
        token_first = token_list[0]
        self.assertEqual(
            "!alert ", input[token_first.index_start : token_first.index_end + 1]
        )
        token_second = token_list[1]
        self.assertEqual(
            "\n\n", input[token_second.index_start : token_second.index_end + 1]
        )

    def testDevel(self):

        input = "!devel example id=settings-example\n"
        input += "               caption=Example use of settings within [#links]. Settings are key-value pairs that\n"
        input += "                       are specified with a separating equal sign (no spaces exist on either side).\n"
        input += "[google](https://www.google.com style=color:teal;)\n"

        _, index_block_start_end, token_list = process(input, 0)

        self.assertEqual(2, len(token_list))
        self.assertEqual(len("!devel "), index_block_start_end)
        token_first = token_list[0]
        self.assertEqual(
            "!devel ", input[token_first.index_start : token_first.index_end + 1]
        )
        token_second = token_list[1]
        self.assertEqual(
            "\n", input[token_second.index_start : token_second.index_end + 1]
        )

    def testDevelBlock(self):

        input = "!devel! example id=break caption=Example line break.\n"
        input += "This sentence has a\\ line break. And so does\\\n"
        input += "this.\n"
        input += "!devel-end!\n"

        _, index_block_start_end, token_list = process(input, 0)

        self.assertEqual(2, len(token_list))
        self.assertEqual(len("!devel! "), index_block_start_end)
        token_first = token_list[0]
        self.assertEqual(
            "!devel! ", input[token_first.index_start : token_first.index_end + 1]
        )
        token_second = token_list[1]
        self.assertEqual(
            "!devel-end!\n",
            input[token_second.index_start : token_second.index_end + 1],
        )


def start(content_file: str, indent_level: int, token_curr: Token):
    return 4, " " * indent_level + str(token_curr.enum) + "\n"


def end(content_file: str, indent_level: int, token_curr: Token):
    return -4, " " * (indent_level - 4) + str(token_curr.enum) + "\n\n"


if __name__ == "__main__":
    unittest.main()

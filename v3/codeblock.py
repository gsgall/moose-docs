import re
import unittest
from enum import Enum

from my_token import Token

EnumCodeBlock = Enum(
    "CodeBlock",
    ["Start", "End"],
)


pattern_tick_end = re.compile(r"[^`]")


def process(buffer: str, index_char: int) -> tuple[str, int, list[Token]]:
    match = pattern_tick_end.search(buffer[index_char:])

    if match is None or match.start() != 3:
        return buffer, index_char, []

    index_newline = buffer.rfind("\n", 0, index_char)
    if (
        index_char - index_newline > 0
        and not buffer[index_newline:index_char].isspace()
    ):
        return buffer, index_char, []

    index_code_block_end = buffer.find("```", index_char + 3)

    assert index_code_block_end != -1
    len_buffer = len(buffer)

    buffer = buffer[:index_code_block_end] + "   " + buffer[index_code_block_end + 3 :]

    assert len_buffer == len(buffer)

    return (
        buffer,
        index_char + 2,
        [
            Token(
                enum=EnumCodeBlock.Start,
                index_start=index_char,
                index_end=index_char + 2,
                index_indent=0,
            ),
            Token(
                enum=EnumCodeBlock.End,
                index_start=index_code_block_end,
                index_end=index_code_block_end + 2,
                index_indent=0,
            ),
        ],
    )


def start(content_file: str, indent_level: int, token_curr: Token):
    return 4, " " * indent_level + str(token_curr.enum) + "\n"


def end(content_file: str, indent_level: int, token_curr: Token):
    return -4, " " * (indent_level - 4) + str(token_curr.enum) + "\n\n"


class TestCodeBlock(unittest.TestCase):
    def testFirstExample(self):

        input = (
            "!devel example caption=Basic fenced code block. id=fenced-code-example\n"
        )
        input += "```language=bash\n"
        input += "export METHOD=opt\n"
        input += "```\n"

        expected_update = (
            "!devel example caption=Basic fenced code block. id=fenced-code-example\n"
        )
        expected_update += "```language=bash\n"
        expected_update += "export METHOD=opt\n"
        expected_update += "   \n"

        index_back_tick = input.find("`")

        buffer_updated, index_code_block_start_end, tokens = process(
            input, index_back_tick
        )

        self.assertEqual(expected_update, buffer_updated)
        self.assertEqual(index_back_tick + 2, index_code_block_start_end)
        self.assertEqual(2, len(tokens))

    def testQuoted(self):
        input = "!devel example caption=Nested content in block quotes. id=quote-nested-example\n"
        input += "> Quotations begin with the character and may\n"
        input += "> contain any valid markdown content, include quotes and code as shown here.\n"
        input += "> \n"
        input += "> > This begins another quotation, which also contains a fenced code block.\n"
        input += "> >\n"
        input += "> > ```language=python\n"
        input += "> > for i in range(10):\n"
        input += "> >   print i\n"
        input += "> > ```\n"
        input += ">\n"
        input += (
            "> Since quotations are block content they must end with an empty line,\n"
        )
        input += "> therefore the nested quote above must contain an empty line.\n"
        input += "\n"

        index_back_tick = input.find("`")

        buffer_updated, index_code_block_start_end, token_list = process(
            input, index_back_tick
        )

        self.assertEqual(index_back_tick, index_code_block_start_end)
        self.assertEqual(0, len(token_list))
        self.assertEqual(input, buffer_updated)

    def testIndented(self):
        input = "!devel example caption=Nested content in block quotes. id=quote-nested-example\n"
        input += " Quotations begin with the character and may\n"
        input += " \n"
        input += "    This begins another quotation, which also contains a fenced code block.\n"
        input += "   \n"
        input += "    ```language=python\n"
        input += "    for i in range(10):\n"
        input += "      print i\n"
        input += "    ```\n"
        input += " \n"
        input += (
            "  Since quotations are block content they must end with an empty line,\n"
        )
        input += "  therefore the nested quote above must contain an empty line.\n"
        input += "\n"

        expected_update = "!devel example caption=Nested content in block quotes. id=quote-nested-example\n"
        expected_update += " Quotations begin with the character and may\n"
        expected_update += " \n"
        expected_update += "    This begins another quotation, which also contains a fenced code block.\n"
        expected_update += "   \n"
        expected_update += "    ```language=python\n"
        expected_update += "    for i in range(10):\n"
        expected_update += "      print i\n"
        expected_update += "       \n"
        expected_update += " \n"
        expected_update += (
            "  Since quotations are block content they must end with an empty line,\n"
        )
        expected_update += (
            "  therefore the nested quote above must contain an empty line.\n\n"
        )

        index_back_tick = input.find("`")

        buffer_updated, index_code_block_start_end, token_list = process(
            input, index_back_tick
        )

        self.assertEqual(expected_update, buffer_updated)
        self.assertEqual(index_back_tick + 2, index_code_block_start_end)
        self.assertEqual(2, len(token_list))


if __name__ == "__main__":

    unittest.main()

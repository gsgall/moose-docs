import unittest
from enum import Enum

from my_token import Token

EnumQuote = Enum("Quote", ["Start", "End"])


def process(buffer: str, index_char: int) -> tuple[str, int, list[Token]]:

    if index_char == len(buffer) - 1:
        return buffer, index_char, []

    if buffer[index_char + 1] != " ":
        return buffer, index_char, []

    indent_depth = index_char - buffer.rfind("\n", 0, index_char) - 1
    # This would occur when it is the first line
    if indent_depth < 0:
        indent_depth = index_char

    index_paragraph_break = buffer.find("\n\n", index_char - indent_depth)

    if index_paragraph_break == -1:
        index_paragraph_break = len(buffer) - 1

    lines_quote = buffer[index_char - indent_depth : index_paragraph_break].splitlines(
        True
    )
    edited_buffer = ""

    for line in lines_quote:
        indent_depth_current_line = line.find(">")

        if indent_depth_current_line == -1:
            edited_buffer += line
            continue

        if indent_depth_current_line == indent_depth:
            edited_buffer += line.replace(">", " ", 1)

    len_buffer = len(buffer)
    buffer = (
        buffer[: index_char - indent_depth]
        + edited_buffer
        + buffer[index_paragraph_break:]
    )
    assert len(buffer) == len_buffer

    return (
        buffer,
        index_char + 1,
        [
            Token(
                enum=EnumQuote.Start,
                index_start=index_char,
                index_end=index_char + 1,
                index_indent=indent_depth,
            ),
            Token(
                enum=EnumQuote.End,
                index_start=index_paragraph_break,
                index_end=index_paragraph_break + 1,
                index_indent=indent_depth,
            ),
        ],
    )


def start(content_file: str, indent_level: int, token_curr: Token):
    return 4, " " * indent_level + str(token_curr.enum) + "\n"


def end(content_file: str, indent_level: int, token_curr: Token):
    return -4, " " * (indent_level - 4) + str(token_curr.enum) + "\n\n"


class TestQuote(unittest.TestCase):
    def testQuote(self):
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
        input += "> therefore the nested quote above must contain an empty line.\n\n"

        expected_update = "!devel example caption=Nested content in block quotes. id=quote-nested-example\n"
        expected_update += "  Quotations begin with the character and may\n"
        expected_update += "  contain any valid markdown content, include quotes and code as shown here.\n"
        expected_update += "  \n"
        expected_update += "  > This begins another quotation, which also contains a fenced code block.\n"
        expected_update += "  >\n"
        expected_update += "  > ```language=python\n"
        expected_update += "  > for i in range(10):\n"
        expected_update += "  >   print i\n"
        expected_update += "  > ```\n"
        expected_update += " \n"
        expected_update += (
            "  Since quotations are block content they must end with an empty line,\n"
        )
        expected_update += (
            "  therefore the nested quote above must contain an empty line.\n\n"
        )

        index_quote = input.find("> ")

        buffer_updated, index_block_start_end, token_list = process(input, index_quote)
        self.maxDiff = None
        self.assertEqual(2, len(token_list))
        self.assertEqual(index_quote + 1, index_block_start_end)
        self.assertEqual(expected_update, buffer_updated)
        self.assertEqual(len(input) - 2, token_list[1].index_start)
        self.assertEqual(len(input) - 1, token_list[1].index_end)
        self.assertEqual(0, token_list[1].index_indent)

    def testNestedQuote(self):

        input = "!devel example caption=Nested content in block quotes. id=quote-nested-example\n"
        input += "  Quotations begin with the character and may\n"
        input += "  contain any valid markdown content, include quotes and code as shown here.\n"
        input += "  \n"
        input += "  > This begins another quotation, which also contains a fenced code block.\n"
        input += "  >\n"
        input += "  > ```language=python\n"
        input += "  > for i in range(10):\n"
        input += "  >   print i\n"
        input += "  > ```\n"
        input += " \n"
        input += (
            "  Since quotations are block content they must end with an empty line,\n"
        )
        input += "  therefore the nested quote above must contain an empty line.\n\n"

        expected_update = "!devel example caption=Nested content in block quotes. id=quote-nested-example\n"
        expected_update += "  Quotations begin with the character and may\n"
        expected_update += "  contain any valid markdown content, include quotes and code as shown here.\n"
        expected_update += "  \n"
        expected_update += "    This begins another quotation, which also contains a fenced code block.\n"
        expected_update += "   \n"
        expected_update += "    ```language=python\n"
        expected_update += "    for i in range(10):\n"
        expected_update += "      print i\n"
        expected_update += "    ```\n"
        expected_update += " \n"
        expected_update += (
            "  Since quotations are block content they must end with an empty line,\n"
        )
        expected_update += (
            "  therefore the nested quote above must contain an empty line.\n\n"
        )

        index_quote = input.find("> ")

        buffer_updated, index_block_start_end, token_list = process(input, index_quote)

        self.assertEqual(2, len(token_list))
        self.assertEqual(index_quote + 1, index_block_start_end)
        self.assertEqual(expected_update, buffer_updated)
        self.assertEqual(len(input) - 2, token_list[1].index_start)
        self.assertEqual(len(input) - 1, token_list[1].index_end)
        self.assertEqual(2, token_list[1].index_indent)


if __name__ == "__main__":

    unittest.main()

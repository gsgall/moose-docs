import unittest
from enum import Enum

from my_token import Token

EnumTable = Enum(
    "Table",
    [
        "Start",
        "End",
    ],
)


def process(buffer: str, index_char: int) -> tuple[str, int, list[Token]]:
    if buffer[index_char + 1] != " ":
        return buffer, index_char, []

    index_curr_char = buffer.find("\n", index_char + 1)

    while index_curr_char > 0 and index_curr_char < len(buffer):
        if buffer[index_curr_char + 1 : index_curr_char + 3] != "| ":
            break

        index_curr_char = buffer.find("\n", index_curr_char + 2)

    return (
        buffer,
        index_curr_char + 1,
        [
            Token(
                enum=EnumTable.Start,
                index_start=index_char,
                index_end=index_char + 1,
                index_indent=0,
            ),
            Token(
                enum=EnumTable.End,
                index_start=index_curr_char,
                index_end=index_curr_char,
                index_indent=0,
            ),
        ],
    )


class TestTable(unittest.TestCase):
    def testTable(self):

        input = "`\\` character, as in the following examples.\n"
        input += "\n"
        input += "| MooseDocs | HTML |\n"
        input += "| :-        | :-   |\n"
        input += "| `\\!`      | \\!   |\n"
        input += "| `\\[`      | \\[   |\n"
        input += "| `\\]`      | \\]   |\n"
        input += "| `\\@`      | \\@   |\n"
        input += "| `\\^`      | \\^   |\n"
        input += "| `\\*`      | \\*   |\n"
        input += "| `\\+`      | \\+   |\n"
        input += "| `\\~`      | \\~   |\n"
        input += "| `\\-`      | \\-   |\n\n"
        input += "[markdown]: https://en.wikipedia.org/wiki/Markdown"

        index_start = input.find("| ")
        index_end = input.find("\n\n[markdown]")

        buffer_updated, index_block_start_end, token_list = process(input, index_start)

        self.assertEqual(input, buffer_updated)

        self.assertEqual(index_end + 1, index_block_start_end)

        self.assertEqual(2, len(token_list))

        token_first = token_list[0]
        self.assertEqual(
            "| ", input[token_first.index_start : token_first.index_end + 1]
        )
        self.assertEqual(index_start, token_first.index_start)
        token_second = token_list[1]
        self.assertEqual(index_end, token_second.index_start)
        self.assertEqual(
            "\n", input[token_second.index_start : token_second.index_end + 1]
        )

        captured_table = "| MooseDocs | HTML |\n"
        captured_table += "| :-        | :-   |\n"
        captured_table += "| `\\!`      | \\!   |\n"
        captured_table += "| `\\[`      | \\[   |\n"
        captured_table += "| `\\]`      | \\]   |\n"
        captured_table += "| `\\@`      | \\@   |\n"
        captured_table += "| `\\^`      | \\^   |\n"
        captured_table += "| `\\*`      | \\*   |\n"
        captured_table += "| `\\+`      | \\+   |\n"
        captured_table += "| `\\~`      | \\~   |\n"
        captured_table += "| `\\-`      | \\-   |\n"

        self.assertEqual(
            captured_table, input[token_first.index_start : token_second.index_end + 1]
        )


def start(content_file: str, indent_level: int, token_curr: Token):
    return 4, " " * indent_level + str(token_curr.enum) + "\n"


def end(content_file: str, indent_level: int, token_curr: Token):
    return -4, " " * (indent_level - 4) + str(token_curr.enum) + "\n\n"


if __name__ == "__main__":
    unittest.main()

import pdb
import re
import unittest
from enum import Enum

from my_token import Token

EnumUnorderedList = Enum(
    "UnorderedList",
    [
        "Start",
        "End",
    ],
)

pattern = re.compile(r"\S")


def process(buffer: str, index_char: int) -> tuple[str, int, list[Token]]:

    if index_char == len(buffer) - 1:
        return buffer, index_char, []

    if buffer[index_char + 1] != " ":
        return buffer, index_char, []

    indent_depth = index_char - buffer.rfind("\n", 0, index_char) - 1
    index_next_new_line = buffer.find("\n", index_char + 1)

    if index_next_new_line == -1:
        return buffer, index_char, []

    index_curr_line_start = buffer.find("\n", index_char + 1) + 1

    edited_buffer = buffer[index_char:index_curr_line_start].replace("-", " ", 1)
    while index_curr_line_start < len(buffer):
        index_next_new_line = buffer.find("\n", index_curr_line_start)
        index_marker_curr_line = buffer.find(
            "- ", index_curr_line_start, index_next_new_line + 1
        )

        if index_marker_curr_line == -1:
            match = pattern.search(
                buffer, index_curr_line_start, index_next_new_line + 1
            )
            # pdb.set_trace()
            if (
                match is not None
                and (match.start() - index_curr_line_start) <= indent_depth
            ):
                break
            edited_buffer += buffer[index_curr_line_start : index_next_new_line + 1]
            index_curr_line_start = index_next_new_line + 1

            continue

        indent_depth_curr_line = index_marker_curr_line - index_curr_line_start

        if indent_depth_curr_line != indent_depth:
            edited_buffer += buffer[index_curr_line_start : index_next_new_line + 1]
            index_curr_line_start = index_next_new_line + 1
            continue

        edited_buffer += buffer[
            index_curr_line_start : index_next_new_line + 1
        ].replace("-", " ", 1)

        index_curr_line_start = index_next_new_line + 1

    len_buffer = len(buffer)

    buffer = buffer[:index_char] + edited_buffer + buffer[index_curr_line_start:]

    assert len_buffer == len(buffer)

    return (
        buffer,
        index_char + 1,
        [
            Token(
                enum=EnumUnorderedList.Start,
                index_start=index_char,
                index_end=index_char + 1,
                index_indent=indent_depth,
            ),
            Token(
                enum=EnumUnorderedList.End,
                index_start=index_curr_line_start - 1,
                index_end=index_curr_line_start - 1,
                index_indent=indent_depth,
            ),
        ],
    )


def start(content_file: str, indent_level: int, token_curr: Token):
    return 4, " " * indent_level + str(token_curr.enum) + "\n"


def end(content_file: str, indent_level: int, token_curr: Token):
    return -4, " " * (indent_level - 4) + str(token_curr.enum) + "\n\n"


class TestList(unittest.TestCase):

    def testUnordered(self):
        input = "!devel! example caption=Unordered list basic syntax. id=unordered-basic-example\n"
        input += "- Item 1\n"
        input += "- Item 2\n"
        input += "!devel-end!\n"
        input += "\n"

        expected_update = "!devel! example caption=Unordered list basic syntax. id=unordered-basic-example\n"
        expected_update += "  Item 1\n"
        expected_update += "  Item 2\n"
        expected_update += "!devel-end!\n"
        expected_update += "\n"

        index_start = input.find("- ")

        buffer_updated, index_block_start_end, token_list = process(input, index_start)
        token_first = token_list[0]
        self.assertEqual(
            "- ", input[token_first.index_start : token_first.index_end + 1]
        )
        token_second = token_list[1]
        self.assertEqual(
            "\n",
            input[token_second.index_start : token_second.index_end + 1],
        )

        self.assertEqual(index_start + 1, index_block_start_end)

        self.assertEqual(0, token_first.index_indent)
        self.assertEqual(0, token_second.index_indent)
        self.assertEqual(input.find("!devel-end!") - 1, token_second.index_start)
        self.assertEqual(input.find("!devel-end!") - 1, token_second.index_end)
        self.assertEqual(expected_update, buffer_updated)

    def testUnorderedOtherMarkdown(self):

        input = "!devel! example caption=Lists can contain other markdown content. id=unordered-nested-example\n"
        input += "- Item with code\n"
        input += "  Content can be contained within a list, all valid MooseDown syntax can be used.\n"
        input += "\n"
        input += "  ```\n"
        input += "  int combo = 12345;\n"
        input += "  ```\n"
        input += "\n"
        input += "- Another item\n"
        input += "\n"
        input += "\n"
        input += "- Foo\n"
        input += "\n"
        input += "  ```\n"
        input += "  bar\n"
        input += "  ```\n"
        input += "!devel-end!\n"

        expected_update = "!devel! example caption=Lists can contain other markdown content. id=unordered-nested-example\n"
        expected_update += "  Item with code\n"
        expected_update += "  Content can be contained within a list, all valid MooseDown syntax can be used.\n"
        expected_update += "\n"
        expected_update += "  ```\n"
        expected_update += "  int combo = 12345;\n"
        expected_update += "  ```\n"
        expected_update += "\n"
        expected_update += "  Another item\n"
        expected_update += "\n"
        expected_update += "\n"
        expected_update += "  Foo\n"
        expected_update += "\n"
        expected_update += "  ```\n"
        expected_update += "  bar\n"
        expected_update += "  ```\n"
        expected_update += "!devel-end!\n"

        index_start = input.find("- ")
        buffer_updated, index_block_start_end, token_list = process(input, index_start)
        token_first = token_list[0]
        token_second = token_list[1]

        self.assertEqual(0, token_first.index_indent)
        self.assertEqual(0, token_second.index_indent)

        self.assertEqual(index_start + 1, index_block_start_end)
        self.assertEqual(
            "- ", input[token_first.index_start : token_first.index_end + 1]
        )
        self.assertEqual(
            "\n",
            input[token_second.index_start : token_second.index_end + 1],
        )
        self.assertEqual(input.find("!devel-end!") - 1, token_second.index_start)
        self.assertEqual(input.find("!devel-end!") - 1, token_second.index_end)
        self.assertEqual(expected_update, buffer_updated)

    def testUnorderedNestedFirstLevel(self):
        input = "!devel! example caption=Nested unordered lists. id=unordered-sublist-example\n"
        input += "- A\n"
        input += "- B\n"
        input += "\n"
        input += "  - B.1\n"
        input += "  - B.2\n"
        input += "\n"
        input += "    - B.2.1\n"
        input += "    - B.2.2\n"
        input += "\n"
        input += "- C\n"
        input += "\n"
        input += "  - B.3\n"
        input += "\n"
        input += "    - B.3.1\n"
        input += "\n"
        input += "      - B 3.1.1\n"
        input += "\n"
        input += "    - B.3.2\n"
        input += "\n"
        input += "  - B.4\n"
        input += "\n"
        input += "- D\n"
        input += "!devel-end!\n"

        expected_update = "!devel! example caption=Nested unordered lists. id=unordered-sublist-example\n"
        expected_update += "  A\n"
        expected_update += "  B\n"
        expected_update += "\n"
        expected_update += "  - B.1\n"
        expected_update += "  - B.2\n"
        expected_update += "\n"
        expected_update += "    - B.2.1\n"
        expected_update += "    - B.2.2\n"
        expected_update += "\n"
        expected_update += "  C\n"
        expected_update += "\n"
        expected_update += "  - B.3\n"
        expected_update += "\n"
        expected_update += "    - B.3.1\n"
        expected_update += "\n"
        expected_update += "      - B 3.1.1\n"
        expected_update += "\n"
        expected_update += "    - B.3.2\n"
        expected_update += "\n"
        expected_update += "  - B.4\n"
        expected_update += "\n"
        expected_update += "  D\n"
        expected_update += "!devel-end!\n"

        index_start = input.find("- ")
        buffer_updated, index_block_start_end, token_list = process(input, index_start)
        token_first = token_list[0]
        token_second = token_list[1]

        self.assertEqual(0, token_first.index_indent)
        self.assertEqual(0, token_second.index_indent)
        self.assertEqual(index_start + 1, index_block_start_end)
        self.assertEqual(expected_update, buffer_updated)
        self.assertEqual(input.find("!devel-end!") - 1, token_second.index_start)
        self.assertEqual(input.find("!devel-end!") - 1, token_second.index_end)

    def testUnorderedNestedSecondLevel(self):

        input = "!devel! example caption=Nested unordered lists. id=unordered-sublist-example\n"
        input += "  A\n"
        input += "  B\n"
        input += "\n"
        input += "  - B.1\n"
        input += "  - B.2\n"
        input += "\n"
        input += "    - B.2.1\n"
        input += "    - B.2.2\n"
        input += "\n"
        input += "  C\n"
        input += "\n"
        input += "  - B.3\n"
        input += "\n"
        input += "    - B.3.1\n"
        input += "\n"
        input += "      - B 3.1.1\n"
        input += "\n"
        input += "    - B.3.2\n"
        input += "\n"
        input += "  - B.4\n"
        input += "\n"
        input += "  D\n"
        input += "!devel-end!\n"

        expected_update = "!devel! example caption=Nested unordered lists. id=unordered-sublist-example\n"
        expected_update += "  A\n"
        expected_update += "  B\n"
        expected_update += "\n"
        expected_update += "    B.1\n"
        expected_update += "    B.2\n"
        expected_update += "\n"
        expected_update += "    - B.2.1\n"
        expected_update += "    - B.2.2\n"
        expected_update += "\n"
        expected_update += "  C\n"
        expected_update += "\n"
        expected_update += "  - B.3\n"
        expected_update += "\n"
        expected_update += "    - B.3.1\n"
        expected_update += "\n"
        expected_update += "      - B 3.1.1\n"
        expected_update += "\n"
        expected_update += "    - B.3.2\n"
        expected_update += "\n"
        expected_update += "  - B.4\n"
        expected_update += "\n"
        expected_update += "  D\n"
        expected_update += "!devel-end!\n"

        index_start = input.find("- ")
        buffer_updated, index_block_start_end, token_list = process(input, index_start)

        token_first = token_list[0]
        token_second = token_list[1]

        self.assertEqual(2, token_first.index_indent)
        self.assertEqual(2, token_second.index_indent)

        self.assertEqual(index_start + 1, index_block_start_end)
        self.assertEqual(expected_update, buffer_updated)
        self.assertEqual(input.find("\n  C"), token_second.index_start)
        self.assertEqual(input.find("\n  C"), token_second.index_end)

    def testUnorderedNestedThirdLevel(self):

        input = "!devel! example caption=Nested unordered lists. id=unordered-sublist-example\n"
        input += "  A\n"
        input += "  B\n"
        input += "\n"
        input += "    B.1\n"
        input += "    B.2\n"
        input += "\n"
        input += "    - B.2.1\n"
        input += "    - B.2.2\n"
        input += "\n"
        input += "  C\n"
        input += "\n"
        input += "  - B.3\n"
        input += "\n"
        input += "    - B.3.1\n"
        input += "\n"
        input += "      - B 3.1.1\n"
        input += "\n"
        input += "    - B.3.2\n"
        input += "\n"
        input += "  - B.4\n"
        input += "\n"
        input += "  D\n"
        input += "!devel-end!\n"

        expected_update = "!devel! example caption=Nested unordered lists. id=unordered-sublist-example\n"
        expected_update += "  A\n"
        expected_update += "  B\n"
        expected_update += "\n"
        expected_update += "    B.1\n"
        expected_update += "    B.2\n"
        expected_update += "\n"
        expected_update += "      B.2.1\n"
        expected_update += "      B.2.2\n"
        expected_update += "\n"
        expected_update += "  C\n"
        expected_update += "\n"
        expected_update += "  - B.3\n"
        expected_update += "\n"
        expected_update += "    - B.3.1\n"
        expected_update += "\n"
        expected_update += "      - B 3.1.1\n"
        expected_update += "\n"
        expected_update += "    - B.3.2\n"
        expected_update += "\n"
        expected_update += "  - B.4\n"
        expected_update += "\n"
        expected_update += "  D\n"
        expected_update += "!devel-end!\n"

        index_start = input.find("- ")
        buffer_updated, index_block_start_end, token_list = process(input, index_start)

        token_first = token_list[0]
        token_second = token_list[1]

        self.assertEqual(4, token_first.index_indent)
        self.assertEqual(4, token_second.index_indent)

        self.assertEqual(index_start + 1, index_block_start_end)
        # self.assertEqual(expected_update, buffer_updated)
        self.assertEqual(input.find("\n  C"), token_second.index_start)
        self.assertEqual(input.find("\n  C"), token_second.index_end)


if __name__ == "__main__":
    unittest.main()

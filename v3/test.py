import re
import time

import codeblock
import heading
import quote
from my_token import EnumCentinal, Token

with open("core.md", "r") as f:
    content_file = f.read()


function_list = [
    heading.process,
    codeblock.process,
    quote.process,
]


buffer_search = "#`>"

pattern = re.compile("[" + re.escape(buffer_search) + "]")
index_current_char = 0

time_start = time.time()

list_of_tokens = []
while index_current_char < len(content_file):
    # print("Iteration")
    # print(f"{file_content[index_current_char]!r} : {index_current_char}")
    match = pattern.search(content_file[index_current_char:])

    if match is None:
        break

    index_char_matched = index_current_char + match.start()

    char_found = content_file[index_char_matched]
    index_delim = buffer_search.find(char_found)

    content_file, index_token_end, tokens_to_append = function_list[index_delim](
        content_file, index_char_matched
    )
    for token in tokens_to_append:
        token.index_appearance = len(list_of_tokens)
        list_of_tokens.append(token)

    index_current_char = index_token_end + 1


list_of_tokens.sort()

list_of_tokens.insert(
    0,
    Token(
        enum=EnumCentinal.StartFile,
        index_start=0,
        index_end=0,
        index_indent=0,
        index_appearance=0,
    ),
)


list_of_tokens.append(
    Token(
        enum=EnumCentinal.EndFile,
        index_start=len(content_file),
        index_end=len(content_file),
        index_indent=0,
        index_appearance=len(list_of_tokens),
    )
)
time_end = time.time()

for token in list_of_tokens:
    print(f"{token} : {content_file[token.index_start : token.index_end + 1]!r}")


print(f"Execution Time For 10k files: {(time_end - time_start) * 10e3:.3f} s")


def startFile(content_file: str, indent_level, token: Token):
    assert indent_level == 0
    assert token.enum == EnumCentinal.StartFile
    return 4, "Start File\n\n"


def endFile(content_file: str, indent_level, token: Token):
    assert indent_level == 4
    assert token.enum == EnumCentinal.EndFile
    return -4, "End File\n"


start_enums = {
    EnumCentinal.StartFile: startFile,
    heading.EnumHeadingStart.Single: heading.start,
    heading.EnumHeadingStart.Double: heading.start,
    heading.EnumHeadingStart.Triple: heading.start,
    heading.EnumHeadingStart.Quad: heading.start,
    heading.EnumHeadingStart.Quint: heading.start,
    heading.EnumHeadingStart.Sext: heading.start,
    codeblock.EnumCodeBlock.Start: codeblock.start,
    quote.EnumQuote.Start: quote.start,
}

end_enums = {
    EnumCentinal.EndFile: endFile,
    heading.EnumHeadingEnd.Single: heading.end,
    heading.EnumHeadingEnd.Double: heading.end,
    heading.EnumHeadingEnd.Triple: heading.end,
    heading.EnumHeadingEnd.Quad: heading.end,
    heading.EnumHeadingEnd.Quint: heading.end,
    heading.EnumHeadingEnd.Sext: heading.end,
    codeblock.EnumCodeBlock.End: codeblock.end,
    quote.EnumQuote.End: quote.end,
}

enum_pairs = {
    EnumCentinal.EndFile: EnumCentinal.StartFile,
    heading.EnumHeadingEnd.Single: heading.EnumHeadingStart.Single,
    heading.EnumHeadingEnd.Double: heading.EnumHeadingStart.Double,
    heading.EnumHeadingEnd.Triple: heading.EnumHeadingStart.Triple,
    heading.EnumHeadingEnd.Quad: heading.EnumHeadingStart.Quad,
    heading.EnumHeadingEnd.Quint: heading.EnumHeadingStart.Quint,
    heading.EnumHeadingEnd.Sext: heading.EnumHeadingStart.Sext,
    codeblock.EnumCodeBlock.End: codeblock.EnumCodeBlock.Start,
    quote.EnumQuote.End: quote.EnumQuote.Start,
}

index_token = 0
stack = []
content = ""
indent_level = 0

while index_token < len(list_of_tokens):

    token_curr = list_of_tokens[index_token]

    if token_curr.enum in start_enums:

        stack.append(token_curr)

        indent_level_update, content_addition = start_enums[token_curr.enum](
            content_file,
            indent_level,
            token_curr,
        )
        indent_level += indent_level_update
        content += content_addition

    if token_curr.enum in end_enums:
        # ensure that the current block type is closed
        assert enum_pairs[token_curr.enum] == stack[-1].enum
        stack.pop()

        indent_level_update, content_addition = end_enums[token_curr.enum](
            content_file,
            indent_level,
            token_curr,
        )
        indent_level += indent_level_update
        content += content_addition

    index_token += 1

assert len(stack) == 0
print(content)

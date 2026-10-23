import re
import sys
import time
from enum import Enum
from token import Token, EnumCentinal
from itertools import chain


import backtick
import error
import escape
import extension
import formatting
import links
import minus
import newline
import pound
import quote

start_time = time.time()
# with open("INSFVMomentumPressure.md", "r") as f:
with open("core.md", "r") as f:
    file_content = f.read()
end_time = time.time()

# When searching for delimiters we can start by searching the main list and
# then do a tree search to find each one based on starting character
open_delims = ["[", "`", ">", "#", "\n", "=", "+", "*", "~", "^", "@", "-", "\\"]


enum_list = [
    #    Enum("Quote", ["Quote"]),
]


start_time = time.time()

list_of_tokens = [
    Token(
        enum=EnumCentinal.BeginFile,
        index_start=0,
        index_end=-1,
    )
]
index_prev_token_end = 0
index_current_char = 0

buffer_search = "#\n`\\=+*~^@-[]()>!"

function_list = [
    pound.pound,
    newline.newline,
    backtick.backtick,
    escape.escape,
    formatting.underline,
    formatting.strong,
    formatting.emphasis,
    formatting.strikethrough,
    formatting.superscript,
    formatting.subscript,
    minus.minus,
    links.squareopen,
    links.squareclose,
    links.parenthesisopen,
    links.parenthesisclose,
    quote.quote,
    extension.extension,
]

pattern = re.compile("[" + re.escape(buffer_search) + "]")

while index_current_char < len(file_content):
    match = pattern.search(file_content[index_current_char:])

    if match is None:
        break

    char_found = file_content[index_current_char + match.start()]
    index_delim = buffer_search.find(char_found)

    index_token_start = index_current_char + match.start()
    index_token_end, enum_token = function_list[index_delim](
        file_content[index_token_start:]
    )

    if type(enum_token) == error.EnumError:
        print("Errored out")
        sys.exit()

    if enum_token is not None:
        list_of_tokens.append(
            Token(
                enum=enum_token,
                index_start=index_token_start,
                index_end=index_token_start + index_token_end,
            )
        )

    index_current_char += match.start() + index_token_end + 1

list_of_tokens.append(
    Token(
        enum=EnumCentinal.EndOfFile,
        index_start=len(file_content),
        index_end=len(file_content),
    )
)
end_time = time.time()

# for token in list_of_tokens:
#    print(f"{token} : {file_content[token.index_start : token.index_end + 1]!r}")
#
#
# print(f"Execution Time: {(end_time - start_time) * 10e3:.3f} s")
#

tokenization_dict = {
    type(pound.EnumPound(1)): pound.process_tokens,
}

index_token = 0
list_of_tokens_cleaned = [
    Token(
        enum=EnumCentinal.BeginFile,
        index_start=0,
        index_end=-1,
    )
]

start_time = time.time()
while index_token < len(list_of_tokens):
    token_current = list_of_tokens[index_token]
    if type(token_current.enum) in tokenization_dict:
        count_to_advance, tokens_to_append = tokenization_dict[
            type(token_current.enum)
        ](list_of_tokens, index_token, file_content)
        list_of_tokens_cleaned.extend(tokens_to_append)
    else:
        count_to_advance = 0

    index_token += count_to_advance + 1

list_of_tokens_cleaned.append(
    Token(
        enum=EnumCentinal.EndOfFile,
        index_start=len(file_content),
        index_end=len(file_content),
    )
)

for token in list_of_tokens_cleaned:
    print(f"{token} : {file_content[token.index_start : token.index_end + 1]!r}")

end_time = time.time()
print(f"Execution Time: {(end_time - start_time) * 10e3:.3f} s")

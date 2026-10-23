from enum import Enum

EnumQuote = Enum("Quote", ["Quote", "QuoteStart", "QuoteEnd"])


def process(buffer, index_char, prev_token):

    if index_char == 0 and buffer[index_char + 1] == " ":
        return buffer, index_char, index_char + 1, EnumQuote.Quote

    if index_char == len(buffer):
        return buffer, index_char, index_char, None

    if buffer[index_char + 1] != " ":
        return buffer, index_char, index_char, None

    indent_depth = buffer[index_char::-1].find("\n") - 1

    if indent_depth < 0:
        indent_depth = index_char
    index_paragraph_break = buffer[index_char:].find("\n\n")

    lines_quote = buffer[index_char : index_char + index_paragraph_break].split("\n")
    edited_buffer = ""

    for line in lines_quote:
        indent_depth_current_line = line.find(">")
        if indent_depth_current_line == indent_depth:
            edited_buffer += line.replace("> ", "  ", 1) + "\n"

    buffer = (
        buffer[:index_char]
        + edited_buffer
        + buffer[index_char + index_paragraph_break + 1 :]
    )
    return buffer, index_char, index_char + 1, EnumQuote.Quote

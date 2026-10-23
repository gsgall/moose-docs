import re
import time
from token import EnumCentinal, Token

import backtick
import escape
import extension
import formatting
import links
import list
import minus
import newline
import quote

import heading

with open("core.md", "r") as f:
    file_content = f.read()


list_of_tokens = [
    Token(
        enum=EnumCentinal.BeginFile,
        index_start=0,
        index_end=-1,
    )
]


buffer_search = "\n#\\`=+*~^@-[]>!0123456789"

# NOTE:
# based on the current implementation where on each character only the heading is provided makes it weird for nested blocks
# what could be better is that on each one we can have the function give a token marks its start location and
# also a token that provides it's ending so this would naturally solve the following issue
# currently we may have something like this
# [Token Quote, Token Quote, Token CodeBlock, Token ParagraphBreak]
# and this is valid but requires extra logic in the token processing step. It would be nice if we were able
# to have the tokenizer do this following
# [Token QuoteStart, Token QuoteStart, Token CodeBlockStart, Token CodeBlockEnd, Token QuoteEnd, TokenQuoteEnd]
# Maybe the way to do this is that we have the token collection method where each heading provides its start and end
# Then after the main token processing look we would end up with this sort of a thing
# [Token QuoteStart, Token QuoteEnd,  Token QuoteStart, Token QuoteEnd, Token CodeBlockStart, Token CodeBlockEnd]
# Now this is still not the right order for a stack based processing method to work for tokens and blocks
# At the end of the token processing look what we can then do is sort the tokens by their start indicies
# In this particular all of the diffenent ends will have the same start index into the buffer
# So we sort by indicies and in the case that they are the same we sort by reverse appearance order the order doing so would provide the following result
# [Token QuoteStart, Token QuoteStart, Token CodeBlockStart, Token CodeBlockEnd, Token QuoteEnd, TokenQuoteEnd]
# Doing it like this would also allow us to provide error messages where possible for certain environments
# Not this will actually not work with one special case and that is the case of nested lists

function_list = [
    newline.process,
    heading.process,
    escape.process,
    backtick.process,
    formatting.underlineProcess,
    formatting.strongProcess,
    formatting.emphasisProcess,
    formatting.strikethroughProcess,
    formatting.superscriptProcess,
    formatting.subscriptProcess,
    minus.process,
    links.squareOpenProcess,
    links.squareCloseProcess,
    quote.process,
    extension.process,
]

for i in range(10):
    function_list.append(list.orderedProcess)

pattern = re.compile("[" + re.escape(buffer_search) + "]")
index_current_char = 0

time_start = time.time()

while index_current_char < len(file_content):
    # print("Iteration")
    # print(f"{file_content[index_current_char]!r} : {index_current_char}")
    match = pattern.search(file_content[index_current_char:])

    if match is None:
        break

    index_char_matched = index_current_char + match.start()
    # print(f"{file_content[index_char_matched]!r} : {index_char_matched}")

    char_found = file_content[index_char_matched]
    index_delim = buffer_search.find(char_found)
    file_content, index_token_start, index_token_end, enum_type = function_list[
        index_delim
    ](file_content, index_char_matched, list_of_tokens[-1])

    if enum_type != None:
        list_of_tokens.append(
            Token(
                enum=enum_type,
                index_start=index_token_start,
                index_end=index_token_end,
            )
        )

    index_current_char = index_token_end + 1


list_of_tokens.append(
    Token(
        enum=EnumCentinal.EndOfFile,
        index_start=len(file_content),
        index_end=len(file_content),
    )
)

time_end = time.time()
for token in list_of_tokens:
    print(f"{token} : {file_content[token.index_start : token.index_end + 1]!r}")


print(f"Execution Time For 10k files: {(time_end - time_start) * 10e3:.3f} s")


def blockStart():
    return 4


def blockEnd():
    return -4


start_enums = {
    EnumCentinal.BeginFile: blockStart,
    backtick.EnumBackTick.Triple: blockStart,
    quote.EnumQuote.Quote: blockStart,
    heading.EnumHeading.Single: blockStart,
    heading.EnumHeading.Double: blockStart,
    heading.EnumHeading.Triple: blockStart,
    heading.EnumHeading.Quad: blockStart,
    heading.EnumHeading.Quint: blockStart,
    heading.EnumHeading.Sext: blockStart,
    list.EnumList.Unordered: blockStart,
    list.EnumList.Ordered: blockStart,
    # links.EnumLink.SquareOpen: blockStart,
    #    formatting.EnumFormatting.MonospaceStart: blockStart,
    #    formatting.EnumFormatting.UnderlineStart: blockStart,
    #    formatting.EnumFormatting.StrongStart: blockStart,
    #    formatting.EnumFormatting.EmphasisStart: blockStart,
    #    formatting.EnumFormatting.StrikethroughStart: blockStart,
    #    formatting.EnumFormatting.SuperScript: blockStart,
    #    formatting.EnumFormatting.SubScript: blockStart,
}
end_enums = {
    EnumCentinal.EndOfFile: blockEnd,
    newline.EnumNewLine.ParagraphBreak: blockEnd,
    newline.EnumNewLine.ParagraphBreak: blockEnd,
    newline.EnumNewLine.ParagraphBreak: blockEnd,
    newline.EnumNewLine.ParagraphBreak: blockEnd,
    newline.EnumNewLine.ParagraphBreak: blockEnd,
    newline.EnumNewLine.ParagraphBreak: blockEnd,
    newline.EnumNewLine.ParagraphBreak: blockEnd,
    newline.EnumNewLine.ParagraphBreak: blockEnd,
    newline.EnumNewLine.ParagraphBreak: blockEnd,
    newline.EnumNewLine.ParagraphBreak: blockEnd,
    # links.EnumLink.SquareOpen: blockEnd,
    #    formatting.EnumFormatting.MonospaceStart,
    #    formatting.EnumFormatting.UnderlineStart,
    #    formatting.EnumFormatting.StrongStart,
    #    formatting.EnumFormatting.EmphasisStart,
    #    formatting.EnumFormatting.StrikethroughStart,
    #    formatting.EnumFormatting.SuperScript,
    #    formatting.EnumFormatting.SubScript,
}

num_pairs = {
    EnumCentinal.BeginFile: EnumCentinal.EndOfFile,
    backtick.EnumBackTick.Triple: newline.EnumNewLine.ParagraphBreak,
    quote.EnumQuote.Quote: newline.EnumNewLine.ParagraphBreak,
    heading.EnumHeading.Single: newline.EnumNewLine.ParagraphBreak,
    heading.EnumHeading.Double: newline.EnumNewLine.ParagraphBreak,
    heading.EnumHeading.Triple: newline.EnumNewLine.ParagraphBreak,
    heading.EnumHeading.Quad: newline.EnumNewLine.ParagraphBreak,
    heading.EnumHeading.Quint: newline.EnumNewLine.ParagraphBreak,
    heading.EnumHeading.Sext: newline.EnumNewLine.ParagraphBreak,
    list.EnumList.Unordered: newline.EnumNewLine.ParagraphBreak,
    list.EnumList.Ordered: newline.EnumNewLine.ParagraphBreak,
}
index_token = 0
stack = []

content = ""
indent_level = 0

while index_token < len(list_of_tokens):
    token_curr = list_of_tokens[index_token]

    if token_curr.enum in start_enums:
        content += " " * indent_level + str(token_curr.enum) + "\n"
        stack.append(token_curr)
        indent_level += start_enums[token_curr.enum]()

    if token_curr.enum in end_enums:
        stack.pop()

        indent_level += end_enums[token_curr.enum]()
        content += " " * indent_level + str(token_curr.enum) + "\n"

    index_token += 1

print(len(stack))
print(content)

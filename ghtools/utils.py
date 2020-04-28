"""Module with miscellaneous utilities"""

import textwrap

def split_paragraphs(text):
    """Split text into paragraphs

    Returns a list of paragraphs - i.e., lines separated by one or more blank lines

    Args:
    text: string
    """
    text_stripped = text.strip()
    lines = text_stripped.splitlines()

    # paragraphs will be a list of lists of lines
    paragraphs = []

    cur_paragraph = []
    for line in lines:
        if line.strip():
            # line has more than spaces: it's part of the current paragraph
            cur_paragraph.append(line)
        else:
            # line is empty - i.e., a paragraph separator
            if cur_paragraph:
                paragraphs.append(cur_paragraph)
            cur_paragraph = []
    if cur_paragraph:
        paragraphs.append(cur_paragraph)

    return ['\n'.join(one_paragraph) for one_paragraph in paragraphs]

def fill_multiparagraph(text, width):
    """Fill a string that may contain multiple paragraphs

    Returns a new, filled string

    Args:
    text: string
    width: integer - width for filling
    """
    text_by_paragraph = split_paragraphs(text)
    # In the following, we use replace_whitespace=False to maintain line breaks in code
    # blocks (and any other intentional line breaks). However, this can mean more line
    # breaks than we'd really want.
    text_filled = [textwrap.fill(one_paragraph,
                                 width=width,
                                 break_long_words=False,
                                 replace_whitespace=False)
                   for one_paragraph in text_by_paragraph]
    return '\n\n'.join(text_filled)

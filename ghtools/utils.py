"""Module with miscellaneous utilities"""

import textwrap

def fill_multiparagraph(text, width):
    """Fill a string that may contain multiple paragraphs

    Returns a new, filled string

    Args:
    text: string
    width: integer - width for filling
    """
    # Note that we fill each line separately. The main point of this is to maintain line
    # breaks in code blocks (and any other intentional line breaks). However, this can
    # mean more line breaks than we'd really want.
    text_by_line = text.splitlines()
    text_filled = [textwrap.fill(one_line,
                                 width=width,
                                 break_long_words=False)
                   for one_line in text_by_line]
    return '\n'.join(text_filled)

"""Module with miscellaneous utilities"""

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

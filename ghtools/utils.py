"""Module with miscellaneous utilities"""

import textwrap
import re

# ------------------------------------------------------------------------
# Regular expressions
# ------------------------------------------------------------------------

# The first capture group matches any number of non-slash characters followed by a slash
# followed by any number of additional non-slash characters. This matches something like
# 'ORG/REPO'. The second capture group matches the pull request number. The final group
# ensures that the pull request number is followed by either a slash, a pound sign, or the
# end of string.
_PR_URL = re.compile(r'github\.com/([^/]+/[^/]+)/pull/([0-9]+)([/#]|$)')

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

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

def split_pr_url(url):
    """Given a URL of a GitHub Pull Request, return the repo and PR number

    Returns a tuple (repo, pr_number), where the repo is the full repository name, like
    ORG/REPO. If the given url doesn't look like the URL of a GitHub Pull Request, returns
    (None, None).
    """
    match = _PR_URL.search(url)
    if match is None:
        return (None, None)

    return (match.group(1), int(match.group(2)))

"""Class for holding a todo item extracted from a GitHub comment
"""

import re

# ------------------------------------------------------------------------
# Regular expressions
# ------------------------------------------------------------------------

# unordered list identifier: '-' or '+' or '*'
_UL = r"[\-\+\*]"

# ordered list identifier: one or more digits followed by '.' or ')'
_OL = r"\d+[\.\)]"

# one unordered or ordered list identifier; note that "(?:" starts a non-capturing group
_UOL = r"(?:" + _UL + r"|" + _OL + r")"

# list: either _OL or _UL followed by one or more whitespace characters
_LIST = _UOL + r"\s+"

# checkbox: '[ ]' followed by one or more whitespace characters
_CHECKBOX = r"\[ \]\s+"

# quote: '>' followed by any number of spaces
_QUOTE = r">\s*"

# any number of list or quote markers
_ANY_NUM_LIST_OR_QUOTE = r"(?:" + _LIST + r"|" + _QUOTE + r")*"

# a todo item on a line is given by:
# - at the start of the line, any amount of whitespace
# - any number of list or quote markers
# - a list indicator
# - an optional unordered or ordered list identifier without a space (this may be a bug in
#   GitHub's parsing, but we are following GitHub's behavior in this respect)
# - a checkbox
# - at least one whitespace character, followed by any other characters (this last piece
#   is put in a capture group)
_TODO = r"^\s*" + _ANY_NUM_LIST_OR_QUOTE + _LIST + _UOL + r"?" + _CHECKBOX + r"(\S.+)"
_TODO_RE = re.compile(_TODO)

# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

def search_line_for_todo(line):
    """Search a line of text for a todo item; return the found match

    If the line is a todo item, then returns the part of the line following the todo
    markdown syntax. If the line is not a todo item, returns None.

    Args:
    line: string - one line of text
    """
    match = _TODO_RE.search(line)
    if match is None:
        return None
    return match.group(1)

# ------------------------------------------------------------------------
# Begin class definition
# ------------------------------------------------------------------------

class CommentTodo:
    """Class for holding a todo item extracted from a GitHub comment"""

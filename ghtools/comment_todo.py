"""Class for holding a todo item extracted from a GitHub comment
"""

import re

# ------------------------------------------------------------------------
# Regular expressions
# ------------------------------------------------------------------------

# unordered list: '-' or '+' or '*' followed by one or more whitespace characters
_UL = r"[\-\+\*]\s+"

# ordered list: one or more digits followed by '.' or ')' followed by one or more
# whitespace characters
_OL = r"\d+[\.\)]\s+"

# list: either _ol or _ul; note that '(?:' starts a non-capturing group
_LIST = r"(?:" + _UL + r"|" + _OL + r")"

# checkbox: '[ ]' followed by one or more whitespace characters
_CHECKBOX = r"\[ \]\s+"

# a todo item on a line is given by:
# - at the start of the line, any amount of whitespace
# - a list indicator
# - a checkbox
# - at least one whitespace character, followed by any other characters (this last piece
#   is put in a capture group)
_TODO = r"^\s*" + _LIST + _CHECKBOX + r"(\S.+)"
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

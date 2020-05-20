"""Class for holding a todo item extracted from a GitHub comment
"""

import re
import textwrap
from ghtools.constants import LINE_WIDTH

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
#
# See https://github.github.com/gfm for GitHub's Markdown specification
#
# Here, we err on the side of being too general/accepting - i.e., we prefer false
# positives (calling something a checkbox when it really isn't) than false negatives
# (missing a true checkbox).
#
# Known issues:
# - The following are rendered as checkboxes by GitHub, but not by this regex:
#   - List item where the text is on the next line, like this:
#     *
#       [ ] todo
#
#     Here we are just parsing things line-by-line. So treating the above as a todo would
#     add a significant amount of work, and it seems very unlikely to come up in
#     practice. If this is an issue, a workaround would be to treat a line with some
#     number of spaces followed by '[ ] ' as a to do item, even though it technically
#     isn't.
#
# - Our regex is too general/accepting in the following ways:
#   - We accept any number of digits (GitHub limits the number of digits allowed in an
#     ordered list item - I think to 9)
#   - We accept any number of consecutive spaces (GitHub limits the number of consecutive
#     spaces - I think to 4)
#   - We accept something that looks like a tasklist item inside a multiline code block:
#     We parse line by line, detecting when we're inside a code block would add a
#     significant amount of work.
_TODO = r"^\s*" + _ANY_NUM_LIST_OR_QUOTE + _LIST + _UOL + r"?" + _CHECKBOX + r"(\S.+)"
_TODO_RE = re.compile(_TODO)

_OPTIONAL = r"^\s*(?:optional:|\[optional\]|\(optional\))\s*"
_OPTIONAL_RE = re.compile(_OPTIONAL, flags=re.IGNORECASE)

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
    """Class for holding a single todo item extracted from a GitHub comment"""

    def __init__(self, username, creation_date, url, text, extra_info=""):
        """Initialize a CommentTodo object.

        Args:
        username: string
        creation_date: datetime
        url: string
        text: string - this should be a single line, containing a single to do item,
           without the leading '- [ ]' or similar; typically, it will be the output from
           the search_line_for_todo function
        extra_info: string - optional extra information to print in the output
           This isn't included in 'text' because it gets inserted thoughtfully in the output
        """
        self._username = username
        self._creation_date = creation_date
        self._url = url
        self._text, self._is_optional = self._strip_optional_prefix(text)
        self._extra_info = extra_info

    def get_creation_date(self):
        """Return the creation date of this todo"""
        return self._creation_date

    def get_text(self):
        """Return the text of this todo"""
        if self.is_optional():
            return "[OPTIONAL] " + self._text
        return self._text

    def is_optional(self):
        """Returns true if this is an optional todo"""
        return self._is_optional

    @staticmethod
    def _strip_optional_prefix(text):
        """Determines if text has a prefix denoting optional; if so, strips it

        Returns a tuple: (normalized_text, is_optional)
        """
        stripped_text, num_replacements = _OPTIONAL_RE.subn("", text, count=1)
        is_optional = (num_replacements > 0)

        return stripped_text, is_optional

    def __repr__(self):
        return(type(self).__name__ +
               "(username={username}, "
               "creation_date={creation_date}, "
               "url={url}, "
               "text={text}, "
               "extra_info={extra_info})".format(username=repr(self._username),
                                                 creation_date=repr(self._creation_date),
                                                 url=repr(self._url),
                                                 text=repr(self.get_text()),
                                                 extra_info=repr(self._extra_info)))

    def __str__(self):
        text_as_list_item = "- {}".format(self.get_text())
        text_wrapped = textwrap.fill(text_as_list_item,
                                     width=LINE_WIDTH,
                                     subsequent_indent='  ',
                                     break_long_words=False)
        return("{text}\n  ({username} at {creation_date}, <{url}>)".format(
            text=text_wrapped,
            username=self._username,
            creation_date=self._creation_date,
            url=self._url))

    def __eq__(self, other):
        if isinstance(other, CommentTodo):
            return self.__dict__ == other.__dict__
        return NotImplemented

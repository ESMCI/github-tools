"""Class for holding information about a single GitHub comment
"""

import textwrap
from enum import Enum, auto
from ghtools.comment_todo import search_line_for_todo, CommentTodo
from ghtools.utils import fill_multiparagraph
from ghtools.constants import LINE_WIDTH, INDENT_LEVEL

class CommentType(Enum):
    """Valid types for the comment_type argument to the Comment constructor"""
    PR_BODY_COMMENT = auto()
    CONVERSATION_COMMENT = auto()
    PR_LINE_COMMENT = auto()
    PR_REVIEW_COMMENT = auto()

class Comment:
    """Class for holding information about a single GitHub comment"""

    def __init__(self, comment_type, username, creation_date, url, content):
        """Initialize a comment object.

        Args:
        comment_type: one of the options in CommentType (e.g., CommentType.CONVERSATION_COMMENT)
        username: string
        creation_date: datetime
        url: string
        content: string
        """
        self._type = comment_type
        self._username = username
        self._creation_date = creation_date
        self._url = url
        self._content = content

    def get_username(self):
        """Return the username that authored this comment"""
        return self._username

    def get_creation_date(self):
        """Return the creation date of this comment"""
        return self._creation_date

    def get_todos(self):
        """Return a list of all lines in the comment that represent todos

        Returns a list of CommentTodo objects (or an empty list if there are no todos in
        this comment)
        """
        todos = []
        for line in self._content.splitlines():
            todo_text = search_line_for_todo(line)
            if todo_text is not None:
                todos.append(CommentTodo(
                    username=self._username,
                    creation_date=self._creation_date,
                    url=self._url,
                    text=todo_text))

        return todos

    def __repr__(self):
        return(type(self).__name__ +
               "(comment_type={comment_type}, "
               "username={username}, "
               "creation_date={creation_date}, "
               "url={url}, "
               "content={content})".format(comment_type=str(self._type),
                                           username=repr(self._username),
                                           creation_date=repr(self._creation_date),
                                           url=repr(self._url),
                                           content=repr(self._content)))

    def __str__(self):
        type_as_str = {CommentType.PR_BODY_COMMENT: "PR body",
                       CommentType.CONVERSATION_COMMENT: "Conversation comment",
                       CommentType.PR_LINE_COMMENT: "PR line comment",
                       CommentType.PR_REVIEW_COMMENT: "PR review comment"}
        content_filled = fill_multiparagraph(self._content, LINE_WIDTH-INDENT_LEVEL)
        return("{comment_type} by {username} on {creation_date} ({url}):\n"
               "{content}".format(comment_type=type_as_str[self._type],
                                  username=self._username,
                                  creation_date=self._creation_date,
                                  url=self._url,
                                  content=textwrap.indent(content_filled, INDENT_LEVEL*" ")))

    def __eq__(self, other):
        if isinstance(other, Comment):
            return self.__dict__ == other.__dict__
        return NotImplemented

"""Class for holding information about a single GitHub comment
"""

import textwrap
from ghtools.comment_todo import search_line_for_todo, CommentTodo
from ghtools.utils import fill_multiparagraph
from ghtools.constants import LINE_WIDTH, INDENT_LEVEL

# The Comment class should not be instantiated directly. Instead, one of its child classes
# should be instantiated (see below for the child classes).
class Comment:
    """Class for holding information about a single GitHub comment"""

    def __init__(self, username, creation_date, url, content):
        """Initialize a comment object.

        Args:
        username: string
        creation_date: datetime
        url: string
        content: string
        """
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

    # This method needs to be implemented by each derived class
    def _type_as_str(self):
        """Return the type of this comment as a string"""
        raise NotImplementedError

    def __repr__(self):
        return(type(self).__name__ +
               "(username={username}, "
               "creation_date={creation_date}, "
               "url={url}, "
               "content={content})".format(username=repr(self._username),
                                           creation_date=repr(self._creation_date),
                                           url=repr(self._url),
                                           content=repr(self._content)))

    def __str__(self):
        content_filled = fill_multiparagraph(self._content, LINE_WIDTH-INDENT_LEVEL)
        return("{comment_type} by {username} on {creation_date} ({url}):\n"
               "{content}".format(comment_type=self._type_as_str(),
                                  username=self._username,
                                  creation_date=self._creation_date,
                                  url=self._url,
                                  content=textwrap.indent(content_filled, INDENT_LEVEL*" ")))

    def __eq__(self, other):
        if isinstance(other, Comment):
            return self.__dict__ == other.__dict__
        return NotImplemented

class PRBodyComment(Comment):
    """Class for holding a PR body comment"""
    def _type_as_str(self):
        return "PR body"

class ConversationComment(Comment):
    """Class for holding a conversation comment"""
    def _type_as_str(self):
        return "Conversation comment"

class PRReviewComment(Comment):
    """Class for holding a PR review comment"""
    def _type_as_str(self):
        return "PR review comment"

class PRLineComment(Comment):
    """Class for holding a PR line comment"""
    def __init__(self, username, creation_date, url, content, path):
        """Initialize a PRLineComment object

        Args: Same as for Comment base class except:
        path: string - path to file that comment applies to
        """
        super().__init__(username=username,
                         creation_date=creation_date,
                         url=url,
                         content=content)
        self._path = path

    def _type_as_str(self):
        return "PR line comment"

    def __repr__(self):
        return(type(self).__name__ +
               "(username={username}, "
               "creation_date={creation_date}, "
               "url={url}, "
               "content={content}, "
               "path={path})".format(username=repr(self._username),
                                     creation_date=repr(self._creation_date),
                                     url=repr(self._url),
                                     content=repr(self._content),
                                     path=repr(self._path)))

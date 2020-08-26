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

    def __init__(self, username, time_info, url, content):
        """Initialize a comment object.

        Args:
        username: string
        time_info: CommentTime
        url: string
        content: string
        """
        self._username = username
        self._time_info = time_info
        self._url = url
        self._content = content

    def get_username(self):
        """Return the username that authored this comment"""
        return self._username

    def get_time_info(self):
        """Return the time info object associated with this comment

        Returns a CommentTime object
        """
        return self._time_info

    def get_creation_date(self):
        """Return the creation date of this comment"""
        return self._time_info.get_creation_time()

    def get_todos(self, completed=False):
        """Return a list of all lines in the comment that represent todos

        Returns a list of CommentTodo objects (or an empty list if there are no todos in
        this comment)

        Args:
        completed: boolean - whether to look for completed todos instead of incomplete todos
        """
        todos = []
        for line in self._content.splitlines():
            todo_text = search_line_for_todo(line, completed=completed)
            if todo_text is not None:
                todos.append(CommentTodo(
                    username=self._username,
                    time_info=self._time_info,
                    url=self._url,
                    text=todo_text,
                    extra_info=self._get_extra_info(),
                    completed=completed))

        return todos

    # This method needs to be implemented by each derived class
    def _type_as_str(self):
        """Return the type of this comment as a string"""
        raise NotImplementedError

    # This method can be overridden by derived classes
    def _get_extra_info(self):
        # pylint: disable=no-self-use
        """Return a string containing any extra info associated with this comment, or None"""
        return None

    def __repr__(self):
        return(type(self).__name__ +
               "(username={username}, "
               "time_info={time_info}, "
               "url={url}, "
               "content={content})".format(username=repr(self._username),
                                           time_info=repr(self._time_info),
                                           url=repr(self._url),
                                           content=repr(self._content)))

    def __str__(self):
        content_filled = fill_multiparagraph(self._content, LINE_WIDTH-INDENT_LEVEL)
        return("{comment_type} by {username} ({time_info}) <{url}>:\n"
               "{content}".format(comment_type=self._type_as_str(),
                                  username=self._username,
                                  time_info=self._time_info,
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
    def __init__(self, username, time_info, url, content, path):
        """Initialize a PRLineComment object

        Args: Same as for Comment base class except:
        path: string - path to file that comment applies to
        """
        super().__init__(username=username,
                         time_info=time_info,
                         url=url,
                         content=content)
        self._path = path

    def _type_as_str(self):
        return "PR line comment ({})".format(self._path)

    def _get_extra_info(self):
        return self._path

    def __repr__(self):
        return(type(self).__name__ +
               "(username={username}, "
               "time_info={time_info}, "
               "url={url}, "
               "content={content}, "
               "path={path})".format(username=repr(self._username),
                                     time_info=repr(self._time_info),
                                     url=repr(self._url),
                                     content=repr(self._content),
                                     path=repr(self._path)))

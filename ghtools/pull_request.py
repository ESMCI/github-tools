"""Class for holding information about a GitHub Pull Request
"""

import textwrap
from ghtools.comment import Comment, CommentType
from ghtools.utils import fill_multiparagraph
from ghtools.constants import LINE_WIDTH, INDENT_LEVEL

class PullRequest:
    """Class for holding information about a GitHub Pull Request"""

    def __init__(self, pr_number, title, username, creation_date, url, body, comments):
        """Initialize a PullRequest object.

        Args:
        pr_number: integer
        title: string
        username: string
        creation_date: datetime
        url: string
        body: string
        comments: iterable of Comments
            Note that this is shallow-copied
        """
        self._pr_number = pr_number
        self._title = title
        self._username = username
        self._creation_date = creation_date
        self._url = url
        self._body = body
        self._comments = sorted(comments, key=lambda c: c.get_creation_date())

    def get_todos(self):
        """Return a list of all lines in the PR body and all comments that represent todos

        Returns a list of CommentTodo objects
        """
        todos = []
        todos.extend(self._body_as_comment().get_todos())
        for one_comment in self._comments:
            todos.extend(one_comment.get_todos())
        return todos

    def _body_as_comment(self):
        """Return a Comment object representing the body of this PullRequest"""
        return Comment(comment_type=CommentType.CONVERSATION_COMMENT,
                       username=self._username,
                       creation_date=self._creation_date,
                       url=self._url,
                       content=self._body)

    def __repr__(self):
        return(type(self).__name__ +
               "(pr_number={pr_number}, "
               "title={title}, "
               "username={username}, "
               "creation_date={creation_date}, "
               "url={url}, "
               "body={body}, "
               "comments={comments})".format(
                   pr_number=repr(self._pr_number),
                   title=repr(self._title),
                   username=repr(self._username),
                   creation_date=repr(self._creation_date),
                   url=repr(self._url),
                   body=repr(self._body),
                   comments=repr(self._comments)))

    def __str__(self):
        body_filled = fill_multiparagraph(self._body, LINE_WIDTH-INDENT_LEVEL)
        my_str = ("PR #{pr_number}: '{title}' by {username} on {creation_date} ({url}):\n"
                  "{body}".format(pr_number=self._pr_number,
                                  title=self._title,
                                  username=self._username,
                                  creation_date=self._creation_date,
                                  url=self._url,
                                  body=textwrap.indent(body_filled, INDENT_LEVEL*" ")))

        for comment in self._comments:
            my_str += "\n\n" + str(comment)

        return my_str

    def __eq__(self, other):
        if isinstance(other, PullRequest):
            return self.__dict__ == other.__dict__
        return NotImplemented

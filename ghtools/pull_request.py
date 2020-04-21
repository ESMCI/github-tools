"""Class for holding information about a GitHub Pull Request
"""

import textwrap

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
            Note that this is shallow-copied; it can be immutable
        """
        self._pr_number = pr_number
        self._title = title
        self._username = username
        self._creation_date = creation_date
        self._url = url
        self._body = body
        self._comments = comments

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
        indent_level = 4

        my_str = ("PR #{pr_number}: '{title}' by {username} on {creation_date} ({url}):\n"
                  "{body}".format(pr_number=self._pr_number,
                                  title=self._title,
                                  username=self._username,
                                  creation_date=self._creation_date,
                                  url=self._url,
                                  body=textwrap.indent(self._body, indent_level*" ")))

        for comment in self._comments:
            my_str += "\n\n" + textwrap.indent(str(comment), indent_level*" ")

        return my_str

    def __eq__(self, other):
        if isinstance(other, PullRequest):
            return self.__dict__ == other.__dict__
        return NotImplemented

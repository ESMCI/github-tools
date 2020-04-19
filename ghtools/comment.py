"""Class for holding information about a single GitHub comment
"""

import textwrap

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
        return("Comment by {username} on {creation_date} ({url}):\n"
               "{content}".format(username=self._username,
                                  creation_date=self._creation_date,
                                  url=self._url,
                                  content=textwrap.indent(self._content, 4*" ")))

    def __eq__(self, other):
        if isinstance(other, Comment):
            return self.__dict__ == other.__dict__
        return NotImplemented

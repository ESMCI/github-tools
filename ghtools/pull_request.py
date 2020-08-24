"""Class for holding information about a GitHub Pull Request
"""

from ghtools.comment import PRBodyComment

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
        self._comments = ([self._body_as_comment()] +
                          sorted(comments, key=lambda c: c.get_creation_date()))

    def get_content(self, filter_username=None):
        """Return a string representation of this PullRequest

        If filter_username is provided (not None), then it should be a string; only
        comments authored by that username are included in the returned string.
        """
        my_str = self.get_header()

        for comment in self._filter_comments(filter_username=filter_username):
            my_str += "\n\n" + str(comment)

        return my_str

    def get_header(self):
        """Return a string giving the header for this PullRequest
        """
        return ("PR #{pr_number}: '{title}' by {username} on {creation_date} ({url}):".format(
            pr_number=self._pr_number,
            title=self._title,
            username=self._username,
            creation_date=self._creation_date,
            url=self._url))

    def get_todos(self, completed=False, filter_username=None):
        """Return a list of all lines in the PR body and all comments that represent todos

        Returns a list of CommentTodo objects; all required todos come first, followed by
        optional todos; within each category (required and optional), they are sorted by
        date.

        Args:
        completed: boolean - whether to look for completed todos instead of incomplete todos
        filter_username: if provided (not None), then it should be a string; only todos
            authored by that username are returned.
        """
        todos = []
        for one_comment in self._filter_comments(filter_username=filter_username):
            todos.extend(one_comment.get_todos(completed=completed))
        todos.sort(key=lambda t: (t.is_optional(), t.get_creation_date()))
        return todos

    def _filter_comments(self, filter_username=None):
        """Return a list of comments, possibly filtered by some attributes

        Args:
        filter_username: string or None - if provided, only comments authored by this
        username are included
        """
        return [c for c in self._comments
                if (filter_username is None or c.get_username() == filter_username)]

    def _body_as_comment(self):
        """Return a Comment object representing the body of this PullRequest"""
        return PRBodyComment(username=self._username,
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
                   # In the following, note that we ignore the first comment, which is the PR body:
                   comments=repr(self._comments[1:])))

    def __str__(self):
        return self.get_content()

    def __eq__(self, other):
        if isinstance(other, PullRequest):
            return self.__dict__ == other.__dict__
        return NotImplemented

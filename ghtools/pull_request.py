"""Class for holding information about a GitHub Pull Request
"""

from ghtools.comment import PRBodyComment

class PullRequest:
    """Class for holding information about a GitHub Pull Request"""

    def __init__(self, pr_number, title, username, time_info, url, body, comments):
        """Initialize a PullRequest object.

        Args:
        pr_number: integer
        title: string
        username: string
        time_info: CommentTime
        url: string
        body: string
        comments: iterable of Comments
            Note that this is shallow-copied
        """
        self._pr_number = pr_number
        self._title = title
        self._username = username
        self._time_info = time_info
        self._url = url
        self._body = body
        self._comments = ([self._body_as_comment()] +
                          sorted(comments, key=lambda c: c.get_creation_date()))

    def get_content(self, filter_username=None, created_since_time=None, updated_since_time=None):
        """Return a string representation of this PullRequest

        If filter_username is provided (not None), then it should be a string; only
        comments authored by that username are included in the returned string.

        If created_since_time is provided (not None), then it should be a datetime.datetime
        object; only comments created on or after that time are included.

        If updated_since_time is provided (not None), then it should be a datetime.datetime
        object; only comments updated on or after that time are included.
        """
        my_str = self.get_header()

        for comment in self._filter_comments(filter_username=filter_username,
                                             created_since_time=created_since_time,
                                             updated_since_time=updated_since_time):
            my_str += "\n\n" + str(comment)

        return my_str

    def get_header(self):
        """Return a string giving the header for this PullRequest
        """
        return ("PR #{pr_number}: '{title}' by {username} ({time_info}) <{url}>:".format(
            pr_number=self._pr_number,
            title=self._title,
            username=self._username,
            time_info=self._time_info,
            url=self._url))

    def get_todos(self, completed=False,
                  filter_username=None, created_since_time=None, updated_since_time=None):
        """Return a list of all lines in the PR body and all comments that represent todos

        Returns a list of CommentTodo objects; all required todos come first, followed by
        optional todos; within each category (required and optional), they are sorted by
        date.

        Args:
        completed: boolean - whether to look for completed todos instead of incomplete todos
        filter_username: if provided (not None), then it should be a string; only todos
            authored by that username are returned.
        created_since_time: if provided (not None), then it should be a datetime.datetime
            object; only comments created on or after that time are included.
        updated_since_time: if provided (not None), then it should be a datetime.datetime
            object; only comments updated on or after that time are included.
        """
        todos = []
        for one_comment in self._filter_comments(filter_username=filter_username,
                                                 created_since_time=created_since_time,
                                                 updated_since_time=updated_since_time):
            todos.extend(one_comment.get_todos(completed=completed))
        todos.sort(key=lambda t: (t.is_optional(), t.get_creation_date()))
        return todos

    def _filter_comments(self, filter_username, created_since_time, updated_since_time):
        """Return a list of comments, possibly filtered by some attributes

        Args:
        filter_username: string or None - if provided (not None), only comments authored
            by this username are included
        created_since_time: datetime.datetime or None - if provided (not None), only comments
            created on or after this time are included
        updated_since_time: datetime.datetime or None - if provided (not None), only comments
            updated on or after this time are included
        """
        # pylint: disable=line-too-long
        return [c for c in self._comments
                if ((filter_username is None or c.get_username() == filter_username) and
                    (created_since_time is None or c.get_time_info().created_since(created_since_time)) and
                    (updated_since_time is None or c.get_time_info().updated_since(updated_since_time)))]

    def _body_as_comment(self):
        """Return a Comment object representing the body of this PullRequest"""
        # There doesn't seem to be a way to get the last-updated time of the body comment
        # itself, so as a conservative guess, we use the last updated time of the PR as a
        # whole.
        return PRBodyComment(username=self._username,
                             time_info=self._time_info.as_guess(),
                             url=self._url,
                             content=self._body)

    def __repr__(self):
        return(type(self).__name__ +
               "(pr_number={pr_number}, "
               "title={title}, "
               "username={username}, "
               "time_info={time_info}, "
               "url={url}, "
               "body={body}, "
               "comments={comments})".format(
                   pr_number=repr(self._pr_number),
                   title=repr(self._title),
                   username=repr(self._username),
                   time_info=repr(self._time_info),
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

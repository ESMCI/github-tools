"""Class for holding the time information for a GitHub comment
"""

class CommentTime:
    """Class for holding the time information for a GitHub comment"""

    def __init__(self, creation_time, last_updated_time=None):
        """Initialize a CommentTime object

        Args:
        creation_time: datetime.datetime
        last_updated_time: datetime.datetime or None. None implies that we don't have any
            last-updated information for this comment. (It does NOT imply that the
            last-updated time is the same as the creation time.)
        """
        if last_updated_time and last_updated_time < creation_time:
            raise ValueError("last_updated_time cannot be before creation_time")
        self._creation_time = creation_time
        self._last_updated_time = last_updated_time

    def created_since(self, time):
        """Returns a boolean saying whether this comment was created on or after the given time

        Args:
        time: datetime.datetime
        """
        return self._creation_time >= time

    def updated_since(self, time):
        """Returns a boolean saying whether this comment was updated on or after the given time

        If the last updated time of this object is None (i.e., unknown), then this always
        returns True.

        Args:
        time: datetime.datetime
        """
        if self._last_updated_time is None:
            return True
        return self._last_updated_time >= time

    def __repr__(self):
        return(type(self).__name__ +
               "(creation_time={creation_time}, "
               "last_updated_time={last_updated_time})".format(
                   creation_time=repr(self._creation_time),
                   last_updated_time=repr(self._last_updated_time)))

    def __str__(self):
        if self._last_updated_time is None:
            updated_string = "last updated: unknown"
        elif self._last_updated_time == self._creation_time:
            updated_string = "last updated: never"
        else:
            updated_string = "last updated: {}".format(self._last_updated_time)
        return("at {creation_time}, {updated_string}".format(
            creation_time=self._creation_time,
            updated_string=updated_string))

    def __eq__(self, other):
        if isinstance(other, CommentTime):
            return self.__dict__ == other.__dict__
        return NotImplemented

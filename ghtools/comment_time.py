"""Class for holding the time information for a GitHub comment
"""

class CommentTime:
    """Class for holding the time information for a GitHub comment"""

    def __init__(self, creation_time, last_updated_time, updated_time_is_guess=False):
        """Initialize a CommentTime object

        Args:
        creation_time: datetime.datetime
        last_updated_time: datetime.datetime
        updated_time_is_guess: boolean - whether last_updated_time is just a guess rather
            than known
        """
        if last_updated_time < creation_time:
            raise ValueError("last_updated_time cannot be before creation_time")
        self._creation_time = creation_time
        self._last_updated_time = last_updated_time
        self._updated_time_is_guess = updated_time_is_guess

    def created_since(self, time):
        """Returns a boolean saying whether this comment was created on or after the given time

        Args:
        time: datetime.datetime
        """
        return self._creation_time >= time

    def updated_since(self, time):
        """Returns a boolean saying whether this comment was updated on or after the given time

        This uses the object's last updated time, even if that is a guess

        Args:
        time: datetime.datetime
        """
        return self._last_updated_time >= time

    def get_creation_time(self):
        """Return the creation time of this comment"""
        return self._creation_time

    def as_guess(self):
        """Create a copy of self, but with updated time as a guess"""
        return self.__class__(creation_time=self._creation_time,
                              last_updated_time=self._last_updated_time,
                              updated_time_is_guess=True)

    def __repr__(self):
        return(type(self).__name__ +
               "(creation_time={creation_time}, "
               "last_updated_time={last_updated_time}, "
               "updated_time_is_guess={updated_time_is_guess})".format(
                   creation_time=repr(self._creation_time),
                   last_updated_time=repr(self._last_updated_time),
                   updated_time_is_guess=repr(self._updated_time_is_guess)))

    def __str__(self):
        if self._updated_time_is_guess:
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

#!/usr/bin/env python

"""Unit tests for Comment class
"""

import unittest
import datetime
from ghtools.comment import Comment, CommentType

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

class TestComment(unittest.TestCase):
    """Tests of Comment class"""

    @staticmethod
    def _create_comment():
        """Returns a basic Comment object"""
        return Comment(comment_type=CommentType.PR_LINE_COMMENT,
                       username="me",
                       creation_date=datetime.datetime(2020, 1, 1),
                       url="https://github.com/org/repo/1#issuecomment-2",
                       content="My content")

    def test_repr_resultsInEqualObject(self):
        """The repr of a Comment object should result in an equivalent object"""
        c = self._create_comment()
        # pylint: disable=eval-used
        c2 = eval(repr(c))
        self.assertEqual(c2, c)

    def test_str_works(self):
        """Just make sure that the str method runs successfully"""
        c = self._create_comment()
        _ = str(c)

if __name__ == '__main__':
    unittest.main()

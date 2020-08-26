#!/usr/bin/env python

"""Unit tests for CommentTime class
"""

import unittest
import datetime
from ghtools.comment_time import CommentTime

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

class TestCommentTime(unittest.TestCase):
    """Tests of CommentTime class"""

    def test_repr_resultsInEqualObject(self):
        """repr of a CommentTime object should result in an equiv. object"""
        # This ability to recreate the object isn't a strict requirement, so if it gets
        # hard to maintain, we can drop it.
        ct = CommentTime(datetime.datetime(2020, 1, 1),
                         datetime.datetime(2020, 1, 2))
        # pylint: disable=eval-used
        ct2 = eval(repr(ct))
        self.assertEqual(ct2, ct)

    def test_str_works(self):
        # pylint: disable=no-self-use
        """Just make sure that the str method runs successfully"""
        ct = CommentTime(datetime.datetime(2020, 1, 1),
                         datetime.datetime(2020, 1, 2))
        _ = str(ct)

    def test_createdSince_true(self):
        """Test created_since method when it should be true"""
        ct = CommentTime(datetime.datetime(2020, 1, 2),
                         datetime.datetime(2020, 1, 4))
        is_created_since = ct.created_since(datetime.datetime(2020, 1, 1))
        self.assertTrue(is_created_since)

    def test_createdSince_false(self):
        """Test created_since method when it should be false"""
        ct = CommentTime(datetime.datetime(2020, 1, 2),
                         datetime.datetime(2020, 1, 4))
        is_created_since = ct.created_since(datetime.datetime(2020, 1, 3))
        self.assertFalse(is_created_since)

    def test_updatedSince_true(self):
        """Test updated_since method when it should be true"""
        ct = CommentTime(datetime.datetime(2020, 1, 2),
                         datetime.datetime(2020, 1, 4))
        is_updated_since = ct.updated_since(datetime.datetime(2020, 1, 3))
        self.assertTrue(is_updated_since)

    def test_updatedSince_false(self):
        """Test updated_since method when it should be false"""
        ct = CommentTime(datetime.datetime(2020, 1, 2),
                         datetime.datetime(2020, 1, 4))
        is_updated_since = ct.updated_since(datetime.datetime(2020, 1, 5))
        self.assertFalse(is_updated_since)

    def test_as_guess(self):
        """Test the as_guess method"""
        # pylint: disable=protected-access
        ct = CommentTime(datetime.datetime(2020, 1, 2),
                         datetime.datetime(2020, 1, 4),
                         updated_time_is_guess=False)
        ct2 = ct.as_guess()
        self.assertEqual(ct2._creation_time, ct._creation_time)
        self.assertEqual(ct2._last_updated_time, ct._last_updated_time)
        self.assertTrue(ct2._updated_time_is_guess)

if __name__ == '__main__':
    unittest.main()

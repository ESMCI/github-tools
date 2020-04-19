#!/usr/bin/env python

"""Unit tests for PullRequest class
"""

import unittest
import datetime
from ghtools.pull_request import PullRequest
from ghtools.comment import Comment

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

class TestPullRequest(unittest.TestCase):
    """Tests of PullRequest class"""

    @staticmethod
    def _simple_comment(comment_id, content):
        """Return a Comment object with some hard-coded pieces

        Args:
        comment_id (integer): used in URL
        content (string)
        """
        return Comment(username="you",
                       creation_date=datetime.datetime(2020, 1, 2),
                       url="https://github.com/org/repo/1#comment-{c_id}".format(c_id=comment_id),
                       content=content)

    @staticmethod
    def _create_pr():
        """Returns a basic PullRequest object"""
        return PullRequest(pr_number=17,
                           title="My title",
                           username="me",
                           creation_date=datetime.datetime(2020, 1, 1),
                           url="https://github.com/org/repo/1",
                           body="PR body",
                           conversation_comments=(TestPullRequest._simple_comment(1, "comment 1"),
                                                  TestPullRequest._simple_comment(2, "comment 2")),
                           review_comments=(TestPullRequest._simple_comment(3, "rc 1"),
                                            TestPullRequest._simple_comment(4, "rc 2"),
                                            TestPullRequest._simple_comment(5, "rc 3")))

    def test_repr_resultsInEqualObject(self):
        """The repr of a PullRequest object should result in an equivalent object"""
        pr = self._create_pr()
        # pylint: disable=eval-used
        pr2 = eval(repr(pr))
        self.assertEqual(pr2, pr)

    def test_str_works(self):
        """Just make sure that the str method runs successfully"""
        pr = self._create_pr()
        _ = str(pr)

if __name__ == '__main__':
    unittest.main()

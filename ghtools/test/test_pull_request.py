#!/usr/bin/env python

"""Unit tests for PullRequest class
"""

import unittest
import datetime
from ghtools.pull_request import PullRequest
from ghtools.comment import Comment, CommentType

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

class TestPullRequest(unittest.TestCase):
    """Tests of PullRequest class"""

    @staticmethod
    def _simple_comment(comment_type, comment_id, content):
        """Return a Comment object with some hard-coded pieces

        Args:
        comment_type (one of the options in CommentType (e.g., CommentType.CONVERSATION_COMMENT))
        comment_id (integer): used in URL
        content (string)
        """
        return Comment(comment_type=comment_type,
                       username="you",
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
                           comments=(TestPullRequest._simple_comment(
                               CommentType.CONVERSATION_COMMENT, 1, "comment"),
                                     TestPullRequest._simple_comment(
                                         CommentType.PR_LINE_COMMENT, 2, "line comment"),
                                     TestPullRequest._simple_comment(
                                         CommentType.PR_REVIEW_COMMENT, 3, "review comment")))

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

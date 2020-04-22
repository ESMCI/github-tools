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
    def _simple_comment(comment_type, comment_id, content, creation_date=None):
        """Return a Comment object with some hard-coded pieces

        Args:
        comment_type (one of the options in CommentType (e.g., CommentType.CONVERSATION_COMMENT))
        comment_id (integer): used in URL
        content (string)
        creation_date (datetime): if not given, uses a hard-coded creation_date
        """
        if creation_date is None:
            creation_date = datetime.datetime(2020, 1, 2)
        return Comment(comment_type=comment_type,
                       username="you",
                       creation_date=creation_date,
                       url="https://github.com/org/repo/1#comment-{c_id}".format(c_id=comment_id),
                       content=content)

    @staticmethod
    def _create_pr(comments=None):
        """Returns a basic PullRequest object

        If comments is given, it should be a list of CommentType objects; otherwise, a
        hard-coded list of comments is used.
        """
        if comments is None:
            comments = (TestPullRequest._simple_comment(
                CommentType.CONVERSATION_COMMENT, 1, "comment"),
                        TestPullRequest._simple_comment(
                            CommentType.PR_LINE_COMMENT, 2, "line comment"),
                        TestPullRequest._simple_comment(
                            CommentType.PR_REVIEW_COMMENT, 3, "review comment"))

        return PullRequest(pr_number=17,
                           title="My title",
                           username="me",
                           creation_date=datetime.datetime(2020, 1, 1),
                           url="https://github.com/org/repo/1",
                           body="PR body",
                           comments=comments)

    def test_repr_resultsInEqualObject(self):
        """The repr of a PullRequest object should result in an equivalent object"""
        # This ability to recreate the object isn't a strict requirement, so if it gets
        # hard to maintain, we can drop it.
        pr = self._create_pr()
        # pylint: disable=eval-used
        pr2 = eval(repr(pr))
        self.assertEqual(pr2, pr)

    def test_str_works(self):
        """Just make sure that the str method runs successfully"""
        pr = self._create_pr()
        _ = str(pr)

    def test_commentsAreSorted(self):
        """Comments should be sorted by date"""
        c1 = self._simple_comment(CommentType.CONVERSATION_COMMENT, 1, "comment",
                                  creation_date=datetime.datetime(2020, 1, 1))
        c2 = self._simple_comment(CommentType.CONVERSATION_COMMENT, 2, "another comment",
                                  creation_date=datetime.datetime(2020, 1, 3))
        c3 = self._simple_comment(CommentType.PR_LINE_COMMENT, 3, "line comment",
                                  creation_date=datetime.datetime(2020, 1, 2))
        c4 = self._simple_comment(CommentType.PR_LINE_COMMENT, 4, "another line comment",
                                  creation_date=datetime.datetime(2020, 1, 5))
        c5 = self._simple_comment(CommentType.PR_REVIEW_COMMENT, 5, "review comment",
                                  creation_date=datetime.datetime(2020, 1, 4))

        pr = self._create_pr(comments=(c1, c2, c3, c4, c5))
        #pylint: disable=protected-access
        self.assertEqual(pr._comments, [c1, c3, c2, c5, c4])

if __name__ == '__main__':
    unittest.main()

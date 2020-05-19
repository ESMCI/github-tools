#!/usr/bin/env python

"""Unit tests for PullRequest class
"""

import unittest
import datetime
from ghtools.pull_request import PullRequest
from ghtools.comment import ConversationComment, PRReviewComment, PRLineComment

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

class TestPullRequest(unittest.TestCase):
    """Tests of PullRequest class"""

    @staticmethod
    def _simple_comment(comment_type, comment_id, content, username=None, creation_date=None):
        """Return a Comment object with some hard-coded pieces

        Args:
        comment_type (one of the subclasses of Comment (e.g., ConversationComment))
        comment_id (integer): used in URL
        content (string)
        username (string): if not given, uses a hard-coded username
        creation_date (datetime): if not given, uses a hard-coded creation_date
        """
        if username is None:
            username = "you"
        if creation_date is None:
            creation_date = datetime.datetime(2020, 1, 2)
        return comment_type(
            username=username,
            creation_date=creation_date,
            url="https://github.com/org/repo/1#comment-{c_id}".format(c_id=comment_id),
            content=content)

    @staticmethod
    def _simple_line_comment(comment_id, content, username=None, creation_date=None, path=None):
        """Return a PRLineComment object with some hard-coded pieces

        Args:
        comment_id (integer): used in URL
        content (string)
        username (string): if not given, uses a hard-coded username
        creation_date (datetime): if not given, uses a hard-coded creation_date
        path (string): if not given, uses a hard-coded path
        """
        if username is None:
            username = "you"
        if creation_date is None:
            creation_date = datetime.datetime(2020, 1, 2)
        if path is None:
            path = "path/to/file.py"
        return PRLineComment(
            username=username,
            creation_date=creation_date,
            url="https://github.com/org/repo/1#comment-{c_id}".format(c_id=comment_id),
            content=content,
            path=path)

    @staticmethod
    def _create_pr(body=None, comments=None, username=None, creation_date=None):
        """Returns a basic PullRequest object

        If body is given, it should be a string; otherwise, a hard-coded body is used

        If comments is given, it should be a list of Comment objects; otherwise, a
        hard-coded list of comments is used.

        If username is given, it should be a string; otherwise, a hard-coded username is used

        If creation_date is given, it should be a datetime object; otherwise, a hard-coded
        creation_date is used.
        """
        if body is None:
            body = "PR body"

        if comments is None:
            comments = (TestPullRequest._simple_comment(
                ConversationComment, 1, "comment"),
                        TestPullRequest._simple_line_comment(
                            2, "line comment"),
                        TestPullRequest._simple_comment(
                            PRReviewComment, 3, "review comment"))

        if username is None:
            username = "me"

        if creation_date is None:
            creation_date = datetime.datetime(2020, 1, 1)

        return PullRequest(pr_number=17,
                           title="My title",
                           username=username,
                           creation_date=creation_date,
                           url="https://github.com/org/repo/1",
                           body=body,
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
        c1 = self._simple_comment(ConversationComment, 1, "comment",
                                  creation_date=datetime.datetime(2020, 1, 1))
        c2 = self._simple_comment(ConversationComment, 2, "another comment",
                                  creation_date=datetime.datetime(2020, 1, 3))
        c3 = self._simple_line_comment(3, "line comment",
                                       creation_date=datetime.datetime(2020, 1, 2))
        c4 = self._simple_line_comment(4, "another line comment",
                                       creation_date=datetime.datetime(2020, 1, 5))
        c5 = self._simple_comment(PRReviewComment, 5, "review comment",
                                  creation_date=datetime.datetime(2020, 1, 4))

        pr = self._create_pr(comments=(c1, c2, c3, c4, c5))
        # In the following, note that we ignore the first comment, since that's the PR body
        #pylint: disable=protected-access
        self.assertEqual(pr._comments[1:], [c1, c3, c2, c5, c4])

    def test_getContent_filterUsername(self):
        """Test the get_content method with username filtering"""

        c1 = self._simple_comment(ConversationComment, 1, "TEST_COMMENT1",
                                  username="user2")
        c2 = self._simple_comment(ConversationComment, 1, "TEST_COMMENT2",
                                  username="user1")
        pr = self._create_pr(body="TEST_PRBODY", comments=(c1, c2),
                             username="user1")
        content = pr.get_content(filter_username="user1")
        self.assertIn("TEST_PRBODY", content)
        self.assertIn("TEST_COMMENT2", content)
        self.assertNotIn("TEST_COMMENT1", content)

    def test_getTodos_noComments(self):
        """Test the get_todos method when there are no comments"""
        pr = self._create_pr(body="", comments=())
        todos = pr.get_todos()
        self.assertEqual(len(todos), 0)

    def test_getTodos(self):
        """Test the get_todos method with multiple comments, each with multiple todos"""
        body = """\
PR body
- [ ] body task 1

More body
- [ ] body task 2"""

        c1_content = """\
Comment 1
- [ ] c1 task 1

More text"""

        c2_content = """\
- [ ] c2 task 1
- [ ] c2 task 2"""

        c3_content = """\
You won't find any tasks here.

Or here."""

        c1 = self._simple_comment(ConversationComment, 1, c1_content,
                                  creation_date=datetime.datetime(2020, 1, 2))
        c2 = self._simple_comment(ConversationComment, 2, c2_content,
                                  creation_date=datetime.datetime(2020, 1, 3))
        c3 = self._simple_comment(ConversationComment, 3, c3_content,
                                  creation_date=datetime.datetime(2020, 1, 4))

        pr = self._create_pr(body=body, comments=(c1, c2, c3),
                             creation_date=datetime.datetime(2020, 1, 1))
        todos = pr.get_todos()
        self.assertEqual(len(todos), 5)
        self.assertEqual(todos[0].get_text(), "body task 1")
        self.assertEqual(todos[1].get_text(), "body task 2")
        self.assertEqual(todos[2].get_text(), "c1 task 1")
        self.assertEqual(todos[3].get_text(), "c2 task 1")
        self.assertEqual(todos[4].get_text(), "c2 task 2")

    def test_getTodos_sorted(self):
        """Make sure that the todos returned by get_todos are sorted properly"""
        body = """\
- [ ] [optional] body-optional
- [ ] body-required"""

        c1_content = """\
- [ ] [optional] c1-optional
- [ ] c1-required"""

        c2_content = """\
- [ ] c2-required
- [ ] [optional] c2-optional"""

        # Note that c1 was created before c2, but we put c2 first in the list - to make
        # sure they get sorted properly.
        c1 = self._simple_comment(ConversationComment, 1, c1_content,
                                  creation_date=datetime.datetime(2020, 1, 2))
        c2 = self._simple_comment(ConversationComment, 2, c2_content,
                                  creation_date=datetime.datetime(2020, 1, 3))

        pr = self._create_pr(body=body, comments=(c2, c1),
                             creation_date=datetime.datetime(2020, 1, 1))
        todos = pr.get_todos()
        self.assertEqual(len(todos), 6)
        self.assertEqual(todos[0].get_text(), "body-required")
        self.assertEqual(todos[1].get_text(), "c1-required")
        self.assertEqual(todos[2].get_text(), "c2-required")
        self.assertIn("body-optional", todos[3].get_text())
        self.assertIn("c1-optional", todos[4].get_text())
        self.assertIn("c2-optional", todos[5].get_text())

    def test_getTodos_filterUsername(self):
        """Test the get_todos method when a username is provided"""

        c1 = self._simple_comment(ConversationComment, 1, "- [ ] c1 task",
                                  username="user2", creation_date=datetime.datetime(2020, 1, 2))
        c2 = self._simple_comment(ConversationComment, 2, "- [ ] c2 task",
                                  username="user1", creation_date=datetime.datetime(2020, 1, 3))
        pr = self._create_pr(body="- [ ] body task", comments=(c1, c2),
                             username="user1", creation_date=datetime.datetime(2020, 1, 1))
        todos = pr.get_todos(filter_username="user1")
        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0].get_text(), "body task")
        self.assertEqual(todos[1].get_text(), "c2 task")

if __name__ == '__main__':
    unittest.main()

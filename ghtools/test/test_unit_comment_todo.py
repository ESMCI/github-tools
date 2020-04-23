#!/usr/bin/env python

"""Unit tests for the comment_todo module
"""

import unittest
import datetime
from ghtools.comment_todo import search_line_for_todo, CommentTodo

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

#pylint: disable=too-many-public-methods
class TestSearchLineForTodo(unittest.TestCase):
    """Tests of search_line_for_todo function"""

    # ------------------------------------------------------------------------
    # Tests of search_line_for_todo: searches expected to find something
    # ------------------------------------------------------------------------

    def test_search_uldash(self):
        """Make sure we find a todo like '- [ ] todo'"""
        result = search_line_for_todo("- [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_ulplus(self):
        """Make sure we find a todo like '+ [ ] todo'"""
        result = search_line_for_todo("+ [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_ulstar(self):
        """Make sure we find a todo like '* [ ] todo'"""
        result = search_line_for_todo("* [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_ulMultipleSpaces(self):
        """Make sure we find a todo with multiple spaces after the unordered list indicator"""
        result = search_line_for_todo("-   [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_oldot(self):
        """Make sure we find a todo like '1. [ ] todo'"""
        result = search_line_for_todo("1. [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_olparen(self):
        """Make sure we find a todo like '1) [ ] todo'"""
        result = search_line_for_todo("1) [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_olMultipleDigits(self):
        """Make sure we find a todo with multiple digits in the list indicator"""
        result = search_line_for_todo("123. [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_olMultipleSpaces(self):
        """Make sure we find a todo with multiple spaces after the ordered list indicator"""
        result = search_line_for_todo("1.   [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_multipleSpacesAfterCheckbox(self):
        """Make sure we find a todo with multiple spaces after the checkbox"""
        result = search_line_for_todo("- [ ]   todo")
        self.assertEqual(result, "todo")

    def test_search_leadingSpaces(self):
        """Make sure we find a todo with leading spaces on the line"""
        result = search_line_for_todo("  - [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_multipleUOL(self):
        """Make sure we find a todo with multiple unordered & ordered list markers"""
        result = search_line_for_todo("- 1.  +   30) [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_quoted(self):
        """Make sure we find a quoted todo"""
        result = search_line_for_todo(">- [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_quotedWithSpace(self):
        """Make sure we find a quoted todo with a space after the quote marker"""
        result = search_line_for_todo("> - [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_multipleQuotes(self):
        """Make sure we find a quoted todo with multiple quote markers"""
        result = search_line_for_todo(">>> > > - [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_multipleAlternatingQuotesAndLists1(self):
        """Make sure we find a todo with a mix of quote and list markers"""
        result = search_line_for_todo("> - > - > - [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_multipleAlternatingQuotesAndLists2(self):
        """Make sure we find a todo with a mix of quote and list markers"""
        result = search_line_for_todo(">- >- >- [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_multipleAlternatingQuotesAndLists3(self):
        """Make sure we find a todo with a mix of quote and list markers"""
        # This is a really weird case, but GitHub treats it as a checkbox, so we will, too
        result = search_line_for_todo(">- >> + >1. - [ ] todo")
        self.assertEqual(result, "todo")

    def test_search_extraListMarkerRightBeforeCheckbox(self):
        """Make sure we find a todo with an extra list marker right before the checkbox"""
        # If there is a valid list item marker with a space after it, then another list
        # item marker without a space after it directly before the checkbox, GitHub
        # renders this as a checkbox, so we'll treat it as one, too - even though I'm not
        # sure if this is a feature or a bug.
        result = search_line_for_todo("- -[ ] todo")
        self.assertEqual(result, "todo")

    # ------------------------------------------------------------------------
    # Tests of search_line_for_todo: searches NOT expected to find something
    # ------------------------------------------------------------------------

    def test_search_emptyString_fails(self):
        """If the input is an empty string, the search should fail"""
        result = search_line_for_todo("")
        self.assertIsNone(result)

    def test_search_checkedCheckbox_fails(self):
        """If the checkbox is checked, the search should fail"""
        result = search_line_for_todo("- [x] todo")
        self.assertIsNone(result)

    def test_search_noListMarker_fails(self):
        """If there is no list marker, the search should fail"""
        result = search_line_for_todo(" [ ] todo")
        self.assertIsNone(result)

    def test_search_noCheckbox_fails(self):
        """If there is no checkbox, the search should fail"""
        result = search_line_for_todo("- todo")
        self.assertIsNone(result)

    def test_search_noWhitespaceAfterUL_fails(self):
        """If there is no whitespace after an unordered list marker, the search should fail"""
        result = search_line_for_todo("-[ ] todo")
        self.assertIsNone(result)

    def test_search_noWhitespaceAfterOL_fails(self):
        """If there is no whitespace after an ordered list marker, the search should fail"""
        result = search_line_for_todo("1.[ ] todo")
        self.assertIsNone(result)

    def test_search_noPeriodOrParenAfterNumber_fails(self):
        """If there is no . or ) after a number, the search should fail"""
        result = search_line_for_todo("1 [ ] todo")
        self.assertIsNone(result)

    def test_search_noWhitespaceAfterCheckbox_fails(self):
        """If no whitespace between the checkbox and the following text, the search should fail"""
        result = search_line_for_todo("- [ ]todo")
        self.assertIsNone(result)

    def test_search_onlyWhitespaceAfterCheckbox_fails(self):
        """If there is only whitespace after the checkbox character, the search should fail"""
        result = search_line_for_todo("- [ ]  ")
        self.assertIsNone(result)

    def test_search_multipleSpacesInBrackets_fails(self):
        """If there are multiple spaces inside the brackets, the search should fail"""
        result = search_line_for_todo("- [  ] todo")
        self.assertIsNone(result)

    def test_search_otherTextFirst_fails(self):
        """If there is other text on the line before the checkbox stuff, the search should fail"""
        result = search_line_for_todo("hi - [ ] todo")
        self.assertIsNone(result)

    def test_search_quoteJustBeforeCheckbox_fails(self):
        """If there are both list and quote markers, but the last is a quote, should fail"""
        result = search_line_for_todo("> - > [ ] todo")
        self.assertIsNone(result)

    def test_search_twoListMarkersRightBeforeCheckbox_fails(self):
        """If there are two list markers right before the checkbox, should fail"""
        # Even though "- -[ ] todo" renders as a checkbox, "- --[ ] todo" does not
        result = search_line_for_todo("- --[ ] todo")
        self.assertIsNone(result)

# ------------------------------------------------------------------------
# Tests of the CommentTodo class
# ------------------------------------------------------------------------

class TestCommentTodo(unittest.TestCase):
    """Tests of CommentTodo class"""

    @staticmethod
    def _create_comment_todo():
        """Returns a basic CommentTodo object"""
        return CommentTodo(username="me",
                           creation_date=datetime.datetime(2020, 1, 1),
                           url="https://github.com/org/repo/1#issuecomment-2",
                           text="My text")

    def test_repr_resultsInEqualObject(self):
        """The repr of a CommentTodo object should result in an equivalent object"""
        # This ability to recreate the object isn't a strict requirement, so if it gets
        # hard to maintain, we can drop it.
        t = self._create_comment_todo()
        # pylint: disable=eval-used
        t2 = eval(repr(t))
        self.assertEqual(t2, t)

    def test_str_works(self):
        """Just make sure that the str method runs successfully"""
        t = self._create_comment_todo()
        _ = str(t)

if __name__ == '__main__':
    unittest.main()

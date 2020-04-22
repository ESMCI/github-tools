#!/usr/bin/env python

"""Unit tests for the comment_todo module
"""

import unittest
from ghtools.comment_todo import search_line_for_todo

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

#pylint: disable=too-many-public-methods
class TestCommentTodo(unittest.TestCase):
    """Tests of comment_todo module"""

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

    def test_search_multipleUL(self):
        """Make sure we find a todo with multiple unordered list markers"""
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

    # ------------------------------------------------------------------------
    # Tests of search_line_for_todo: searches NOT expected to find something
    # ------------------------------------------------------------------------

    def test_search_checkedCheckbox_fails(self):
        """If the checkbox is checked, the search should fail"""
        result = search_line_for_todo("- [x] todo")
        self.assertIsNone(result)

    def test_search_noListMarker_fails(self):
        """If there is no list marker, the search should fail"""
        result = search_line_for_todo("[ ] todo")
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

    def test_search_quoteJustBeforeCheckbox_fails(self):
        """If there are both list and quote markers, but the last is a quote, should fail"""
        result = search_line_for_todo("> - > [ ] todo")
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

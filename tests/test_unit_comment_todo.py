#!/usr/bin/env python

"""Unit tests for the comment_todo module
"""

import unittest
import datetime
from ghtools.comment_time import CommentTime
from ghtools.comment_todo import search_line_for_todo, is_line_quoted, CommentTodo

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
    # Tests of search_line_for_todo with completed=True: searches expected to find something
    # ------------------------------------------------------------------------

    def test_search_completed_lowercasex(self):
        """Make sure we find a completed todo like '- [x] todo'"""
        result = search_line_for_todo("- [x] todo", completed=True)
        self.assertEqual(result, "todo")

    def test_search_completed_uppercasex(self):
        """Make sure we find a completed todo like '- [X] todo'"""
        result = search_line_for_todo("- [X] todo", completed=True)
        self.assertEqual(result, "todo")

    # ------------------------------------------------------------------------
    # Tests of search_line_for_todo with completed=True: searches NOT expected to find something
    # ------------------------------------------------------------------------

    def test_search_completed_y_fails(self):
        """If the checkbox is 'checked' with '[y]' instead of '[x'], should fail"""
        result = search_line_for_todo("- [y] todo", completed=True)
        self.assertIsNone(result)

    def test_search_completed_unchecked_fails(self):
        """If the checkbox is unchecked, should fail"""
        result = search_line_for_todo("- [ ] todo", completed=True)
        self.assertIsNone(result)

class TestIsLineQuoted(unittest.TestCase):
    """Tests of is_line_quoted function"""

    def test_isLineQuoted_lineStartsWithQuote(self):
        """Quote character at the start of the line should yield True"""
        result = is_line_quoted("> - [ ] todo")
        self.assertTrue(result)

    def test_isLineQuoted_lineStartsWithIndentedQuote(self):
        """Indented quote character at the start of the line should yield True"""
        result = is_line_quoted("  > - [ ] todo")
        self.assertTrue(result)

    def test_isLineQuoted_lineStartsWithQuoteNoSpaces(self):
        """Quote character at the start of the line, with no space afterwards, should yield True"""
        result = is_line_quoted(">- [ ] todo")
        self.assertTrue(result)

    def test_isLineQuoted_quoteAfterOtherChars(self):
        """Quote character after other characters should yield False"""
        result = is_line_quoted("a> - [ ] todo")
        self.assertFalse(result)

# ------------------------------------------------------------------------
# Tests of the CommentTodo class
# ------------------------------------------------------------------------

class TestCommentTodo(unittest.TestCase):
    """Tests of CommentTodo class"""

    @staticmethod
    def _create_comment_todo(text=None, is_quoted=False, extra_info=None, completed=False):
        """Returns a basic CommentTodo object

        If text is None, some default text will be used
        """
        if text is None:
            text = "My text"
        time_info = CommentTime(creation_time=datetime.datetime(2020, 1, 1),
                                last_updated_time=datetime.datetime(2020, 1, 2))
        return CommentTodo(username="me",
                           time_info=time_info,
                           url="https://github.com/org/repo/1#issuecomment-2",
                           text=text,
                           is_quoted=is_quoted,
                           extra_info=extra_info,
                           completed=completed)

    def test_repr_resultsInEqualObject(self):
        """The repr of a CommentTodo object should result in an equivalent object"""
        # This ability to recreate the object isn't a strict requirement, so if it gets
        # hard to maintain, we can drop it.
        t = self._create_comment_todo()
        # pylint: disable=eval-used
        t2 = eval(repr(t))
        self.assertEqual(t2, t)

    def test_repr_optional_resultsInEqualObject(self):
        """The repr of a CommentTodo object with optional prefix should result in equiv object"""
        # This ability to recreate the object isn't a strict requirement, so if it gets
        # hard to maintain, we can drop it.
        t = self._create_comment_todo(text="[optional] Not necessary")
        # pylint: disable=eval-used
        t2 = eval(repr(t))
        self.assertEqual(t2, t)

    def test_repr_quoted_resultsInEqualObject(self):
        """The repr of a CommentTodo object with is_quoted=True should result in equiv object"""
        # This ability to recreate the object isn't a strict requirement, so if it gets
        # hard to maintain, we can drop it.
        t = self._create_comment_todo(is_quoted=True)
        # pylint: disable=eval-used
        t2 = eval(repr(t))
        self.assertEqual(t2, t)

    def test_repr_extraInfo_resultsInEqualObject(self):
        """The repr of a CommentTodo object with extra info should result in equiv object"""
        # This ability to recreate the object isn't a strict requirement, so if it gets
        # hard to maintain, we can drop it.
        t = self._create_comment_todo(extra_info="extra stuff")
        # pylint: disable=eval-used
        t2 = eval(repr(t))
        self.assertEqual(t2, t)

    def test_repr_completed_resultsInEqualObject(self):
        """The repr of a CommentTodo object that is completed should result in equiv object"""
        t = self._create_comment_todo(completed=True)
        # pylint: disable=eval-used
        t2 = eval(repr(t))
        self.assertEqual(t2, t)

    def test_str_works(self):
        """Just make sure that the str method runs successfully"""
        t = self._create_comment_todo()
        _ = str(t)

    def test_isOptional_nonOptional(self):
        """Test is_optional method on a non-optional todo"""
        # Only considered optional if it *starts* with the tag
        text = "Not [optional] even though that tag appears somewhere"
        t = self._create_comment_todo(text=text)
        self.assertFalse(t.is_optional())
        self.assertEqual(t.get_full_text(), text)

    def test_isOptional_optional1(self):
        """Test is_optional method on an optional todo"""
        t = self._create_comment_todo(text="[optional] Not necessary")
        self.assertTrue(t.is_optional())
        self.assertEqual(t.get_full_text(), "[OPTIONAL] Not necessary")

    def test_isOptional_optional2(self):
        """Test is_optional method on an optional todo"""
        t = self._create_comment_todo(text="(OPTIONAL) Not necessary")
        self.assertTrue(t.is_optional())
        self.assertEqual(t.get_full_text(), "[OPTIONAL] Not necessary")

    def test_isOptional_optional3(self):
        """Test is_optional method on an optional todo"""
        t = self._create_comment_todo(text="Optional: Not necessary")
        self.assertTrue(t.is_optional())
        self.assertEqual(t.get_full_text(), "[OPTIONAL] Not necessary")

    def test_isOptional_optionalWithLeadingSpace(self):
        """Test is_optional method on an optional todo with leading spaces"""
        t = self._create_comment_todo(text="   [optional] Not necessary")
        self.assertTrue(t.is_optional())
        self.assertEqual(t.get_full_text(), "[OPTIONAL] Not necessary")

    def test_isOptional_twoOptionals(self):
        """Test is_optional method on a todo with two occurrences of [optional]"""
        # Only the first should be replaced
        t = self._create_comment_todo(text="[optional] Not [optional] necessary")
        self.assertTrue(t.is_optional())
        self.assertEqual(t.get_full_text(), "[OPTIONAL] Not [optional] necessary")

    def test_getFullText_basic(self):
        """Test get_full_text with a basic todo (non-optional, no extra info)"""
        t = self._create_comment_todo(text="My text")
        self.assertEqual(t.get_full_text(), "My text")

    def test_getFullText_extraInfo(self):
        """Test get_full_text with a extra info"""
        t = self._create_comment_todo(text="My text", extra_info="Extra stuff")
        self.assertEqual(t.get_full_text(), "{Extra stuff} My text")

    def test_getFullText_optionalAndExtraInfo(self):
        """Test get_full_text with an optional todo that also has extra info"""
        t = self._create_comment_todo(text="[optional]  My text", extra_info="Extra stuff")
        self.assertEqual(t.get_full_text(), "[OPTIONAL] {Extra stuff} My text")

    def test_getFullText_optionalAndExtraInfoAndCompleted(self):
        """Test get_full_text with an optional todo that also has extra info and is completed"""
        t = self._create_comment_todo(text="[optional]  My text",
                                      extra_info="Extra stuff",
                                      completed=True)
        self.assertEqual(t.get_full_text(), "[COMPLETED] [OPTIONAL] {Extra stuff} My text")

    def test_getFullText_optionalAndExtraInfoAndQuoted(self):
        """Test get_full_text with an optional todo that also has extra info and is quoted"""
        t = self._create_comment_todo(text="[optional]  My text",
                                      extra_info="Extra stuff",
                                      is_quoted=True)
        self.assertEqual(t.get_full_text(), "[QUOTED] [OPTIONAL] {Extra stuff} My text")

if __name__ == '__main__':
    unittest.main()

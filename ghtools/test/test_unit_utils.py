#!/usr/bin/env python

"""Unit tests for utils module
"""

import unittest
from ghtools.utils import split_paragraphs

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

class TestSplitParagraphs(unittest.TestCase):
    """Tests of split_paragraphs function"""

    # ------------------------------------------------------------------------
    # Tests of split_paragraphs
    # ------------------------------------------------------------------------

    def test_oneline(self):
        """split_paragraphs on a one-line string"""
        text = "hello"
        text_split = split_paragraphs(text)
        self.assertEqual(text_split, ["hello"])

    def test_multilineOneParagraph(self):
        """split_paragraphs on a multi-line but one-paragraph string"""
        text = """\
hello
there
hi"""
        text_split = split_paragraphs(text)
        self.assertEqual(text_split, [text])

    def test_multiparagraph(self):
        """split_paragraphs on a multi-paragraph string"""

        # In the following, note that there are some spaces on the line in between
        # paragraphs 1 and 2
        text = """\
paragraph 1a
paragraph 1b
   
paragraph 2a

paragraph 3a
paragraph 3b
paragraph 3c"""
        p1 = "paragraph 1a\nparagraph 1b"
        p2 = "paragraph 2a"
        p3 = "paragraph 3a\nparagraph 3b\nparagraph 3c"
        text_split = split_paragraphs(text)
        self.assertEqual(text_split, [p1, p2, p3])

    def test_multiparagraph_multipleNewlines(self):
        """split_paragraphs on a multi-paragraph string with multiple newlines between paragraphs"""
        text = """\
paragraph 1a
paragraph 1b
   
paragraph 2a



paragraph 3a
paragraph 3b
paragraph 3c"""
        p1 = "paragraph 1a\nparagraph 1b"
        p2 = "paragraph 2a"
        p3 = "paragraph 3a\nparagraph 3b\nparagraph 3c"
        text_split = split_paragraphs(text)
        self.assertEqual(text_split, [p1, p2, p3])

    def test_emptyString(self):
        """split_paragraphs on an empty string"""
        text = ""
        text_split = split_paragraphs(text)
        self.assertEqual(text_split, [])

if __name__ == '__main__':
    unittest.main()

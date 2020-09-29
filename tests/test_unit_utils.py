#!/usr/bin/env python

"""Unit tests for utils module
"""

import unittest
from ghtools.utils import split_pr_url

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

class TestUtils(unittest.TestCase):
    """Tests of utils module"""

    def assertSplitPrUrlFailure(self, repo, pr_number):
        """Asserts that the given return values of split_pr_url indicate failure"""
        self.assertIsNone(repo)
        self.assertIsNone(pr_number)

    def test_splitPrUrl_success_basic(self):
        """A basic success test of split_pr_url"""
        (repo, pr_number) = split_pr_url('https://github.com/ESMCI/github-tools/pull/1357')
        self.assertEqual(repo, 'ESMCI/github-tools')
        self.assertEqual(pr_number, 1357)

    def test_splitPrUrl_success_basic_extraSlash(self):
        """A success test of split_pr_url with a trailing slash"""
        (repo, pr_number) = split_pr_url('https://github.com/ESMCI/github-tools/pull/1357/')
        self.assertEqual(repo, 'ESMCI/github-tools')
        self.assertEqual(pr_number, 1357)

    def test_splitPrUrl_success_extraTrailing(self):
        """A success test of split_pr_url with acceptable trailing stuff in the URL"""
        (repo, pr_number) = split_pr_url('https://github.com/ESMCI/github-tools/pull/1357/files')
        self.assertEqual(repo, 'ESMCI/github-tools')
        self.assertEqual(pr_number, 1357)

    def test_splitPrUrl_failure_noPull(self):
        """Failure test of split_pr_url: no 'pull' in the URL"""
        (repo, pr_number) = split_pr_url('https://github.com/ESMCI/github-tools/1357')
        self.assertSplitPrUrlFailure(repo, pr_number)

    def test_splitPrUrl_failure_noOrg(self):
        """Failure test of split_pr_url: no org in the URL"""
        (repo, pr_number) = split_pr_url('https://github.com/github-tools/pull/1357')
        self.assertSplitPrUrlFailure(repo, pr_number)

    def test_splitPrUrl_failure_extraComponent(self):
        """Failure test of split_pr_url: extra component in the URL"""
        (repo, pr_number) = split_pr_url('https://github.com/ESMCI/github-tools/foo/pull/1357')
        self.assertSplitPrUrlFailure(repo, pr_number)

    def test_splitPrUrl_failure_badTrailing(self):
        """Failure test of split_pr_url: bad trailing stuff in the URL"""
        (repo, pr_number) = split_pr_url('https://github.com/ESMCI/github-tools/pull/1357a')
        self.assertSplitPrUrlFailure(repo, pr_number)

if __name__ == '__main__':
    unittest.main()

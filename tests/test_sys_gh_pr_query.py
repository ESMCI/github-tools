#!/usr/bin/env python

"""System tests for gh_pr_query

Recommendation: Define an environment variable named GITHUB_TOKEN containing your GitHub
personal access token so that the tests here can use this token, and thus be less likely
to fail due to GitHub's API rate limiting.
"""

import unittest
import contextlib
import io
import re
from ghtools.gh_pr_query import gh_pr_query

# Allow names that pylint doesn't like, because otherwise I find it hard
# to make readable unit test names
# pylint: disable=invalid-name

def _remove_whitespace(string):
    """Return a version of the input string with whitespace removed"""
    whitespace_re = re.compile(r"\s+")
    return whitespace_re.sub('', string)

class TestSysGhPrQuery(unittest.TestCase):
    """System tests of gh_pr_query"""

    def test_ghPrQuery(self):
        """Basic system test of gh_pr_query"""
        stdout_redirect = io.StringIO()
        with contextlib.redirect_stdout(stdout_redirect):
            # Normally we wouldn't specify both todo and show in a single run of this. We
            # do that here for efficiency - to avoid two separate sets of queries.
            gh_pr_query(repo="ESMCI/github-tools",
                        pr_number=1,
                        show=True,
                        todo=True,
                        completed=False)
        output = stdout_redirect.getvalue()

        # Note that this is the same as what's given in the example in the top-level
        # README file. These should be kept in sync.
        expected_show_output = """\
PR #1: 'Changes for the sake of demo PR' by billsacks on 2020-04-23 19:24:00-06:00 (https://github.com/ESMCI/github-tools/pull/1):

PR body by billsacks on 2020-04-23 19:24:00-06:00 (https://github.com/ESMCI/github-tools/pull/1):
    This PR is for demonstration purposes only.

    There is a checklist in the body:

    - [ ] (optional) Do a task suggested in the body
    - [x] Do another task suggested in the body

    After some more text, there is another checklist:

    - [ ] Do a task from the body's second checklist

PR line comment (README.md) by billsacks on 2020-04-23 19:25:28-06:00 (https://github.com/ESMCI/github-tools/pull/1#discussion_r414063434):
    I would like the following changes to this line:

    - [ ] (optional) Please change "just" to "only"
    - [ ] Please change "PR" to "Pull Request"

PR review comment by billsacks on 2020-04-23 19:25:49-06:00 (https://github.com/ESMCI/github-tools/pull/1#pullrequestreview-399407911):
    In addition to my line comments, please also:

    - [ ] Add a section on Demo deletions

Conversation comment by billsacks on 2020-04-23 19:26:39-06:00 (https://github.com/ESMCI/github-tools/pull/1#issuecomment-618612295):
    PR comments can also include checklist items

    - [x] I should do this
    - [ ] I should do that

Conversation comment by billsacks on 2020-04-23 19:34:19-06:00 (https://github.com/ESMCI/github-tools/pull/1#issuecomment-618616900):
    Closing this PR that was for demonstration purposes only.
"""

        # Note that this is the same as what's given in the example in the top-level
        # README file. These should be kept in sync.
        expected_todo_output = """\
- Do a task from the body's second checklist
  (billsacks at 2020-04-23 19:24:00-06:00, <https://github.com/ESMCI/github-tools/pull/1>)

- {README.md} Please change "PR" to "Pull Request"
  (billsacks at 2020-04-23 19:25:28-06:00, <https://github.com/ESMCI/github-tools/pull/1#discussion_r414063434>)

- Add a section on Demo deletions
  (billsacks at 2020-04-23 19:25:49-06:00, <https://github.com/ESMCI/github-tools/pull/1#pullrequestreview-399407911>)

- I should do that
  (billsacks at 2020-04-23 19:26:39-06:00, <https://github.com/ESMCI/github-tools/pull/1#issuecomment-618612295>)

- [OPTIONAL] Do a task suggested in the body
  (billsacks at 2020-04-23 19:24:00-06:00, <https://github.com/ESMCI/github-tools/pull/1>)

- [OPTIONAL] {README.md} Please change "just" to "only"
  (billsacks at 2020-04-23 19:25:28-06:00, <https://github.com/ESMCI/github-tools/pull/1#discussion_r414063434>)
"""

        # Remove all whitespace before comparing, so that the test won't fail if we just
        # change some of the output formatting.
        expected_show_output_no_whitespace = _remove_whitespace(expected_show_output)
        expected_todo_output_no_whitespace = _remove_whitespace(expected_todo_output)
        output_no_whitespace = _remove_whitespace(output)

        # We use assertIn so that we are insensitive to whether the show or todo output
        # appears first. (As noted above, it is not typical to run gh_pr_query with both
        # show and todo, but we do it here for efficiency.)
        self.assertIn(expected_show_output_no_whitespace, output_no_whitespace)
        self.assertIn(expected_todo_output_no_whitespace, output_no_whitespace)

    def test_ghPrQuery_completed_verbose(self):
        """System test of gh_pr_query covering both the completed and verbose options"""
        stdout_redirect = io.StringIO()
        with contextlib.redirect_stdout(stdout_redirect):
            gh_pr_query(repo="ESMCI/github-tools",
                        pr_number=1,
                        show=False,
                        todo=False,
                        completed=True,
                        verbose=True)
        output = stdout_redirect.getvalue()
        expected_output = """\
PR #1: 'Changes for the sake of demo PR' by billsacks on 2020-04-23 19:24:00-06:00 (https://github.com/ESMCI/github-tools/pull/1):

- [COMPLETED] Do another task suggested in the body
  (billsacks at 2020-04-23 19:24:00-06:00, <https://github.com/ESMCI/github-tools/pull/1>)

- [COMPLETED] I should do this
  (billsacks at 2020-04-23 19:26:39-06:00, <https://github.com/ESMCI/github-tools/pull/1#issuecomment-618612295>)
"""
        # Remove all whitespace before comparing, so that the test won't fail if we just
        # change some of the output formatting.
        expected_output_no_whitespace = _remove_whitespace(expected_output)
        output_no_whitespace = _remove_whitespace(output)

        self.assertEqual(output_no_whitespace, expected_output_no_whitespace)

if __name__ == '__main__':
    unittest.main()

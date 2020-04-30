# github-tools

## Overview

This repository contains tools for working with GitHub repositories from
the command line. For now there is just one (`gh-pr-query`).

## Installation

This script and its necessary dependencies can be installed similarly to
other python tools, using `pip install`. It is not yet on PyPI, but it
can be installed directly from this GitHub repository with:

```
pip install git+https://github.com/ESMCI/github-tools.git@master
```

## Tools contained here

### gh-pr-query

Tool for querying GitHub Pull Requests

To show all of the outstanding todo items in all comments in a pull request
(i.e., all unchecked checkboxes):

    gh-pr-query -r REPO -p PR_NUMBER -t

To show all comments in a pull request:

    gh-pr-query -r REPO -p PR_NUMBER -s

Output is sorted by date; for todos, all required todos are listed
before optional todos. (Optional todos are denoted by starting a todo
item with '[optional]', '(optional)', or 'optional:', lowercase or
uppercase.)

For either usage, output can be filtered on username - only showing
comments made by the given username - with the `-u` or
`--filter-username` option.

For more detailed help, run

    gh-pr-query -h
    
#### Examples

##### Showing all outstanding todo items

```
$ ./gh-pr-query -r esmci/github-tools -p 1 -t
- Do a task from the body's second checklist
  (billsacks at 2020-04-23 19:24:00-06:00, <https://github.com/ESMCI/github-tools/pull/1>)

- Please change "PR" to "Pull Request"
  (billsacks at 2020-04-23 19:25:28-06:00, <https://github.com/ESMCI/github-tools/pull/1#discussion_r414063434>)

- Add a section on Demo deletions
  (billsacks at 2020-04-23 19:25:49-06:00, <https://github.com/ESMCI/github-tools/pull/1#pullrequestreview-399407911>)

- I should do that
  (billsacks at 2020-04-23 19:26:39-06:00, <https://github.com/ESMCI/github-tools/pull/1#issuecomment-618612295>)

- [OPTIONAL] Do a task suggested in the body
  (billsacks at 2020-04-23 19:24:00-06:00, <https://github.com/ESMCI/github-tools/pull/1>)

- [OPTIONAL] Please change "just" to "only"
  (billsacks at 2020-04-23 19:25:28-06:00, <https://github.com/ESMCI/github-tools/pull/1#discussion_r414063434>)
```

##### Showing all comments

```
$ ./gh-pr-query -r esmci/github-tools -p 1 -s
PR #1: 'Changes for the sake of demo PR' by billsacks on 2020-04-23 19:24:00-06:00 (https://github.com/ESMCI/github-tools/pull/1):

PR body by billsacks on 2020-04-23 19:24:00-06:00 (https://github.com/ESMCI/github-tools/pull/1):
    This PR is for demonstration purposes only.

    There is a checklist in the body:

    - [ ] (optional) Do a task suggested in the body
    - [x] Do another task suggested in the body

    After some more text, there is another checklist:

    - [ ] Do a task from the body's second checklist

PR line comment by billsacks on 2020-04-23 19:25:28-06:00 (https://github.com/ESMCI/github-tools/pull/1#discussion_r414063434):
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
```

## Providing a personal access token

To avoid GitHub's fairly restrictive rate limiting when querying
repositories without authentication, you can provide a GitHub personal
access token in the environment variable `GITHUB_TOKEN`. [See the wiki
for more details.](https://github.com/ESMCI/github-tools/wiki/Tips-for-GitHub-Personal-Access-Tokens)

## Testing the code

If you make changes the code, you should run the tests in the `tests`
subdirectory. See the README file in that directory for details.

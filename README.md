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

Tool for querying GitHub pull requests

To show all of the outstanding todo items in all comments in a pull request
(i.e., all unchecked checkboxes):

    gh-pr-query -r REPO -p PR_NUMBER -t

or:

    gh-pr-query https://github.com/ORG/REPO/pull/PR_NUMBER -t

To show all of the completed todo items in all comments in a pull request
(i.e., all checked checkboxes):

    gh-pr-query -r REPO -p PR_NUMBER -c

or:

    gh-pr-query https://github.com/ORG/REPO/pull/PR_NUMBER -c

To show all comments in a pull request:

    gh-pr-query -r REPO -p PR_NUMBER -s

or:

    gh-pr-query https://github.com/ORG/REPO/pull/PR_NUMBER -s

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

This shows all outstanding todo items in [this pull request](https://github.com/ESMCI/github-tools/pull/1):

```
$ gh-pr-query -r esmci/github-tools -p 1 -t
- Do a task from the body's second checklist
  (billsacks (at 2020-04-23 19:24:00-06:00, last updated: unknown) <https://github.com/ESMCI/github-tools/pull/1>)

- {README.md} Please change "PR" to "Pull Request"
  (billsacks (at 2020-04-23 19:25:28-06:00, last updated: 2020-04-29 13:18:59-06:00) <https://github.com/ESMCI/github-tools/pull/1#discussion_r414063434>)

- Add a section on Demo deletions
  (billsacks (at 2020-04-23 19:25:49-06:00, last updated: unknown) <https://github.com/ESMCI/github-tools/pull/1#pullrequestreview-399407911>)

- I should do that
  (billsacks (at 2020-04-23 19:26:39-06:00, last updated: 2020-04-23 19:37:52-06:00) <https://github.com/ESMCI/github-tools/pull/1#issuecomment-618612295>)

- [OPTIONAL] Do a task suggested in the body
  (billsacks (at 2020-04-23 19:24:00-06:00, last updated: unknown) <https://github.com/ESMCI/github-tools/pull/1>)

- [OPTIONAL] {README.md} Please change "just" to "only"
  (billsacks (at 2020-04-23 19:25:28-06:00, last updated: 2020-04-29 13:18:59-06:00) <https://github.com/ESMCI/github-tools/pull/1#discussion_r414063434>)
```

##### Showing all comments

This shows all comments made in [this pull request](https://github.com/ESMCI/github-tools/pull/1):

```
$ gh-pr-query -r esmci/github-tools -p 1 -s
PR #1: 'Changes for the sake of demo PR' by billsacks (at 2020-04-23 19:24:00-06:00, last updated: 2020-04-29 13:18:59-06:00) <https://github.com/ESMCI/github-tools/pull/1>:

PR body by billsacks (at 2020-04-23 19:24:00-06:00, last updated: unknown) <https://github.com/ESMCI/github-tools/pull/1>:
    This PR is for demonstration purposes only.

    There is a checklist in the body:

    - [ ] (optional) Do a task suggested in the body
    - [x] Do another task suggested in the body

    After some more text, there is another checklist:

    - [ ] Do a task from the body's second checklist

PR line comment (README.md) by billsacks (at 2020-04-23 19:25:28-06:00, last updated: 2020-04-29 13:18:59-06:00) <https://github.com/ESMCI/github-tools/pull/1#discussion_r414063434>:
    I would like the following changes to this line:

    - [ ] (optional) Please change "just" to "only"
    - [ ] Please change "PR" to "Pull Request"

PR review comment by billsacks (at 2020-04-23 19:25:49-06:00, last updated: unknown) <https://github.com/ESMCI/github-tools/pull/1#pullrequestreview-399407911>:
    In addition to my line comments, please also:

    - [ ] Add a section on Demo deletions

Conversation comment by billsacks (at 2020-04-23 19:26:39-06:00, last updated: 2020-04-23 19:37:52-06:00) <https://github.com/ESMCI/github-tools/pull/1#issuecomment-618612295>:
    PR comments can also include checklist items

    - [x] I should do this
    - [ ] I should do that

Conversation comment by billsacks (at 2020-04-23 19:34:19-06:00, last updated: never) <https://github.com/ESMCI/github-tools/pull/1#issuecomment-618616900>:
    Closing this PR that was for demonstration purposes only.
```

#### Recommended workflow

See [the
wiki](https://github.com/ESMCI/github-tools/wiki/Recommended-pull-request-workflow-with-gh-pr-query)
for the recommended workflow in order to most effectively leverage this
tool's `--todo` option.

### gh-org-query

Tool for querying GitHub organizations

Currently, the only supported usage of this tool is to get an
alphabetical list of repositories in the organization:

    gh-org-query -o ORG -r

Note that private repositories will only be shown if your access token
has appropriate permissions (including `repo` permissions to access
private repositories). See [the section
below](#Providing-a-personal-access-token) for instructions on providing
a personal access token to this and other tools.

## Providing a personal access token

The tools here optionally allow you to set a GitHub personal access
token in the environment variable `GITHUB_TOKEN`. This is a personal,
random string generated by GitHub, which is NOT the same as your GitHub
password. For tools that only do read operations on public repositories,
an access token is not required. However, GitHub rate-limits fetches via
the API, and the limit is very small if you do not provide an access
token. So, in order to do more than a few queries per hour, you will
likely need to set up and provide a personal access token.

[GitHub's help
guide](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line)
provides instructions for creating a personal access token. If you only
need read access to public repositories, then you do not need to check
any of the boxes when setting up your access token.

You only need to create a personal access token once, but once you do,
you will need to save it somewhere, such as in a password manager.

You can then either set `GITHUB_TOKEN` in your shell's environment, or
specify it just for the given command - e.g.,:

```
GITHUB_TOKEN=abc123 gh-pr-query ...
```

## Testing the code

If you make changes the code, you should run the tests in the `tests`
subdirectory. See the README file in that directory for details.

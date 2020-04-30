# Testing github-tools

## Overview and quick start

This `tests` directory contains tests of the code in this repository,
along with a Makefile to facilitate running these tests. Tests should be
run by running `make` from this directory with an appropriate target.

To run all tests, simply run `make all` from this directory. All tests
should pass before code is merged to master.

## Test categories

The following sets of tests can be run; all of these should be kept
passing on master:

- `make utest`: unit tests

- `make stest`: system tests

- `make lint`: pylint

In addition, there are a number of targets that run combinations of the
above:

- `make test`: unit and system tests

- `make all`: all of the above

## Notes about running system tests

The system tests exercise the GitHub API. The GitHub API has fairly
restrictive rate limiting if you don't provide authentication. As with
interactive use of the tools, the system tests will use authentication
if you have set the environment variable `GITHUB_TOKEN`. So, if you plan
to run the system tests, it is best to define that environment variable,
setting its value to your GitHub Personal Access Token.

Note that the system tests can be somewhat fragile - e.g., they will
fail without an internet connection, if the GitHub API is down, etc.

Also, the expected output for the system tests may need to be
updated. If a system test fails because you have changed what the output
looks like: do a careful examination of the new output to make sure it
looks good, then replace the expected output with the new expected
output. Note that the expected output for `test_ghPrQuery` also appears
in the top-level README file, so that should be updated at the same
time.

Finally, for the system tests, I think it's safe to ignore a warning
that looks like this (which appears if a system test fails):

```
/Users/sacks/bin_external/github-tools/ghtools/gh_pr_query.py:32: ResourceWarning: unclosed <ssl.SSLSocket fd=6, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('192.168.0.10', 64665), raddr=('140.82.113.6', 443)>
  pr_number=pr_number)
ResourceWarning: Enable tracemalloc to get the object allocation traceback
```

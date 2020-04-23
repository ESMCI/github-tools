"""Functions implementing gh-pr-query tool"""

import argparse
from ghtools.github_fetch import fetch_pull_request

# ========================================================================
# Public functions
# ========================================================================

def main():
    """Main function called when gh-pr-query is run from the command line"""
    args = _commandline_args()
    gh_pr_query(repo=args.repo,
                pr_number=args.pr_number,
                todo=args.todo,
                access_token=args.access_token)

def gh_pr_query(repo, pr_number, todo, access_token=None):
    """Implementation of the gh-pr-query command

    Args:
    repo: string - GitHub repository, in the form ORG/REPO
    pr_number: integer - Pull Request number
    todo: boolean - Whether to print all outstanding todo items in this PR
    access_token: string - A GitHub personal access token
    """
    pull_request = fetch_pull_request(repo=repo,
                                      pr_number=pr_number,
                                      access_token=access_token)
    if todo:
        print_pr_todos(pull_request)

def print_pr_todos(pull_request):
    """Print all outstanding todo items for the given PullRequest"""
    todos = pull_request.get_todos()
    for todo in todos:
        print("- {}\n".format(str(todo)))

# ========================================================================
# Private functions
# ========================================================================

def _commandline_args():
    """Parse and return command-line arguments"""

    description = """
Tool for querying GitHub Pull Requests
"""

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-r', '--repo', required=True,
                        help='GitHub repository, in the form ORG/REPO')

    parser.add_argument('-p', '--pr-number', required=True, type=int,
                        help='Pull Request number')

    parser.add_argument('-t', '--todo', action='store_true',
                        help='Print all outstanding todo items in this PR')

    # FIXME(wjs, 2020-04-23) Add more detailed help for this, pointing to the GitHub help page.
    parser.add_argument('-a', '--access-token',
                        help='GitHub personal access token (like a password)')

    # FIXME(wjs, 2020-04-23) Add a -s/--summary argument. Ensure that at least one of
    # --todo or --summary is given. Also add an --output-dir optional argument, and ensure
    # that this is given if both --todo and --summary are given. (But actually, maybe
    # initially, just allow one of the two without the --output-dir option; can add that
    # as a later feature.)
    args = parser.parse_args()
    return args

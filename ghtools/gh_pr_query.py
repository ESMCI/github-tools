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
                show_comments=args.show_comments,
                todo=args.todo,
                access_token=args.access_token)

def gh_pr_query(repo, pr_number, todo, show_comments, access_token=None):
    """Implementation of the gh-pr-query command

    Args:
    repo: string - GitHub repository, in the form ORG/REPO
    pr_number: integer - Pull Request number
    show_comments: boolean - Whether to print all comments from this PR
    todo: boolean - Whether to print all outstanding todo items in this PR
    access_token: string - A GitHub personal access token
    """
    pull_request = fetch_pull_request(repo=repo,
                                      pr_number=pr_number,
                                      access_token=access_token)
    if show_comments:
        print_pr_comments(pull_request)
    if todo:
        print_pr_todos(pull_request)

def print_pr_comments(pull_request):
    """Print all comments for the given PullRequest"""
    for comment in pull_request.get_comments():
        print(str(comment) + "\n\n")

def print_pr_todos(pull_request):
    """Print all outstanding todo items for the given PullRequest"""
    for todo in pull_request.get_todos():
        print("- {}\n".format(str(todo)))

# ========================================================================
# Private functions
# ========================================================================

def _commandline_args():
    """Parse and return command-line arguments"""

    description = """
Tool for querying GitHub Pull Requests

To show all comments in a pull request:
    gh-pr-query -r REPO -p PR_NUMBER -s

To show all of the outstanding todo items in all comments in a pull request
(i.e., all unchecked checkboxes):
    gh-pr-query -r REPO -p PR_NUMBER -t

Example:
    gh-pr-query -r ESMCI/github-tools -p 1 -t
"""

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-r', '--repo', required=True,
                        help='GitHub repository, in the form ORG/REPO')

    parser.add_argument('-p', '--pr-number', required=True, type=int,
                        help='Pull Request number')

    mode = parser.add_mutually_exclusive_group(required=True)

    mode.add_argument('-s', '--show-comments', action='store_true',
                      help='Print all comments from this PR')

    mode.add_argument('-t', '--todo', action='store_true',
                      help='Print all outstanding todo items in this PR')

    parser.add_argument('-a', '--access-token',
                        help='GitHub personal access token (like a password)\n'
                        'This is not required, but without it, GitHub severely limits\n'
                        'the number of queries that can be run in a period of time.\n'
                        'For more information, see:\n'
                        'https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line') # pylint: disable=line-too-long

    args = parser.parse_args()
    return args

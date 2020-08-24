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
                show=args.show,
                todo=args.todo,
                completed=args.completed,
                filter_username=args.filter_username,
                verbose=args.verbose)

def gh_pr_query(repo, pr_number, show, todo,
                completed=False, filter_username=None, verbose=False):
    """Implementation of the gh-pr-query command

    Args:
    repo: string - GitHub repository, in the form ORG/REPO
    pr_number: integer - Pull Request number
    show: boolean - Whether to print all comments from this PR
    todo: boolean - Whether to print all outstanding todo items in this PR
    completed: boolean - Whether to look for completed todos instead of incomplete todos
        (only relevant if todo is True)
    filter_username: string or None - A GitHub user name; if provided, will only show
        comments authored by this user
    verbose: boolean - Whether verbose output is enabled
    """
    pull_request = fetch_pull_request(repo=repo,
                                      pr_number=pr_number)
    if show:
        print(pull_request.get_content(filter_username=filter_username))
    if todo:
        if verbose:
            print(pull_request.get_header() + '\n')
        print_pr_todos(pull_request,
                       completed=completed,
                       filter_username=filter_username,
                       verbose=verbose)

def print_pr_todos(pull_request, completed=False, filter_username=None, verbose=False):
    """Print all outstanding todo items for the given PullRequest

    Args:
    pull_request: PullRequest object
    completed: boolean - whether to look for completed todos instead of incomplete todos
    filter_username: string or None - A GitHub user name; if provided, will only show
        comments authored by this user
    verbose: boolean - Whether verbose output is enabled
    """
    all_todos = pull_request.get_todos(completed=completed,
                                       filter_username=filter_username)
    for todo in all_todos:
        print(str(todo) + "\n")
    if verbose and not all_todos:
        if completed:
            print('NO COMPLETED TODO ITEMS')
        else:
            print('NO OUTSTANDING TODO ITEMS')

# ========================================================================
# Private functions
# ========================================================================

def _commandline_args():
    """Parse and return command-line arguments"""

    description = """
Tool for querying GitHub pull requests

To show all of the outstanding todo items in all comments in a pull request
(i.e., all unchecked checkboxes):
    gh-pr-query -r REPO -p PR_NUMBER -t

To show all comments in a pull request:
    gh-pr-query -r REPO -p PR_NUMBER -s

Output is sorted by date; for todos, all required todos are listed before optional
todos. (Optional todos are denoted by starting a todo item with '[optional]',
'(optional)', or 'optional:', lowercase or uppercase.)

If the environment variable GITHUB_TOKEN is set, it will be used as a personal access
token for authentication. Otherwise, no authentication will be used. For details, see
<https://github.com/ESMCI/github-tools#providing-a-personal-access-token>.

Example:
    gh-pr-query -r ESMCI/github-tools -p 1 -t
"""

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-r', '--repo', required=True,
                        help='GitHub repository, in the form ORG/REPO')

    parser.add_argument('-p', '--pr-number', required=True, type=int,
                        help='Pull request number')

    mode = parser.add_mutually_exclusive_group(required=True)

    mode.add_argument('-s', '--show', action='store_true',
                      help='Print all comments from this PR')

    mode.add_argument('-t', '--todo', action='store_true',
                      help='Print all outstanding todo items in this PR')

    parser.add_argument('-u', '--filter-username',
                        help='Only show comments made by the given user')

    parser.add_argument('-c', '--completed', action='store_true',
                        help='Can be combined with -t/--todo to show completed todo items\n'
                        'instead of outstanding todo items')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()

    if args.completed and not args.todo:
        parser.error('-c/--completed can only be given along with -t/--todo')

    return args

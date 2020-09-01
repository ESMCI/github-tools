"""Functions implementing gh-pr-query tool"""

import argparse
import datetime
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
                created_since=args.created_since,
                updated_since=args.updated_since,
                verbose=args.verbose)

def gh_pr_query(repo, pr_number, show, todo, completed,
                filter_username=None, created_since=None, updated_since=None,
                verbose=False):
    """Implementation of the gh-pr-query command

    Args:
    repo: string - GitHub repository, in the form ORG/REPO
    pr_number: integer - Pull Request number
    show: boolean - Whether to print all comments from this PR
    todo: boolean - Whether to print all outstanding todo items in this PR
    completed: boolean - Whether to print all completed todo items in this PR
    filter_username: string or None - A GitHub user name; if provided, will only show
        comments authored by this user
    created_since: string or None - A string formatted as an ISO date/time (e.g.,
        YYYY-MM-DD); if provided, will only show comments created since this date/time
    updated_since: string or None - A string formatted as an ISO date/time (e.g.,
        YYYY-MM-DD); if provided, will only show comments updated since this date/time
    verbose: boolean - Whether verbose output is enabled
    """
    pull_request = fetch_pull_request(repo=repo,
                                      pr_number=pr_number)

    created_since_datetime = _date_string_to_datetime(created_since)
    updated_since_datetime = _date_string_to_datetime(updated_since)

    if show:
        print(pull_request.get_content(filter_username=filter_username,
                                       created_since_time=created_since_datetime,
                                       updated_since_time=updated_since_datetime))
    if todo:
        print_pr_todos(pull_request,
                       completed=False,
                       filter_username=filter_username,
                       created_since_datetime=created_since_datetime,
                       updated_since_datetime=updated_since_datetime,
                       verbose=verbose)
    if completed:
        print_pr_todos(pull_request,
                       completed=True,
                       filter_username=filter_username,
                       created_since_datetime=created_since_datetime,
                       updated_since_datetime=updated_since_datetime,
                       verbose=verbose)

def print_pr_todos(pull_request, completed,
                   filter_username, created_since_datetime, updated_since_datetime,
                   verbose):
    """Print all outstanding todo items for the given PullRequest

    Args:
    pull_request: PullRequest object
    completed: boolean - whether to look for completed todos instead of outstanding todos
    filter_username: string or None - A GitHub user name; if provided, will only show
        comments authored by this user
    created_since_datetime: datetime.datetime or None - If provided, will only show
        comments created since this date/time
    updated_since_datetime: datetime.datetime or None - If provided, will only show
        comments updated since this date/time
    verbose: boolean - Whether verbose output is enabled
    """
    if verbose:
        print(pull_request.get_header() + '\n')

    all_todos = pull_request.get_todos(completed=completed,
                                       filter_username=filter_username,
                                       created_since_time=created_since_datetime,
                                       updated_since_time=updated_since_datetime)
    if verbose:
        if completed:
            description = 'COMPLETED'
        else:
            description = 'OUTSTANDING'
        print('{} {} TODO ITEMS\n'.format(len(all_todos), description))
    for todo in all_todos:
        print(str(todo) + "\n")

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

    mode.add_argument('-c', '--completed', action='store_true',
                      help='Print all completed todo items in this PR')

    parser.add_argument('-u', '--filter-username',
                        help='Only show comments made by the given user')

    parser.add_argument('--created-since',
                        help='Only show comments created since the given date/time.\n'
                        '(Format can be YYYY-MM-DD or other ISO-formatted date/time strings.\n'
                        'Unless timezone is explicitly specified, date/time is assumed to be UTC.\n'
                        'Requires python 3.7 or later.)')

    parser.add_argument('--updated-since',
                        help='Only show comments updated since the given date/time.\n'
                        'Note that updated time is not available for the top-level PR comment\n'
                        'and for top-level review comments. So we show these if anything in the\n'
                        'PR has been updated since the given time.\n'
                        'Also: based on experimentation, it seems like GitHub may update the\n'
                        'last-updated time of comments more often than expected, so this option\n'
                        'may show more than expected.\n'
                        '(Format can be YYYY-MM-DD or other ISO-formatted date/time strings.\n'
                        'Unless timezone is explicitly specified, date/time is assumed to be UTC.\n'
                        'Requires python 3.7 or later.)')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()

    return args

def _date_string_to_datetime(string):
    """Convert the given string to a datetime.datetime object and return it

    string should be formatted as an ISO date/time (e.g., YYYY-MM-DD)

    If no timezone info is provided in the string, it is assumed to be in UTC.

    If string is None, then returns None
    """
    if string is None:
        return None
    return datetime.datetime.fromisoformat(string).astimezone()

"""Functions implementing gh-org-query tool"""

import argparse
from ghtools.github_fetch import fetch_organization

# ========================================================================
# Public functions
# ========================================================================

def main():
    """Main function called when gh-org-query is run from the command line"""
    args = _commandline_args()
    gh_org_query(org=args.org,
                 list_repos=args.list_repos)

def gh_org_query(org, list_repos):
    """Implementation of the gh-org-query command

    Args:
    org: string - Github organization
    list_repos: boolean - Whether to list all repositories in this organization
    """
    org = fetch_organization(org)
    if list_repos:
        for repo in org.get_repos(type='all', sort='full_name', direction='asc'):
            print(repo.full_name)

# ========================================================================
# Private functions
# ========================================================================

def _commandline_args():
    """Parse and return command-line arguments"""

    description = """
Tool for querying GitHub organizations

Currently only supports listing all repositories in an organization:
    gh-org-query -o ORG -r
"""

    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-o', '--org', required=True,
                        help='GitHub organization')

    mode = parser.add_mutually_exclusive_group(required=True)

    mode.add_argument('-r', '--list-repos', action='store_true',
                      help='List all repositories in the organization')

    args = parser.parse_args()

    return args

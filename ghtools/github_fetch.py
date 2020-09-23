"""Functions for fetching information from GitHub using the GitHub API"""

import os
from github import Github
from ghtools.comment import ConversationComment, PRReviewComment, PRLineComment
from ghtools.comment_time import CommentTime
from ghtools.pull_request import PullRequest

def fetch_pull_request(repo, pr_number):
    """Fetch information about the given Pull Request, returning a PullRequest object

    Args:
    repo: string - in the format Org/Repo
    pr_number: integer - PR ID in this repo
    """
    gh_inst = _get_github_instance()
    gh_repo = gh_inst.get_repo(repo)
    gh_pr = gh_repo.get_pull(pr_number)

    # This is the time that *anything* in the PR was last updated. We use this as a
    # conservative guess of when comments were last updated if we don't have any other
    # last-updated information for a given comment.
    pr_last_updated = gh_pr.updated_at.astimezone()

    comments = []
    for gh_comment in gh_pr.get_issue_comments():
        time_info = CommentTime(creation_time=gh_comment.created_at.astimezone(),
                                last_updated_time=gh_comment.updated_at.astimezone())
        this_comment = ConversationComment(username=gh_comment.user.login,
                                           time_info=time_info,
                                           url=gh_comment.html_url,
                                           content=gh_comment.body)
        comments.append(this_comment)

    for gh_comment in gh_pr.get_comments():
        time_info = CommentTime(creation_time=gh_comment.created_at.astimezone(),
                                last_updated_time=gh_comment.updated_at.astimezone())
        this_comment = PRLineComment(username=gh_comment.user.login,
                                     time_info=time_info,
                                     url=gh_comment.html_url,
                                     content=gh_comment.body,
                                     path=gh_comment.path)
        comments.append(this_comment)

    for gh_comment in gh_pr.get_reviews():
        if gh_comment.body:
            # GitHub creates a Pull Request Review for any PR line comments that have been
            # made - even individual line comments made outside a review, or when you make
            # a set of line comments in a review but don't leave an overall
            # comment. Exclude empty reviews that are created in these circumstances.

            # Pull Request Reviews don't appear to support a last-updated time, so we use
            # the last updated time of the PR as a whole as a conservative guess.
            time_info = CommentTime(creation_time=gh_comment.submitted_at.astimezone(),
                                    last_updated_time=pr_last_updated,
                                    updated_time_is_guess=True)
            this_comment = PRReviewComment(username=gh_comment.user.login,
                                           time_info=time_info,
                                           url=gh_comment.html_url,
                                           content=gh_comment.body)
            comments.append(this_comment)

    time_info = CommentTime(creation_time=gh_pr.created_at.astimezone(),
                            last_updated_time=pr_last_updated)
    return PullRequest(pr_number=pr_number,
                       title=gh_pr.title,
                       username=gh_pr.user.login,
                       time_info=time_info,
                       url=gh_pr.html_url,
                       body=gh_pr.body,
                       comments=comments)

def fetch_organization(org):
    """Fetch information about the given organization

    Returns an object of type github.Organization.Organization (part of the python github
    API)

    Args:
    org: string
    """
    gh_inst = _get_github_instance()
    return gh_inst.get_organization(org)

def _get_github_instance():
    """Returns an instance of the Github class"""
    return Github(login_or_token=_get_access_token())

def _get_access_token():
    """Get a GitHub personal access token from the environment, if one is set.

    This is not necessary for a public repository, but providing it allows for much higher
    limits for GitHub API's rate limiting. As long as you're working with a public
    repository, the token does not need any specific permissions - i.e., no
    scopes/permissions need to be checked. See
    https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
    for more details.
    """
    return os.environ.get("GITHUB_TOKEN")

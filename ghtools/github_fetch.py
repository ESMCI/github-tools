"""Functions for fetching information from GitHub using the GitHub API"""

from github import Github
from ghtools.comment import Comment
from ghtools.pull_request import PullRequest

def fetch_pull_request(repo, pr_number, access_token=None):
    """Fetch information about the given Pull Request, returning a PullRequest object

    Args:
    repo: string - in the format Org/Repo
    pr_number: integer - PR ID in this repo
    access_token: string or None - if specified, this should be a GitHub personal access token
        This is not necessary for a public repository, but providing it allows for much
        higher limits for GitHub API's rate limiting. As long as you're working with a
        public repository, the token does not need any specific permissions - i.e., no
        scopes/permissions need to be checked. See
        https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
        for more details.
    """
    gh_inst = Github(login_or_token=access_token)
    gh_repo = gh_inst.get_repo(repo)
    gh_pr = gh_repo.get_pull(pr_number)

    conversation_comments = []
    for gh_comment in gh_pr.get_issue_comments():
        this_comment = Comment(username=gh_comment.user.login,
                               creation_date=gh_comment.created_at,
                               url=gh_comment.html_url,
                               content=gh_comment.body)
        conversation_comments.append(this_comment)

    review_comments = []
    for gh_comment in gh_pr.get_comments():
        this_comment = Comment(username=gh_comment.user.login,
                               creation_date=gh_comment.created_at,
                               url=gh_comment.html_url,
                               content=gh_comment.body)
        review_comments.append(this_comment)

    return PullRequest(pr_number=pr_number,
                       title=gh_pr.title,
                       username=gh_pr.user.login,
                       creation_date=gh_pr.created_at,
                       url=gh_pr.html_url,
                       body=gh_pr.body,
                       conversation_comments=conversation_comments,
                       review_comments=review_comments)

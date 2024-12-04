import logging
import os
from typing import List

from dotenv import load_dotenv
from github import Github, Repository, Stargazer, RateLimit, NamedUser, GithubException
from github.PaginatedList import PaginatedList

load_dotenv()

# Authenticate using the GitHub token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# The per_page setting should ideally be customizable at least using a EV.
# Maybe initializing multiple clients for different use cases could be an approach.
# For example with per_page 10, 30 and 100, but it could also have other different settings.
# 100 is the maximum allowed for the parameter per_page : https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api
g = Github(GITHUB_TOKEN, per_page=100)

logger = logging.getLogger('uvicorn.error')


def _safe_github_call(func, *args, **kwargs):
    """
    Wraps GitHub API calls to handle exceptions specific to the GitHub API. Logs the error and raises a custom
    GitHubAPIException with additional context for further handling.

    Args:
        func (callable): The GitHub API function to execute.
        *args: Positional arguments for the GitHub API function.
        **kwargs: Keyword arguments for the GitHub API function.

    Returns:
        The result of the API function call if successful.
    """
    try:
        return func(*args, **kwargs)
    except GithubException as e:  # Catch only GitHub-related exceptions
        logger.error(f"GitHub API error ({e.__class__.__name__}) in function {func.__name__}: {e}")
        raise GitHubAPIException(f"Error calling GitHub API: {e}", code=e.status, github_exception=e)


def check_github_connection() -> None:
    """
    Check if GitHub connection is working by checking the token and hitting the rate limit endpoint.

    Returns:
        None

    Raises:
        Exception: If the GitHub API returns a non-200 status code
    """
    # Check if token is present
    if GITHUB_TOKEN is None:
        logger.critical("No GitHub token provided!")
        raise GitHubAPIException("GitHub token is missing.")

    # Check if rate limit is not reached
    try:
        rate_limit: RateLimit = _safe_github_call(g.get_rate_limit)
    except GithubException as e:
        logger.error(f"Failed to fetch rate limit: {e}")
        raise GitHubAPIException(f"GitHub API rate limit check failed: {e}")

    if rate_limit.core.remaining == 0:
        logger.error("GitHub API rate limit exceeded.")
        raise GitHubAPIException("Rate limit exceeded")

    logger.info("GitHub connection successful!")


def get_stargazers(owner: str, repo: str) -> PaginatedList[NamedUser] | None:
    """
    Fetch stargazers for a given repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.

    Returns:
        List[Stargazer] | None: A list of stargazer objects or None if the repository isn't found.
    """
    # Here we could make only one call by making a direct request to the GitHub API.
    repo = _safe_github_call(g.get_repo, f"{owner}/{repo}")
    if repo is None:
        return None  # Return an empty list if the repository was not found
    return _safe_github_call(repo.get_stargazers)


def get_starred_repos_for_user(user: NamedUser) -> PaginatedList[Repository]:
    """
    Fetch repositories starred by a given user.

    Args:
        user (NamedUser): The GitHub user object whose starred repositories we want to fetch.

    Returns:
        List[Repository]: List of repositories the user has starred.
    """
    # Multiple calls can be made here, PyGithub automatically manage the pagination.
    starred_repos: PaginatedList[Repository] = _safe_github_call(user.get_starred)
    return starred_repos


class GitHubAPIException(Exception):
    """Exception raised for errors related to GitHub API calls."""

    def __init__(self, message: str, code: int = None, github_exception: GithubException = None):
        super().__init__(message)
        self.message = message
        if code is not None:
            self.code = code
        elif github_exception:
            self.code = github_exception.status
        else:
            self.code = 500
        self.github_exception = github_exception

    def __str__(self):
        return f"GitHub API Error {self.code}: {self.message}"

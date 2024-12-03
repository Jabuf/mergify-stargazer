import logging
import os
from typing import List

from dotenv import load_dotenv
from github import Github, Repository, Stargazer, RateLimit, NamedUser
from github.PaginatedList import PaginatedList

# Load environment variables
load_dotenv()

# Authenticate using the GitHub token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)

logger = logging.getLogger('uvicorn.error')


def check_github_connection() -> None:
    """
    Check if GitHub connection is working by hitting the rate limit endpoint.

    Returns:
        None

    Raises:
        Exception: If the GitHub API returns a non-200 status code
    """
    if GITHUB_TOKEN is None:
        logger.error("No GitHub token provided!")
    rate_limit: RateLimit = g.get_rate_limit()
    if rate_limit.core.remaining == 0:
        raise Exception("Rate limit exceeded")
    logger.info("GitHub connection successful!")


def get_stargazers(owner: str, repo: str) -> PaginatedList[NamedUser]:
    """
    Fetch stargazers for a given repository.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.

    Returns:
        List[Stargazer]: A list of stargazer objects.
    """
    repo: Repository = g.get_repo(f"{owner}/{repo}")
    return repo.get_stargazers()


def get_starred_repos_for_user(user: NamedUser) -> PaginatedList[Repository]:
    """
    Fetch repositories starred by a given user.

    Args:
        user (NamedUser): The GitHub user object whose starred repositories we want to fetch.

    Returns:
        List[Repository]: List of repositories the user has starred.
    """
    starred_repos: PaginatedList[Repository] = user.get_starred()
    return starred_repos

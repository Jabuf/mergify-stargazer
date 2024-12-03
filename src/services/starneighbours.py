import logging
from collections import defaultdict
from typing import List, Dict

from github import Repository, GithubException
from github.NamedUser import NamedUser
from github.PaginatedList import PaginatedList

from src.services.github import get_stargazers, get_starred_repos_for_user

logger = logging.getLogger('uvicorn.error')


def get_repository_neighbours(owner: str, repo: str) -> List[Dict]:
    """
    Find the neighbouring repositories based on shared stargazers.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.

    Returns:
        List[Dict]: A list of repositories with shared stargazers.
    """
    try:
        # Step 1: Get stargazers for the given repository
        stargazers: PaginatedList[NamedUser] = get_stargazers(owner, repo)
        if not stargazers:
            logger.warning(f"No stargazers found for {repo} by {owner}")
            return []

    except GithubException as e:
        logger.error(f"GitHub API error while fetching stargazers for {repo} by {owner}: {e}")
        raise

    # Step 2: Build a map of repositories to users who starred them
    repo_to_users: Dict[str, set[str]] = defaultdict(set)

    if stargazers is None:
        return []

    for stargazer in stargazers:
        try:
            starred_repos: PaginatedList[Repository] = get_starred_repos_for_user(stargazer)
        except GithubException as e:
            logger.error(f"GitHub API error while fetching starred repositories for {stargazer.login}: {e}")
            continue

        # Step 3: Add the stargazer to each repository they have starred
        for starred_repo in starred_repos:
            repo_to_users[starred_repo.full_name].add(stargazer.login)

    # Step 4: Identify neighbours (repos with shared stargazers)
    neighbours: List[Dict] = []
    for neighbour_repo, users in repo_to_users.items():
        if neighbour_repo != f"{owner}/{repo}":  # Avoid the same repository
            shared_stargazers: set[str] = users.intersection([s.login for s in stargazers])
            if shared_stargazers:
                neighbours.append({
                    "repo": neighbour_repo,
                    "stargazers": list(shared_stargazers)
                })

    return neighbours

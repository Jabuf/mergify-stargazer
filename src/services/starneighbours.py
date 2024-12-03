from collections import defaultdict
from typing import List, Dict

from github import Repository
from github.NamedUser import NamedUser
from github.PaginatedList import PaginatedList

from src.services.github import get_stargazers, get_starred_repos_for_user


def get_repository_neighbours(owner: str, repo: str) -> List[Dict]:
    """
    Find the neighbouring repositories based on shared stargazers.

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.

    Returns:
        List[Dict]: A list of repositories with shared stargazers.
    """
    # Step 1: Get stargazers for the given repository
    try:
        stargazers: PaginatedList[NamedUser] = get_stargazers(owner, repo)
    except Exception as e:
        raise Exception(f"Failed to get stargazers for {owner}/{repo}: {e}")

    # Step 2: Build a map of repositories to users who starred them
    repo_to_users: Dict[str, set[str]] = defaultdict(set)

    for stargazer in stargazers:
        try:
            starred_repos: PaginatedList[Repository] = get_starred_repos_for_user(stargazer)
        except Exception as e:
            raise Exception(f"Failed to get starred repositories for user {stargazer.login}: {e}")

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

from fastapi import APIRouter, HTTPException
from github import GithubException

from src.config.urls import ROUTE_STARNEIGHBOURS
from src.services.github import GitHubAPIException
from src.services.starneighbours import get_repository_neighbours

router = APIRouter()


@router.get(ROUTE_STARNEIGHBOURS)
def get_star_neighbours(user: str, repo: str):
    try:
        starneighbours = get_repository_neighbours(user, repo)
    except GitHubAPIException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

    if not starneighbours:
        raise HTTPException(status_code=404, detail=f"Repository {repo} by {user} has no neighbours.")

    return starneighbours

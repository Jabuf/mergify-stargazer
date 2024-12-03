import logging
import time

from fastapi import APIRouter, HTTPException

from src.config.urls import ROUTE_STARNEIGHBOURS
from src.services.github import GitHubAPIException
from src.services.starneighbours import get_repository_neighbours

router = APIRouter()
logger = logging.getLogger('uvicorn.error')


@router.get(ROUTE_STARNEIGHBOURS)
def get_star_neighbours(user: str, repo: str):
    start_time = time.time()
    try:
        starneighbours = get_repository_neighbours(user, repo)
    except GitHubAPIException as e:
        raise HTTPException(status_code=e.code, detail=e.message)

    if not starneighbours:
        raise HTTPException(status_code=404, detail=f"Repository {repo} by {user} has no neighbours.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"Request took {elapsed_time:.2f} seconds.")

    return starneighbours

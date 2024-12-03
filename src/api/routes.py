from fastapi import APIRouter

from src.config.urls import ROUTE_STARNEIGHBOURS
from src.services.starneighbours import get_repository_neighbours

router = APIRouter()


@router.get(ROUTE_STARNEIGHBOURS)
def get_star_neighbours(user: str, repo: str):
    return  get_repository_neighbours(user, repo)

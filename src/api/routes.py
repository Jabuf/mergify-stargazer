from fastapi import APIRouter

from src.config.urls import ROUTE_STARNEIGHBOURS

router = APIRouter()

@router.get(ROUTE_STARNEIGHBOURS)
def get_star_neighbours(user: str, repo: str):
    return {"message": "To implement"}

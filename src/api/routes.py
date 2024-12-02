from fastapi import APIRouter

router = APIRouter()

@router.get("/repos/{user}/{repo}/starneighbours")
def get_star_neighbours(user: str, repo: str):
    return {"message": "To implement"}

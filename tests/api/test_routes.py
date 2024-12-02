from fastapi.testclient import TestClient

from src.config.urls import ROUTE_STARNEIGHBOURS, API_VERSION
from src.main import app

client = TestClient(app)


def test_get_star_neighbours():
    url = API_VERSION+ROUTE_STARNEIGHBOURS.format(user="user", repo="repo")
    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == {"message": "To implement"}

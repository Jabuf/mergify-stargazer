from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_star_neighbours():
    # Arrange: Define test input
    user = "user"
    repo = "repo"
    url = f"/repos/{user}/{repo}/starneighbours"

    # Act: Make a request to the endpoint
    response = client.get(url)

    # Assert: Check the response
    assert response.status_code == 200
    assert response.json() == {"message": "To implement"}

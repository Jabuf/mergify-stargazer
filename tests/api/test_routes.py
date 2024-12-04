import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.config.urls import ROUTE_STARNEIGHBOURS, API_VERSION
from src.main import app
from src.utils.jwt_handler import JWTHandler


class TestStarNeighboursEndpoint(unittest.TestCase):

    @patch('src.api.routes.get_repository_neighbours')
    def test_get_star_neighbours(self, mock_get_repository_neighbours):
        # Mock data for the expected response
        mock_neighbours = [
            {"repo": "owner/repo1", "stargazers": ["userA", "userB"]},
            {"repo": "owner/repo2", "stargazers": ["userA", "userB"]}
        ]
        mock_get_repository_neighbours.return_value = mock_neighbours

        # Create the TestClient instance
        client = TestClient(app)

        # Generate a valid JWT token
        valid_token = JWTHandler._generate_token({"username": "valid_user"}, secret=JWTHandler.access_secret, lifetime=JWTHandler.access_token_lifetime)

        # Simulate a GET request to /starneighbours
        url = API_VERSION + ROUTE_STARNEIGHBOURS.format(user="owner", repo="repo")
        headers = {"Authorization": f"Bearer {valid_token}"}
        response = client.get(url, headers=headers)

        # Assertions
        mock_get_repository_neighbours.assert_called_once_with("owner", "repo")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_neighbours)


if __name__ == '__main__':
    unittest.main()

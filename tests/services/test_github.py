import unittest
from unittest.mock import patch, MagicMock

from github import Repository

from src.services.github import get_stargazers, get_starred_repos_for_user


class TestGitHubService(unittest.TestCase):

    @patch('github.Github.get_repo')  # Mocking get_repo method to return a mock repo
    def test_get_stargazers(self, mock_get_repo):
        # Mock the return value of get_stargazers
        mock_stargazers = [
            {"login": "userA", "id": 1, "starred_at": "2024-12-01T12:00:00Z"},
            {"login": "userB", "id": 2, "starred_at": "2024-12-02T12:00:00Z"}
        ]

        # Mock the repo to return our mocked stargazers
        mock_repo = mock_get_repo.return_value
        mock_repo.get_stargazers.return_value = mock_stargazers

        # Call the function to test
        owner = "octocat"
        repo = "hello-world"
        stargazers = get_stargazers(owner, repo)

        # Assertions
        mock_get_repo.assert_called_once_with(f"{owner}/{repo}")
        mock_repo.get_stargazers.assert_called_once()
        self.assertEqual(stargazers[0]["login"], "userA")  # Check login of first stargazer
        self.assertEqual(stargazers[1]["id"], 2)  # Check ID of second stargazer

    @patch('github.Github.get_user')  # Mocking the get_user method to return a mock user
    def test_get_starred_repos_for_user(self, mock_get_user):
        # Mock the user object
        mock_user = MagicMock()

        # Mock the return value of get_starred (a PaginatedList of Repository objects)
        mock_starred_repos = [
            MagicMock(spec=Repository, full_name="repo1"),
            MagicMock(spec=Repository, full_name="repo2"),
            MagicMock(spec=Repository, full_name="repo3")
        ]

        # Set the mock to return the mocked starred repositories
        mock_user.get_starred.return_value = mock_starred_repos

        # Mock the get_user to return our mock_user
        mock_get_user.return_value = mock_user

        starred_url = "userA/starred_url"
        starred_repos = get_starred_repos_for_user(starred_url)

        # Assertions
        mock_get_user.assert_called_once_with(starred_url)
        mock_user.get_starred.assert_called_once()
        self.assertEqual(starred_repos[0].full_name, "repo1")  # Check if the full_name matches


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock

from github import Repository
from github.NamedUser import NamedUser

from src.services.github import get_stargazers, get_starred_repos_for_user


class TestGitHubService(unittest.TestCase):

    @patch('github.Github.get_repo')
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
        self.assertEqual(stargazers[0]["login"], "userA")
        self.assertEqual(stargazers[1]["id"], 2)

    @patch('src.services.starneighbours.NamedUser.get_starred')
    def test_get_starred_repos_for_user(self, mock_get_starred):
        # Mock data for starred repositories
        mock_repo_1 = MagicMock(spec=Repository, full_name="owner/repo1")
        mock_repo_2 = MagicMock(spec=Repository, full_name="owner/repo2")
        mock_starred_repos = [mock_repo_1, mock_repo_2]

        # Mock the return value of get_starred
        mock_get_starred.return_value = mock_starred_repos

        # Create a mock user and mock the get_starred method
        mock_user = MagicMock(spec=NamedUser)
        mock_user.get_starred = mock_get_starred

        # Call the function to test
        starred_repos = get_starred_repos_for_user(mock_user)

        # Assertions
        mock_get_starred.assert_called_once()
        self.assertEqual(starred_repos, mock_starred_repos)


if __name__ == '__main__':
    unittest.main()

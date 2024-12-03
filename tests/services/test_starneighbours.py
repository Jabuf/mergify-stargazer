import unittest
from unittest.mock import patch, MagicMock

from src.services.starneighbours import get_repository_neighbours


class TestGitHubService(unittest.TestCase):

    @patch('src.services.starneighbours.get_stargazers')
    @patch('src.services.starneighbours.get_starred_repos_for_user')
    def test_get_repository_neighbours(self, mock_get_starred_repos_for_user, mock_get_stargazers):
        mock_stargazers = [
            MagicMock(login="userA"),
            MagicMock(login="userB")
        ]
        mock_repo_1 = MagicMock(full_name="owner/repo1")
        mock_repo_2 = MagicMock(full_name="owner/repo2")
        mock_starred_repos = [mock_repo_1, mock_repo_2]

        mock_get_stargazers.return_value = mock_stargazers
        mock_get_starred_repos_for_user.return_value = mock_starred_repos

        owner = "owner"
        repo = "repo"
        neighbours = get_repository_neighbours(owner, repo)

        mock_get_stargazers.assert_called_once_with(owner, repo)

        mock_get_starred_repos_for_user.assert_any_call(
            mock_stargazers[0])

        expected_neighbours = [
            {"repo": "owner/repo1", "stargazers": sorted(["userA", "userB"])},
            {"repo": "owner/repo2", "stargazers": sorted(["userA", "userB"])}
        ]

        for neighbour in neighbours:
            stargazers = neighbour["stargazers"]
            if neighbour["repo"] == "owner/repo1":
                self.assertCountEqual(stargazers, ["userA", "userB"])
            elif neighbour["repo"] == "owner/repo2":
                self.assertCountEqual(stargazers, ["userA", "userB"])


if __name__ == '__main__':
    unittest.main()

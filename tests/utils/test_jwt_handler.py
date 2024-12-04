import unittest

from src.utils.jwt_handler import JWTHandler, AuthenticationError


class TestJWTHandler(unittest.TestCase):

    def setUp(self):
        # Mock environment variables
        JWTHandler.access_secret = "test_access_secret"
        JWTHandler.refresh_secret = "test_refresh_secret"
        JWTHandler.access_token_lifetime = 300
        JWTHandler.refresh_token_lifetime = 1800
        self.user_info = {"userName": "Test"}

    def test_generate_authentication_tokens(self):
        tokens = JWTHandler.generate_authentication_tokens(self.user_info)
        self.assertIn("accessToken", tokens)
        self.assertIn("refreshToken", tokens)

    def test_verify_token_valid(self):
        tokens = JWTHandler.generate_authentication_tokens(self.user_info)
        JWTHandler.verify_token(tokens["accessToken"], JWTHandler.access_secret)

    def test_verify_token_expired(self):
        expired_token = JWTHandler._generate_token(
            self.user_info, JWTHandler.access_secret, -1
        )
        with self.assertRaises(AuthenticationError):
            JWTHandler.verify_token(expired_token, JWTHandler.access_secret)

    def test_refresh_tokens(self):
        tokens = JWTHandler.generate_authentication_tokens(self.user_info)
        refreshed_tokens = JWTHandler.refresh_tokens(tokens["refreshToken"])
        self.assertIn("accessToken", refreshed_tokens)
        self.assertIn("refreshToken", refreshed_tokens)

    def test_decode_token(self):
        tokens = JWTHandler.generate_authentication_tokens(self.user_info)
        decoded = JWTHandler.decode_token(tokens["accessToken"], JWTHandler.access_secret)
        self.assertEqual(decoded["userName"], self.user_info["userName"])

    def test_check_secrets_invalid(self):
        JWTHandler.access_secret = "same_secret"
        JWTHandler.refresh_secret = "same_secret"
        with self.assertRaises(AuthenticationError):
            JWTHandler.check_secrets()

    def test_check_secrets_valid(self):
        JWTHandler.access_secret = "test_access_secret"
        JWTHandler.refresh_secret = "test_refresh_secret"
        try:
            JWTHandler.check_secrets()
        except AuthenticationError:
            self.fail()


if __name__ == "__main__":
    unittest.main()

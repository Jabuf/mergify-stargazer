import os
from time import time
from typing import TypedDict, Dict

import jwt


# Define a custom exception for invalid tokens
class AuthenticationError(Exception):
    pass


# The structure of the JWT payload
class UserInformationJWT(TypedDict):
    userName: str


# Structure for returned tokens
class AuthenticationTokens(TypedDict):
    accessToken: str
    refreshToken: str


class JWTHandler:
    # Missing secrets will lead to an error when starting the application, which is intended since secrets are mandatory
    access_secret: str = os.getenv("ACCESS_TOKEN_SECRET",
                                   "")
    refresh_secret: str = os.getenv("REFRESH_TOKEN_SECRET", "")
    access_token_lifetime: int = int(os.getenv("ACCESS_TOKEN_LIFETIME", 300))  # in seconds
    refresh_token_lifetime: int = int(os.getenv("REFRESH_TOKEN_LIFETIME", 1800))  # in seconds

    @staticmethod
    def generate_authentication_tokens(user_info: UserInformationJWT) -> AuthenticationTokens:
        """
        Generate access and refresh tokens for a user.

        Args:
            user_info (UserInformationJWT): The user information to include in the tokens.

        Returns:
            AuthenticationTokens: A dictionary containing the access token and refresh token.
        """
        return {
            "accessToken": JWTHandler._generate_token(
                user_info, JWTHandler.access_secret, JWTHandler.access_token_lifetime
            ),
            "refreshToken": JWTHandler._generate_token(
                user_info, JWTHandler.refresh_secret, JWTHandler.refresh_token_lifetime
            ),
        }

    @staticmethod
    def _generate_token(payload: Dict, secret: str, lifetime: int) -> str:
        """
        Generate a single JWT.

        Args:
            payload (Dict): The data to include in the token's payload.
            secret (str): The secret key to sign the token.
            lifetime (int): The token's expiration time in seconds.

        Returns:
            str: The encoded JWT.
        """
        payload["exp"] = int(time() + lifetime)
        # We could extract the algorithm used in a single EV
        return jwt.encode(payload, secret, algorithm="HS256")

    @staticmethod
    def verify_token(token: str, secret: str) -> None:
        """
        Verify the validity of a given JWT.

        Args:
            token (str): The token to verify.
            secret (str): The secret key that was used to sign the token.

        Raises:
            AuthenticationError: If the token is expired or invalid.
        """
        try:
            jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token.")

    @staticmethod
    def refresh_tokens(refresh_token: str) -> AuthenticationTokens:
        """
        Refresh authentication tokens using a valid refresh token.

        Args:
            refresh_token (str): The refresh token to validate and use for generating new tokens.

        Returns:
            AuthenticationTokens: A dictionary containing the new access token and refresh token.

        Raises:
            AuthenticationError: If the refresh token is invalid or expired.
        """
        JWTHandler.verify_token(refresh_token, JWTHandler.refresh_secret)
        decoded = JWTHandler.decode_token(refresh_token, JWTHandler.refresh_secret)
        return JWTHandler.generate_authentication_tokens(decoded)

    @staticmethod
    def decode_token(token: str, secret:str) -> UserInformationJWT:
        """
        Decode a token to extract its payload.

        Args:
            token (str): The token to decode.
            secret (str): The secret key that was used to sign the token.

        Returns:
            UserInformationJWT: An object containing the user information extracted from the token.

        Raises:
            AuthenticationError: If the token is invalid or decoding fails.
        """
        decoded = jwt.decode(token, secret, algorithms="HS256")
        return UserInformationJWT(
            userName=decoded["userName"],
        )

    @staticmethod
    def check_secrets():
        """
        Check the validity of the secrets used for JWT generation.

        Raises:
            AuthenticationError: If the access or refresh token secrets are missing or identical.
        """
        if not JWTHandler.access_secret or not JWTHandler.refresh_secret or JWTHandler.access_secret == JWTHandler.refresh_secret:
            raise AuthenticationError("Invalid or missing JWT secrets.")

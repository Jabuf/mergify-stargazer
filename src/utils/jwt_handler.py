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
    _access_secret = os.getenv("ACCESS_TOKEN_SECRET", "") # An empty string will lead to an error, which is intended since a secret is mandatory
    _refresh_secret = os.getenv("REFRESH_TOKEN_SECRET", "")
    _access_token_lifetime = int(os.getenv("ACCESS_TOKEN_LIFETIME", 300))  # in seconds
    _refresh_token_lifetime = int(os.getenv("REFRESH_TOKEN_LIFETIME", 1800))  # in seconds

    @staticmethod
    def generate_authentication_tokens(user_info: UserInformationJWT) -> AuthenticationTokens:
        """
        Generate access and refresh tokens.
        """
        return {
            "accessToken": JWTHandler._generate_token(
                user_info, JWTHandler._access_secret, JWTHandler._access_token_lifetime
            ),
            "refreshToken": JWTHandler._generate_token(
                user_info, JWTHandler._refresh_secret, JWTHandler._refresh_token_lifetime
            ),
        }

    @staticmethod
    def _generate_token(payload: Dict, secret: str, lifetime: int) -> str:
        """
        Generate a single JWT.
        """
        payload["exp"] = int(time() + lifetime)
        return jwt.encode(payload, secret, algorithm="HS256")

    @staticmethod
    def verify_token(token: str, secret: str) -> None:
        """
        Verify a token's validity.
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
        """
        JWTHandler.verify_token(refresh_token, JWTHandler._refresh_secret)
        decoded = JWTHandler.decode_token(refresh_token)
        return JWTHandler.generate_authentication_tokens(decoded)

    @staticmethod
    def decode_token(token: str) -> UserInformationJWT:
        """
        Decode a token to extract payload.
        """
        decoded = jwt.decode(token, options={"verify_signature": False})
        return UserInformationJWT(
            userName=decoded["userName"],
        )

    @staticmethod
    def check_secrets():
        """
        Throw an error if the secrets used to generate the JWTs aren't valid.
        To be valid you must have both the secret for the access and refresh token filled in the environment variables (see the corresponding keys above), and they must be different.
        """
        if not JWTHandler._access_secret or not JWTHandler._refresh_secret or JWTHandler._access_secret == JWTHandler._refresh_secret:
            raise AuthenticationError("Invalid or missing JWT secrets.")
import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse

from src.api.routes import router
from src.config.urls import API_VERSION
from src.services.github import check_github_connection, GitHubAPIException
from src.utils.jwt_handler import JWTHandler, AuthenticationError

# Load environment variables from .env
load_dotenv()

log_level = os.getenv("LOG_LEVEL", logging.DEBUG)

logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger('uvicorn.error')
logger.info("Log level : " + log_level)

app = FastAPI()

# Check if GitHub connection is valid
try:
    check_github_connection()
except GitHubAPIException as e:
    logger.critical(f"GitHub API error: {e}")
# Check if JWT secrets are present
try:
    JWTHandler.check_secrets()
except AuthenticationError as e:
    logger.critical(f"Configuration error: {e}")


# Middleware for JWT validation
@app.middleware("http")
async def jwt_validation_middleware(request: Request, call_next):
    """
    Middleware to validate JWT for specific routes.
    """
    if request.url.path.startswith(API_VERSION):  # Need to be adapted
        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse({"error": "Missing token"}, status_code=401)
        try:
            token = token.split("Bearer ")[1]
            JWTHandler.verify_token(token, JWTHandler.access_secret)
        except AuthenticationError as ex:
            return JSONResponse({"error": str(ex)}, status_code=401)

    response = await call_next(request)
    return response


app.include_router(router, prefix=API_VERSION)


def print_openapi_schema():
    openapi_schema = get_openapi(title="Stargazer API", version="1.0.0", routes=app.routes)
    for path, path_info in openapi_schema["paths"].items():
        for method, operation in path_info.items():
            print(f"{method.upper()} {path} -> {operation.get('summary', 'No summary')}")


app.add_event_handler("startup", print_openapi_schema)


@app.get("/")
def read_root():
    return {"Mergify Stagazer": "A technical showcase project developed as part of the hiring process at Mergify"}


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port, log_level=log_level)

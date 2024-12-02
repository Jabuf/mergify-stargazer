import logging
import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.routes import router
from src.config.urls import API_VERSION
from src.services.github import check_github_connection

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
check_github_connection()

app.include_router(router, prefix=API_VERSION)


@app.get("/")
def read_root():
    return {"Mergify Stagazer": "A technical showcase project developed as part of the hiring process at Mergify"}


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port, log_level=log_level)

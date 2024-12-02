import os
from typing import Union

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from src.api import router
from src.config.urls import API_VERSION
from src.services.github import check_github_connection

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Check if GitHub connection is valid
check_github_connection()

app.include_router(router, prefix=API_VERSION)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)

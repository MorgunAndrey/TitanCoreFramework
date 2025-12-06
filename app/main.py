# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware 
import logging.config
import sys
from pathlib import Path
import os


sys.path.append(str(Path(__file__).parent.parent))

from config import route
from config.app import settings
from config.logging import LOGGING

app = FastAPI(title=settings.appBaseName)

logging.config.dictConfig(LOGGING)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "fallback-dev-key-only-for-dev"), 
    session_cookie="session",      
    max_age=60 * 60 * 24 * 7   
)

app.include_router(route.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


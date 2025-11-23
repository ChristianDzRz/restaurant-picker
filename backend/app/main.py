from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, restaurants
from app.core.config import settings
from app.db.base import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI.
    Runs on startup and shutdown.
    """
    # Startup: Initialize database
    print("Initializing database...")
    await init_db()
    print("Database initialized!")

    yield

    # Shutdown: cleanup if needed
    print("Shutting down...")


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later: restrict to frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(restaurants.router)

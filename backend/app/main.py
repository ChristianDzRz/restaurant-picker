from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health, restaurants
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
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

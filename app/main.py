import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables BEFORE any other imports that might need them
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.routes import router
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    init_db()
    yield

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator", lifespan=lifespan)

# Mount static files
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Include routes
app.include_router(router)

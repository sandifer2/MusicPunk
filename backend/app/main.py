from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import test_connection, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting MusicBox")
    print("Testing db connection")
    if not test_connection():
        raise RuntimeError("DB connection failed")
    yield #split startup and shutdown
    print("Shutting down MusicBox API")
    engine.dispose()

app = FastAPI(
    title="MusicBoxAPI",
    lifespan=lifespan
)

@app.get("/")
async def health_check():
    return {
        "message": "API is running",
        "status": "healthy"
    }
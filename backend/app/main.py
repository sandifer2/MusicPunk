from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from app.database import get_db, test_connection

app = FastAPI(
    title="MusicBoxAPI"
)

@app.on_event("startup")
async def startup_check():
    '''Check db connection on startup'''
    print("Starting MusicBox")
    print("Testing db connection")
    test_connection()

@app.get("/")
async def health_check():
    return {
        "message": "API is running",
        "status": "healthy"
    }

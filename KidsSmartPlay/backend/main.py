# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.exercise_store import load_exercises

app = FastAPI(
    title="SmartPlay AI",
    description="Daily AI-generated cognitive games for kids",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/game/{num}")
def get_game(num: int):
    exercises = load_exercises()
    if num < 1:
        num = 1

    if num > len(exercises):
        return {
            "message": "All exercises completed"
        }
    return exercises[num-1]

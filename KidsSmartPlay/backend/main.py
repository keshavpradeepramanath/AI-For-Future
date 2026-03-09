# backend/main.py

from fastapi import FastAPI
from workflows.game_workflow import workflow
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def home():

    return {
        "message": "SmartPlay AI running",
        "endpoint": "/game/{day}"
    }


@app.get("/game/{day}")
def generate_game(day: int):

    result = workflow.invoke({"day": day})

    return result

# backend/schemas/game_schema.py

from pydantic import BaseModel
from typing import List, Optional


class Game(BaseModel):

    day: int

    game_name: str

    skill: str

    type: str

    instruction: str

    question: Optional[str] = None

    objects: Optional[List[str]] = None

    options: Optional[List[str]] = None

    answer: Optional[str] = None

    difficulty: str = "easy"

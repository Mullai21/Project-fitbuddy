from pydantic import BaseModel, Field
from typing import Literal

class UserInput(BaseModel):
    name: str = Field(...)
    user_id: str = Field(...)
    age: int = Field(gt=0, lt=120)
    weight: float = Field(gt=0)
    goal: str = Field(...)
    intensity: Literal['low', 'medium', 'high'] = Field(...)

class FeedbackRequest(BaseModel):
    user_id: str = Field(...)
    feedback: str = Field(min_length=3)

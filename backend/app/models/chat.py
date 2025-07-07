from typing import List
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class ChatAnswer(BaseModel):
    answer: str
    images: List[str] = []
    videos: List[str] = []

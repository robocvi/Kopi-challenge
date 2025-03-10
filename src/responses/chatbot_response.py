from pydantic import BaseModel
from typing import List, Literal

class Message(BaseModel):
    role: Literal["user", "bot"]
    message: str

class ChatBotResponse(BaseModel):
    conversation_id: str
    messages: List[Message]

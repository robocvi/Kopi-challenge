from pydantic import BaseModel
from typing import Optional

class ChatbotRequest(BaseModel):
    conversation_id: Optional[str]
    message: str
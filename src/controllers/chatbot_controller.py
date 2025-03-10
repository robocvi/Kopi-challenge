from src.settings import OPENAI_API_KEY
from src.requests.chatbot_request import ChatbotRequest
from src.responses.chatbot_response import ChatBotResponse, Message

class ChatbotController:
    @staticmethod
    def ask_chatbot(request: ChatbotRequest) -> ChatBotResponse:
        user_message = Message(role="user", message=request.message)
        conversation_history = [user_message]
        return ChatBotResponse(conversation_id="1", messages=conversation_history)

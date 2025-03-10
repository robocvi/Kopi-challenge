from openai import OpenAI
import uuid
from pymongo import MongoClient

from src.settings import OPENAI_API_KEY, MONGO_DB_CONNECTION_STRING
from src.requests.chatbot_request import ChatbotRequest
from src.responses.chatbot_response import ChatBotResponse, Message

client = OpenAI(api_key=OPENAI_API_KEY)

mongo_client = MongoClient(MONGO_DB_CONNECTION_STRING)
db = mongo_client["chatbot_db"]
conversations_collection = db["conversations"]

class ChatbotController:

    @staticmethod
    def first_message(request: ChatbotRequest) -> ChatBotResponse:
        response = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {"role": "system", "content": f'''Hold a debate in which you defend an irrational stance and try to convince the user that it is true. You must maintain your position persuasively and coherently throughout the entire conversation, no matter how absurd the idea may be. You must not give in to counterarguments or admit that the stance is incorrect.  
            Your goal is to persuade me without being overly aggressive or confrontational, using internal logic, subtle fallacies if necessary, and effective rhetorical techniques. Keep your responses concise while still making strong, persuasive arguments.  
            Here is the statement you must defend: {request.message}'''}
          ]
        )
        response_message = response.choices[0].message.content

        first_user_message = Message(role="user", message=request.message)
        first_bot_message = Message(role="bot", message=response_message)

        conversation_history = [first_user_message, first_bot_message]

        conversation_id = str(uuid.uuid4())
        conversations_collection.insert_one({
            "_id": conversation_id,
            "messages": [
                {"role": "user", "message": request.message},
                {"role": "bot", "message": response_message}
            ]
        })

        return ChatBotResponse(conversation_id=conversation_id, messages=conversation_history)

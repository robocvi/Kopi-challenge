from openai import OpenAI
import uuid
from pymongo import MongoClient

from src.settings import OPENAI_API_KEY, MONGO_DB_CONNECTION_STRING, LLM_MODEL
from src.requests.chatbot_request import ChatbotRequest
from src.responses.chatbot_response import ChatBotResponse, Message

client = OpenAI(api_key=OPENAI_API_KEY)

mongo_client = MongoClient(MONGO_DB_CONNECTION_STRING)
db = mongo_client["chatbot_db"]
conversations_collection = db["conversations"]

class ChatbotController:

    @staticmethod
    def first_message(request: ChatbotRequest) -> ChatBotResponse:
        system_message = f'''Hold a debate in which you defend an irrational stance and try to convince the user that it is true. You must maintain your position persuasively and coherently throughout the entire conversation, no matter how absurd the idea may be. You must not give in to counterarguments or admit that the stance is incorrect.  
        Your goal is to persuade me without being overly aggressive or confrontational, using internal logic, subtle fallacies if necessary, and effective rhetorical techniques. Keep your responses concise while still making strong, persuasive arguments.  
        Here is the statement you must defend: {request.message}'''
        response = client.chat.completions.create(
          model=LLM_MODEL,
          messages=[{"role": "system", "content": system_message}]
        )
        response_message = response.choices[0].message.content

        first_user_message = Message(role="user", message=request.message)
        first_bot_message = Message(role="bot", message=response_message)

        conversation_history = [first_user_message, first_bot_message]

        conversation_id = str(uuid.uuid4())
        conversations_collection.insert_one({
            "_id": conversation_id,
            "messages": [
                {"role": "system", "message": system_message},
                {"role": "user", "message": request.message},
                {"role": "bot", "message": response_message}
            ]
        })

        return ChatBotResponse(conversation_id=conversation_id, messages=conversation_history)
    
    @staticmethod
    def continue_conversation(request: ChatbotRequest) -> ChatBotResponse:
        conversation_id = request.conversation_id
        conversation = conversations_collection.find_one({"_id": conversation_id})
        if not conversation:
            raise ValueError(f"Conversation ID '{conversation_id}' not found in the database.")
        
        messages = conversation["messages"]
        formatted_messages = [{"role": msg["role"].replace("bot", "assistant"), "content": msg["message"]} for msg in messages]
        
        formatted_messages.append({"role": "user", "content": request.message})
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=formatted_messages
        )
        response_message = response.choices[0].message.content
        conversations_collection.update_one(
            {"_id": conversation_id},
            {"$push": {"messages":
                {"role": "user", "message": request.message}
            }}
        )
        conversations_collection.update_one(
            {"_id": conversation_id},
            {"$push": {"messages":
                {"role": "bot", "message": response_message}
            }}
        )
        messages.pop(0)
        conversation_history = [Message(role=msg["role"], message=msg["message"]) for msg in messages[-8:]]
        conversation_history.append(Message(role="user", message=request.message))
        conversation_history.append(Message(role="bot", message=response_message))
        
        return ChatBotResponse(conversation_id=conversation_id, messages=conversation_history)

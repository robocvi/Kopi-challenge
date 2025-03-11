from fastapi import FastAPI, HTTPException
from src.requests.chatbot_request import ChatbotRequest
from src.controllers.chatbot_controller import ChatbotController
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Prueba kopi-challenge API!"}

@app.post("/kopi-chatbot", tags=["Chatbot"])
async def chatbot(request: ChatbotRequest):
    try:
        conversation_id = request.conversation_id
        if not conversation_id:
            return ChatbotController.first_message(request)
        else:
            return ChatbotController.continue_conversation(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
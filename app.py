from fastapi import FastAPI
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
    return ChatbotController.ask_chatbot(request)
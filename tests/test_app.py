import pytest
from fastapi.testclient import TestClient
from app import app
from unittest.mock import patch, MagicMock
from src.controllers.chatbot_controller import ChatbotController
from src.requests.chatbot_request import ChatbotRequest
from src.responses.chatbot_response import ChatBotResponse, Message

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Prueba kopi-challenge API!"}

@patch.object(ChatbotController, "first_message")
def test_chatbot_first_message(mock_first_message):
    mock_response = ChatBotResponse(
        conversation_id="12345",
        messages=[Message(role="user", message="Hello"), Message(role="bot", message="Hi there!")]
    )
    mock_first_message.return_value = mock_response

    response = client.post("/kopi-chatbot", json={"conversation_id": None, "message": "Hello"})
    assert response.status_code == 200
    assert response.json() == {
        "conversation_id": "12345",
        "messages": [
            {"role": "user", "message": "Hello"},
            {"role": "bot", "message": "Hi there!"}
        ]
    }
    mock_first_message.assert_called_once()

@patch.object(ChatbotController, "continue_conversation")
def test_chatbot_continue_conversation(mock_continue_conversation):
    mock_response = ChatBotResponse(
        conversation_id="12345",
        messages=[Message(role="user", message="Hello"), Message(role="bot", message="Hi there!")]
    )
    mock_continue_conversation.return_value = mock_response

    response = client.post("/kopi-chatbot", json={"conversation_id": "12345", "message": "Hello"})
    assert response.status_code == 200
    assert response.json() == {
        "conversation_id": "12345",
        "messages": [
            {"role": "user", "message": "Hello"},
            {"role": "bot", "message": "Hi there!"}
        ]
    }
    mock_continue_conversation.assert_called_once()

@patch.object(ChatbotController, "continue_conversation", side_effect=ValueError("Conversation ID 'invalid_id' not found in the database."))
def test_chatbot_invalid_conversation_id(mock_continue_conversation):
    response = client.post("/kopi-chatbot", json={"conversation_id": "invalid_id", "message": "Hello"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Conversation ID 'invalid_id' not found in the database."}

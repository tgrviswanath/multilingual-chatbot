from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.service import chat

router = APIRouter(prefix="/api/v1/nlp", tags=["chatbot"])


class ChatInput(BaseModel):
    message: str
    translate_response: bool = True


@router.post("/chat")
def chat_endpoint(body: ChatInput):
    if not body.message.strip():
        raise HTTPException(status_code=400, detail="message cannot be empty")
    try:
        return chat(body.message, body.translate_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.service import chat

router = APIRouter(prefix="/api/v1/nlp", tags=["chatbot"])


class ChatInput(BaseModel):
    message: str
    translate_response: bool = True


@router.post("/chat")
async def chat_endpoint(body: ChatInput):
    if not body.message.strip():
        raise HTTPException(status_code=400, detail="message cannot be empty")
    try:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, chat, body.message, body.translate_response)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

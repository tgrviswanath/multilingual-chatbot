from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.service import chat
import httpx

router = APIRouter(prefix="/api/v1", tags=["chatbot"])


class ChatInput(BaseModel):
    message: str
    translate_response: bool = True


def _handle(e: Exception):
    if isinstance(e, httpx.ConnectError):
        raise HTTPException(status_code=503, detail="NLP service unavailable")
    if isinstance(e, httpx.HTTPStatusError):
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def chat_endpoint(body: ChatInput):
    try:
        return await chat(body.message, body.translate_response)
    except Exception as e:
        _handle(e)

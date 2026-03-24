import httpx
from app.core.config import settings

NLP_URL = settings.NLP_SERVICE_URL


async def chat(message: str, translate_response: bool = True) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{NLP_URL}/api/v1/nlp/chat",
            json={"message": message, "translate_response": translate_response},
            timeout=60.0,
        )
        r.raise_for_status()
        return r.json()

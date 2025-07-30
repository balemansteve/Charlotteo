"""
Modulo que maneja el endpoint POST /prompt.
Punto de entrada general a la FastAPI.
Envía mensaje del usuario a OpenAI.
"""

from fastapi import APIRouter
from app.schemas.prompt import PromptRequest
from app.services.openai_client import OpenAIClient

router = APIRouter()

llm_client = OpenAIClient()

@router.post("/")
def handle_prompt(request: PromptRequest):
    # Enviar mensaje del usuario a OpenAI y obtener la respuesta
    response = llm_client.send_prompt(request.message)
    return {
        "response": response
    }

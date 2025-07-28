"""
Modulo que maneja el endpoint POST /prompt.
Punto de entrada general a la FastAPI.
Envía mensaje del usuario a OpenAI.
"""

from fastapi import APIRouter
from app.schemas.prompt import PromptRequest
from app.services.openai_client import OpenAIClient
from app.utils.severity import calcular_severidad
import json

router = APIRouter()

llm_client = OpenAIClient()

@router.post("/")
def handle_prompt(request: PromptRequest):
    # Enviar mensaje del usuario a OpenAI y obtener la respuesta
    response = llm_client.send_prompt(request.message)

    # Intentar calcular severidad si es posible
    severity = "info"
    try:
        # Si la respuesta es string y parece JSON, intenta convertirla en dict
        response_data = json.loads(response) if isinstance(response, str) else response
        metric_key = response_data.get("metric_key")
        value = response_data.get("value")
        # Intenta extraer metric_key y value de la respuesta técnica
        if metric_key and value is not None:
            severity = calcular_severidad(metric_key, value)
    # Si algo falla, ignora el error y deja severity en "info"
    except Exception:
        pass

    return {
        "response": response,
        "severity": severity
    }

"""
Modulo que maneja el endpoint POST /prompt.
Punto de entrada general a la FastAPI.
Envía mensaje del usuario a OpenAI.
"""

from fastapi import APIRouter
from app.schemas.prompt import PromptRequest
from app.services.prompt_builder import PromptBuilder
from app.services.openai_client import OpenAIClient
# from app.services.vmware_client import VmwareClient
from app.services.vmware_client_mock import VmwareClient
from app.utils.severity import calcular_severidad


router = APIRouter()

prompt_builder = PromptBuilder()
llm_client = OpenAIClient()
vmware_client = VmwareClient()

@router.post("/")
def handle_prompt(request: PromptRequest):
    # Construir el prompt a partir del mensaje del usuario
    prompt = prompt_builder.build_prompt(request.message)

    # Enviar a OpenAI y obtener la respuesta (texto o diccionario)
    response = llm_client.send_prompt(prompt)

    # Si la respuesta es diccionario, hay una acción a ejecutar
    if isinstance(response, dict):
        action = response.get("action")
        vm_name = response.get("vm_name")
        # Ejecutar la acción en VMware
        vmware_result = vmware_client.execute_metric_action(vm_name, action)
        user_friendly_response = llm_client.summarize_response(vmware_result)
         # Obtén metric_key y valor
        metric_key = None
        valor = None
        if isinstance(vmware_result, dict):
            metric_key = vmware_result.get("metric_key")
            valor = vmware_result.get("value")
        # Calcula la severidad solo si hay datos válidos
        severity = calcular_severidad(metric_key, valor) if (metric_key and valor is not None) else "info"
        return {
            "response": user_friendly_response,
            "severity": severity
        }
    # Si la respuesta es texto plano, devolver directo
    return {"response": response, "severity": "info"}

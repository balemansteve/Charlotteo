"""
Modulo que maneja el endpoint POST /prompt.
Punto de entrada general a la FastAPI.
Envía mensaje del usuario a OpenAI.
"""

from fastapi import APIRouter
from app.schemas.prompt import PromptRequest
from app.services.prompt_builder import PromptBuilder
from app.services.openai_client import OpenAIClient
from app.services.vmware_client import VmwareClient

router = APIRouter()

prompt_builder = PromptBuilder()
llm_client = OpenAIClient()
vmware_client = VmwareClient()

@router.post("/")
def handle_prompt(request: PromptRequest):
    # Construir el prompt
    prompt = prompt_builder.build_prompt(request.message)

    # Enviar a OpenAI
    response = llm_client.send_prompt(prompt)

    # Si la respuesta es diccionario, hay una acción a ejecutar
    if isinstance(response, dict):
        #  script = response.get("script")  / Si es necesario script por linea de comandos
        action = response.get("action")
        vm_name = response.get("vm_name")

        vmware_result = vmware_client.execute_script(vm_name, action)
        final_response = llm_client.summarize_response(vmware_result)
        return {"response": final_response}
    
    # Si la respuesta es texto plano, devolver directo
    return {"response": response}

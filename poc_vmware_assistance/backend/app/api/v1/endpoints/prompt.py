"""
Modulo que maneja el endpoint POST /prompt.
Punto de entrada general a la FastAPI.
Envía mensaje del usuario a Bedrock.
"""

from fastapi import APIRouter
from app.schemas.prompt import PromptRequest
from app.services.prompt_builder import PromtBuilder
from poc_vmware_assistance.backend.app.services.openai_client import BedrockClient
from app.services.vmware_client import VmwareClient

router = APIRouter()

prompt_builder = PromptBuilder()
bedrock_client = BedrockClient()
vmware_client = VmwareClient()

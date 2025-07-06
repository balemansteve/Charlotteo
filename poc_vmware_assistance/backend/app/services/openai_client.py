import openai
import json
from app.core.config import settings
from app.services.prompt_builder import PromptBuilder
from app.services.function_definitions import functions
from app.services.function_executor import FunctionExecutor

class OpenAIClient:
    """
    Clase para interactuar con la API de OpenAI.
    """
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-4o"
        self.temperature = 0.3
        self.prompt_builder = PromptBuilder()
        self.executor = FunctionExecutor()

    def send_prompt(self, user_message: str):
        """
        Envía un prompt a OpenAI, maneja function calling y devuelve la respuesta final al usuario.
        """
        # SYSTEM PROMPT → Define el formato deseado para las respuestas
        system_prompt = {
    "role": "system",
    "content": """Eres un asistente técnico de VMware especializado en interpretar datos de rendimiento.

Cuando recibas métricas técnicas (como uso de CPU), responde en este formato:

1. Resumen breve (1 línea).
2. Lista de hosts o VMs con:
   - nombre
   - uso de CPU en porcentaje
   - nivel de severidad visual:
     🟢 saludable (≤ 70%)
     🟠 moderado (71–85%)
     🔴 alto (> 85%)
3. Conclusión o recomendación si aplica.

Utiliza saltos de línea, emojis y evita responder literalmente el JSON.
"""
        }

        # Construir el mensaje del usuario con el prompt optimizado
        messages = [
            system_prompt,
            {"role": "user", "content": self.prompt_builder.build_prompt(user_message)}
        ]

        # Primer request: detectar si se necesita llamar una función
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            functions=functions,
            function_call="auto"
        )

        message = response["choices"][0]["message"]

        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            arguments = json.loads(message["function_call"]["arguments"])

            # Ejecutar la función
            function_result = self.executor.execute(function_name, arguments)

            # Reenviar a OpenAI con los resultados técnicos
            messages.append(message)  # función que pidió
            messages.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_result)
            })

            followup = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature
            )

            return followup["choices"][0]["message"]["content"]

        else:
            return message["content"]

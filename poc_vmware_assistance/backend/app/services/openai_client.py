"""
Módulo que maneja la lógica para enviar mensajes a OpenAI
y recibir respuestas.
"""

import openai
import os
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
        """
        Inicializa el cliente de OpenAI con la clave de API.
        """
        openai.api_key = settings.OPENAI_API_KEY
        self.model = "gpt-4o"
        self.temperature = 0.5
        self.prompt_builder = PromptBuilder()
        self.executor = FunctionExecutor()

    def send_prompt(self, user_message: str):
        """
        Envía un prompt a la API de OpenAI y devuelve la respuesta.

        :param prompt: El texto del prompt a enviar.
        :return: Respuesta de la API de OpenAI.
        """
        messages = [{"role": "user", "content": self.prompt_builder.build_prompt(user_message)}]

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

            # Ejecutar función y enviar resultado como nuevo mensaje
            function_result = self.executor.execute(function_name, arguments)

            # Ahora reenviar a OpenAI con el resultado técnico
            messages.append(message)
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


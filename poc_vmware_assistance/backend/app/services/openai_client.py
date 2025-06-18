"""
Módulo que maneja la lógica para enviar mensajes a OpenAI
y recibir respuestas.
"""

import openai
import os
import json
from app.core.config import settings

class OpenAIClient:
    """
    Clase para interactuar con la API de OpenAI.
    """

    def __init__(self):
        """
        Inicializa el cliente de OpenAI con la clave de API.
        """
        self.api_key = settings.OPENAI_API_KEY
        # openai.api_key = self.api_key // SDK viejo
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"  # Versión del modelo usado

    def send_prompt(self, prompt: str):
        """
        Envía un prompt a la API de OpenAI y devuelve la respuesta.

        :param prompt: El texto del prompt a enviar.
        :return: Respuesta de la API de OpenAI.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Eres un asistente de VMware que ayuda a sus usuarios a diagnosticar problemas, encontrar soluciones y dar recomendaciones."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        result = response.choices[0].message.content

        try:
            import json
            return json.loads(result)  # Intentar decodificar como JSON
        except json.JSONDecodeError:
            # Si no se puede decodificar como JSON, devolver el texto plano
            return result

    def summarize_response(self, technical_output: str):
        """
        Resume la respuesta técnica para que sea más comprensible.

        :param technical_output: La salida técnica a resumir.
        :return: Resumen de la salida técnica.
        """
        return f"technical result interpreted: {technical_output}"

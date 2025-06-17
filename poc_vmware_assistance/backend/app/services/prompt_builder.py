"""
Módulo que construye el prompt que será enviado al agente de IA.
"""

class PromptBuilder:
    def __init__(self):
        self.instructions = (
            "Eres un asistente de diagnóstico de VMware.\n"
            "Al recibir una pregunta de un usuario, determina si requiere una acción de VMware o si se puede responder directamente.\n"
            "Si se requiere una acción, devuelve SOLO un JSON válido con las claves: 'action' y 'vm_name'.\n"
            "Por ejemplo: {\"action\": \"get_cpu_metrics\", \"vm_name\": \"SRV-WEB01\"}\n"
            "Si no se requiere ninguna acción, devuelve SOLO una respuesta en texto sin formato.\n"
            "No des instrucciones adicionales ni explicaciones, solo responde a la pregunta del usuario.\n"
        )

    def build_prompt(self, user_message: str) -> str:
        return f"{self.instructions}\n\nUser question: {user_message}"

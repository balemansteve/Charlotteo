"""
Módulo que construye el prompt que será enviado al agente de IA.
"""

class PromptBuilder:
    def __init__(self):
        self.instructions = (
            "You are a VMware diagnostic assistant.\n"
            "When receiving a user question, determine whether it requires a VMware action or can be answered directly.\n"
            "If an action is needed, return ONLY a valid JSON with keys: 'action' and 'vm_name'.\n"
            "For example: {\"action\": \"get_cpu_metrics\", \"vm_name\": \"SRV-WEB01\"}\n"
            "If no action is needed, return ONLY a plain text answer."
        )

    def build_prompt(self, user_message: str) -> str:
        return f"{self.instructions}\n\nUser question: {user_message}"

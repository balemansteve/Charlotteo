"""
Módulo que define la forma del JSON que recibe POST /prompt.
"""

from pydantic import BaseModel

class PromptRequest(BaseModel):
    message: str

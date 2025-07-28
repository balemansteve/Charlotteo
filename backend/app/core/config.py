"""
Modulo encargado de leer variables de entorno, tokens,
regiones AWS, etc.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ARIA_API_URL = os.getenv("ARIA_API_URL")
    ARIA_API_USER = os.getenv("ARIA_API_USER")
    ARIA_API_PASSWORD = os.getenv("ARIA_API_PASSWORD")


settings = Config()

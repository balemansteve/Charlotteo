"""
Módulo del punto de entrada de la app.
Crea la instancia de FastAPI y se incluye el router.
"""

from fastapi import FastAPI
from app.api.v1.endpoints import prompt
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="VMware Assistance Poc",
    description="Backend para consultas y diagnósticos de VMware con IA",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt.router, prefix="/api/v1/prompt", tags=["Prompt"])

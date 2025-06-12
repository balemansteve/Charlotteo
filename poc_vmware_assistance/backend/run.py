"""
Módulo del punto de entrada de la app.
Crea la instancia de FastAPI y se incluye el router.
"""

from fastapi import FastAPI
from app.api.v1.endpoints import prompt, metrics

app = FastAPI(
    title="VMware Assistance Poc",
    version="1.0"
)

app.include_router(prompt.router, prefix="/api/v1/prompt", tags=["Prompt"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["Metrics"])

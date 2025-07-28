"""
Modulo que maneja el endpoint GET /metrics.
Mock de prueba temporal.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/{vm_name}")
def get_cpu_metrics(vm_name: str):
    """
    Obtiene las métricas de CPU de una máquina virtual específica.
    
    Args:
        vm_name (str): Nombre de la máquina virtual.
    
    Returns:
        dict: Métricas de CPU de la máquina virtual.
    """
    # Este mock simula la respuesta de Aria Operations API
    return {
        "metric_key": "cpu|usage_average",
        "value": 92.3
    }

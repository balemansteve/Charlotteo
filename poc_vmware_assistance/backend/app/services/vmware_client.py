"""
Módulo que maneja la lógica para ejecutar scripts en vSphere.
Enviar la ejecución al endpoint que corresponda.
"""

import requests

class VmwareClient:
    def execute_script(self, vm_name: str, action: str):
        if action == "get_cpu_metrics":
            url == f"http://localhost:8000/api/v1/metrics/{vm_name}"
            response = requests.get(url)
            return response.json()
        return {"message": "Action not implemented"}

"""
Módulo que maneja la lógica para ejecutar scripts en vSphere.
Enviar la ejecución al endpoint que corresponda.
"""

# import requests

# class VmwareClient:
#     def execute_metric_action(self, vm_name: str, action: str):
#         if action == "get_cpu_metrics":
#             url == f"http://localhost:8000/api/v1/metrics/{vm_name}"
#             response = requests.get(url)
#             return response.json()
#         return {"message": "Action not implemented"}


import os
import requests
from dotenv import load_dotenv

class VmwareClient:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("ARIA_BASE_URL")
        self.username = os.getenv("ARIA_USERNAME")
        self.password = os.getenv("ARIA_PASSWORD")
        self.token = None

    def authenticate(self):
        """
        Obtiene un token de autenticación usando usuario y contraseña.
        """
        url = f"{self.base_url}/auth/token/acquire"
        response = requests.post(url, auth=(self.username, self.password), verify=False)
        if response.status_code == 200:
            self.token = response.json()['token']
            print("[VmwareClient] Token obtenido correctamente.")
        else:
            raise Exception(f"[VmwareClient] Error autenticando: {response.status_code} {response.text}")

    def get_headers(self):
        if not self.token:
            self.authenticate()
        return {"Authorization": f"Bearer {self.token}"}

    def get_resource_id(self, resource_name):
        """
        Busca el resourceId de una VM o cluster por nombre.
        """
        url = f"{self.base_url}/resources"
        params = {"name": resource_name}
        headers = self.get_headers()
        response = requests.get(url, headers=headers, params=params, verify=False)
        data = response.json()
        if data.get("resourceList"):
            return data["resourceList"][0]["identifier"]
        else:
            print(f"[VmwareClient] Recurso '{resource_name}' no encontrado.")
            return None

    def get_metric(self, resource_id, metric_key):
        """
        Obtiene la métrica deseada de un recurso.
        """
        url = f"{self.base_url}/resources/{resource_id}/stats/latest"
        params = {"statKey": metric_key}
        headers = self.get_headers()
        response = requests.get(url, headers=headers, params=params, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[VmwareClient] Error consultando la métrica: {response.status_code} {response.text}")
            return None

    def execute_metric_action(self, resource_name, action):
        """
        Mapea la acción a una métrica y devuelve el valor consultado.
        """
        action_map = {
            "get_cpu_metrics": "cpu|usage_average",
            "get_memory_metrics": "mem|usage_average",
            "get_network_traffic": "net|usage_average"
        }
        if action not in action_map:
            print(f"[VmwareClient] Acción '{action}' no soportada.")
            return None

        metric_key = action_map[action]
        resource_id = self.get_resource_id(resource_name)
        if not resource_id:
            return None
        return self.get_metric(resource_id, metric_key)

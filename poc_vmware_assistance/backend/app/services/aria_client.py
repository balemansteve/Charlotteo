"""
Módulo que define la clase AriaClient, encargada
de interactuar con la API de Aria Operations.
"""

import requests
from app.core.config import settings

class AriaClient:
    """
    Clase para interactuar con la API de Aria Operations.
    """
    def __init__(self):
        self.base_url = settings.ARIA_API_URL
        self.session = requests.Session()
        self.session.auth = (settings.ARIA_API_USER, settings.ARIA_API_PASSWORD)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def get_top_vms_by_metric(self, metric: str, limit: int, time_range: str = "last_1h"):
        # TODO: Implementar la lógica para consultar la API de Aria Operations (o un mock)
        # y devolver las VMs con mayor valor en una métrica específica dentro de un rango de tiempo
        return {
            "status": "success",
            "data": f"Top {limit} VMs by {metric} in {time_range}"
        }

    def get_vms_with_metric_threshold(self, metric: str, operator: str, value: float, time_range: str = "last_1h"):
        """
        Consulta real a la API de Aria Operations para obtener métricas de VMs y filtrar por umbral.
        """
        # Primero obtener todos los resource IDs de VMs con la funcion auxiliar get_vm_resource_ids
        vms = self.get_vm_resource_ids()
        if isinstance(vms, dict) and vms.get("status") == "error":
            return vms  # si falló, devolvemos el error directamente

        vm_ids = [vm["id"] for vm in vms]

        url = f"{self.base_url}/suite-api/api/resources/stats/query"

        # Mapear tiempo legible a formato Aria (esto puede ajustarse)
        time_range_map = {
            "last_1h": "-60min",
            "last_3d": "-3d"
        }
        start_time = time_range_map.get(time_range, "-60min")

        # Segundo construir el payload con resource IDs y stat keys
        payload = {
            "resourceIds": vm_ids,
            "statKey": [metric],
            "startTime": start_time,
            "rollUpType": "AVG",
            "intervalType": "MINUTES",
            "maxSamples": 1
        }

        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            result = response.json()

            # Tercero filtrar las VMs según el operador y valor
            matching_vms = []

            for stat_entry in result.get("values", []):
                resource_id = stat_entry.get("resourceId")
                stat_values = stat_entry.get("stat-list", {}).get("stat", [])

                for stat in stat_values:
                    samples = stat.get("data", [])
                    if samples:
                        metric_value = samples[0]
                        if self._compare(metric_value, operator, value):
                            # Buscar nombre legible por ID
                            vm_name = next((vm["name"] for vm in vms if vm["id"] == resource_id), resource_id)
                            matching_vms.append({
                                "name": vm_name,
                                "value": metric_value
                            })

            return {
                "status": "success",
                "filtered_vms": matching_vms
            }

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Aria API error: {str(e)}"
            }

    def get_vms_with_snapshots_older_than(self, days: int):
        # TODO: Implementar la lógica para obtener las VMs que tengan snapshots activos 
        # más antiguos que una cantidad específica de días
        return {
            "status": "success",
            "data": f"VMs with snapshots older than {days} days"
        }

    def get_idle_vms(self, cpu_threshold: float = 20, memory_threshold: float = 20, duration_days: int = 7):
        # TODO: Implementar la lógica para identificar VMs inactivas,
        # es decir, con bajo uso de CPU y memoria durante varios días consecutivos
        return {
            "status": "success",
            "data": f"VMs with CPU < {cpu_threshold}% and RAM < {memory_threshold}% over {duration_days} days"
        }

    def get_host_metric_info(self, metric: str, operator: str = None, value: float = None, time_range: str = "last_1h"):
        # TODO: Implementar la lógica para obtener información de métricas de hosts,
        # opcionalmente filtrando por operador lógico, valor y rango de tiempo
        return {
            "status": "success",
            "data": f"Hosts with {metric} metric filtered by {operator} {value} in {time_range}"
        }

    #  METODOS AUXILIARES
    def get_vm_resource_ids(self):
        """
        Consulta la API de Aria Operations para obtener los resource IDs de todas las VMs.
        """
        url = f"{self.base_url}/suite-api/api/resources"

        # Filtros para obtener solo recursos del tipo VirtualMachine
        params = {
            "resourceKind": "VirtualMachine"
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            resources = response.json().get("resourceList", [])

            # Extraemos ID y nombre de cada VM
            vm_resources = [
                {
                    "id": res.get("identifier"),
                    "name": res.get("resourceKey", {}).get("name")
                }
                for res in resources
                if res.get("resourceKey", {}).get("name") is not None
            ]

            return vm_resources

        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Error getting VM resource IDs: {str(e)}"
            }

    def _compare(self, a: float, operator: str, b: float) -> bool:
        if operator == ">": return a > b
        if operator == "<": return a < b
        if operator == ">=": return a >= b
        if operator == "<=": return a <= b
        return False

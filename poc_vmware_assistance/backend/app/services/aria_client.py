"""
Módulo que define la clase AriaClient, encargada
de interactuar con la API de Aria Operations y 
consumir sus endpoints.
"""

import requests
import time
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
        """
        Devuelve las N VMs con mayor valor de una métrica específica en un rango de tiempo.
        """
        resource_ids = self.get_vm_resource_ids()
        if not resource_ids:
            return {"status": "error", "message": "No se pudieron obtener resourceIds de las VMs."}

        url = f"{self.base_url}/suite-api/api/resources/stats/latest"

        payload = {
            "statKeys": [metric],
            "resourceId": resource_ids
        }

        try:
            response = self.session.post(url, json=payload, verify=False)
            response.raise_for_status()
            data = response.json()

            vm_metrics = []
            for stat in data.get("values", []):
                resource_id = stat.get("resourceId")
                stat_list = stat.get("stat-list", {}).get("stat", [])
                if stat_list:
                    value = stat_list[0].get("data", [0])[0]
                    name = self.get_vm_name_by_id(resource_id)
                    vm_metrics.append({"vm_name": name, "value": value})

            vm_metrics_sorted = sorted(vm_metrics, key=lambda x: x["value"], reverse=True)[:limit]

            return {"status": "success", "data": vm_metrics_sorted}

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Aria API error: {str(e)}"}

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Aria API error: {str(e)}"}

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
            response = self.session.post(url, json=payload, verify=False)
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
        """
        Devuelve las VMs que tienen snapshots activos más antiguos que una cantidad específica de días.
        Aún no se puede implementar porque no tenemos autorización para acceder a los endpoints de snapshots.
        """
        # TODO: Implementar la lógica para obtener las VMs que tengan snapshots activos 
        # más antiguos que una cantidad específica de días
        return {
            "status": "success",
            "data": f"VMs with snapshots older than {days} days"
        }

    def get_idle_vms(self, cpu_threshold: float = 20, memory_threshold: float = 20, duration_days: int = 7):
        """
        Devuelve VMs con bajo uso de CPU y memoria sostenido durante una cantidad de días.
        """
        resource_ids = self.get_vm_resource_ids()
        if not resource_ids:
            return {"status": "error", "message": "No se pudieron obtener resourceIds de las VMs."}

        url = f"{self.base_url}/suite-api/api/resources/stats/query"

        # Tiempo en milisegundos desde hace 'n' días hasta ahora
        end_time = int(time.time() * 1000)
        start_time = end_time - (duration_days * 24 * 60 * 60 * 1000)

        payload = {
            "resourceId": resource_ids,
            "statKey": ["cpu|usage_average", "mem|usage_average"],
            "startTime": start_time,
            "endTime": end_time,
            "rollUpType": "AVG",
            "intervalType": "HOURS"
        }

        try:
            response = self.session.post(url, json=payload, verify=False)
            response.raise_for_status()
            data = response.json()

            idle_vms = {}

            for stat_entry in data.get("values", []):
                resource_id = stat_entry.get("resourceId")
                stats = stat_entry.get("stat-list", {}).get("stat", [])
                for stat in stats:
                    key = stat.get("statKey")
                    avg_values = stat.get("data", [])

                    if not avg_values:
                        continue

                    avg_usage = sum(avg_values) / len(avg_values)
                    if resource_id not in idle_vms:
                        idle_vms[resource_id] = {}

                    idle_vms[resource_id][key] = avg_usage

            result = []
            for rid, usage in idle_vms.items():
                cpu_ok = usage.get("cpu|usage_average", 0) < cpu_threshold
                mem_ok = usage.get("mem|usage_average", 0) < memory_threshold
                if cpu_ok and mem_ok:
                    name = self.get_vm_name_by_id(rid)
                    result.append({
                        "vm_name": name,
                        "cpu_avg": usage.get("cpu|usage_average"),
                        "mem_avg": usage.get("mem|usage_average")
                    })

            return {"status": "success", "data": result}

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Aria API error: {str(e)}"}

    def get_host_metric_info(self, metric: str, operator: str = None, value: float = None, time_range: str = "last_1h"):
        """
        Consulta una métrica específica de hosts, con filtros opcionales.
        """
        url = f"{self.base_url}/suite-api/api/resources/stats/query"

        # 1. Obtener resourceIds de hosts
        try:
            response = self.session.get(f"{self.base_url}/suite-api/api/resources?resourceKind=HostSystem", verify=False)
            response.raise_for_status()
            hosts = response.json().get("resourceList", [])
            resource_ids = [host["identifier"] for host in hosts]
        except Exception as e:
            return {"status": "error", "message": f"No se pudieron obtener hosts: {str(e)}"}

        # 2. Calcular rango de tiempo
        time_map = {"last_1h": 1, "last_3d": 3 * 24}
        hours = time_map.get(time_range, 1)
        end_time = int(time.time() * 1000)
        start_time = end_time - (hours * 60 * 60 * 1000)

        payload = {
            "resourceId": resource_ids,
            "statKey": [metric],
            "startTime": start_time,
            "endTime": end_time,
            "rollUpType": "AVG",
            "intervalType": "HOURS"
        }

        try:
            stats_response = self.session.post(url, json=payload, verify=False)
            stats_response.raise_for_status()
            stats_data = stats_response.json()
        except Exception as e:
            return {"status": "error", "message": f"Error al obtener estadísticas: {str(e)}"}

        # 3. Procesar y filtrar
        result = []
        for stat in stats_data.get("values", []):
            rid = stat.get("resourceId")
            values = stat.get("stat-list", {}).get("stat", [])
            if not values:
                continue
            data = values[0].get("data", [])
            if not data:
                continue
            avg = sum(data) / len(data)

            if operator and value is not None:
                if not self._compare(avg, operator, value):
                    continue

            host_name = self.get_vm_name_by_id(rid)
            result.append({
                "host_name": host_name,
                "average": avg,
                "metric": metric
            })

        return {"status": "success", "data": result}

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
            response = self.session.get(url, params=params, verify=False)
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

    def get_vm_name_by_id(self, resource_id: str):
        """
        Devuelve el nombre legible de una VM dado su resourceId.
        """
        url = f"{self.base_url}/suite-api/api/resources/{resource_id}"

        try:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            data = response.json()
            return data.get("resourceKey", {}).get("name", resource_id)

        except requests.exceptions.RequestException:
            return f"VM ({resource_id})"

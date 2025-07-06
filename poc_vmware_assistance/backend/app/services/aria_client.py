"""
Módulo que define la clase AriaClient, encargada
de interactuar con la API de Aria Operations y 
consumir sus endpoints.
"""

import requests
import time
import xml.etree.ElementTree as ET
from app.core.config import settings

class AriaClient:
    """
    Clase para interactuar con la API de Aria Operations.
    """
    def __init__(self):
        self.base_url = settings.ARIA_API_URL
        self.session = requests.Session()
        self.token = None
        self.authenticate()

    def authenticate(self):
        """
        Autenticación por token en Aria Operations.
        """
        auth_url = f"{self.base_url}/suite-api/api/auth/token/acquire"
        payload = {
            "username": settings.ARIA_API_USER,
            "authSource": "LOCAL",
            "password": settings.ARIA_API_PASSWORD
        }

        try:
            response = self.session.post(auth_url, json=payload, verify=False)

            if response.status_code != 200:
                raise RuntimeError(
                    f"Auth failed with status {response.status_code}: {response.text}"
                )

            try:
                root = ET.fromstring(response.text)
                ns = {"ops": "http://webservice.vmware.com/vRealizeOpsMgr/1.0/"}
                self.token = root.findtext("ops:token", namespaces=ns)
            except Exception as e:
                raise RuntimeError(f"Failed to parse XML token: {str(e)}")

            if not self.token:
                raise ValueError("No token received from Aria Operations")

            self.session.headers.update({
                "Authorization": f"vRealizeOpsToken {self.token}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            })

        except requests.RequestException as e:
            raise RuntimeError(f"Authentication request failed: {str(e)}")

    def request(self, method: str, endpoint: str, **kwargs):
        """
        Wrapper para manejar expiración de token. Intenta una vez, y reintenta tras reautenticación si da 401.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, verify=False, **kwargs)
            if response.status_code == 401:
                self.authenticate()
                response = self.session.request(method, url, verify=False, **kwargs)

            response.raise_for_status()
            return response

        except requests.RequestException as e:
            raise RuntimeError(f"Request to {endpoint} failed: {str(e)}")

    def get_top_vms_by_metric(self, metric: str, limit: int, time_range: str = "last_1h"):
        resource_ids = self.get_vm_resource_ids()
        if not resource_ids:
            return {"status": "error", "message": "No se pudieron obtener resourceIds de las VMs."}

        payload = {
            "statKeys": [metric],
            "resourceId": resource_ids
        }

        try:
            response = self.request("POST", "/suite-api/api/resources/stats/latest", json=payload)
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

    def get_vms_with_metric_threshold(self, metric: str, operator: str, value: float, time_range: str = "last_1h"):
        vms = self.get_vm_resource_ids()
        if isinstance(vms, dict) and vms.get("status") == "error":
            return vms

        vm_ids = [vm["id"] for vm in vms]

        time_range_map = {
            "last_1h": "-60min",
            "last_3d": "-3d"
        }
        start_time = time_range_map.get(time_range, "-60min")

        payload = {
            "resourceIds": vm_ids,
            "statKey": [metric],
            "startTime": start_time,
            "rollUpType": "AVG",
            "intervalType": "MINUTES",
            "maxSamples": 1
        }

        try:
            response = self.request("POST", "/suite-api/api/resources/stats/query", json=payload)
            result = response.json()

            matching_vms = []
            for stat_entry in result.get("values", []):
                resource_id = stat_entry.get("resourceId")
                stat_values = stat_entry.get("stat-list", {}).get("stat", [])

                for stat in stat_values:
                    samples = stat.get("data", [])
                    if samples:
                        metric_value = samples[0]
                        if self._compare(metric_value, operator, value):
                            vm_name = next((vm["name"] for vm in vms if vm["id"] == resource_id), resource_id)
                            matching_vms.append({
                                "name": vm_name,
                                "value": metric_value
                            })

            return {"status": "success", "filtered_vms": matching_vms}

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Aria API error: {str(e)}"}

    def get_vms_with_snapshots_older_than(self, days: int):
        try:
            resource_ids = self.get_vm_resource_ids()
            if not resource_ids:
                return {"status": "error", "message": "No VM resource IDs found"}

            payload = {
                "resourceIds": resource_ids,
                "propertyKeys": ["snapshot|age"]
            }

            response = self.request("POST", "/suite-api/api/resources/properties/latest/query", json=payload)
            data = response.json()

            result = []
            for item in data.get("propertyValues", []):
                resource_id = item["resourceId"]
                properties = item.get("propertyValues", [])
                for prop in properties:
                    if prop["propertyKey"] == "snapshot|age":
                        try:
                            age_days = int(prop["statKey"]["key"] or 0)
                            if age_days > days:
                                name = self.get_vm_name_by_id(resource_id)
                                result.append(name or resource_id)
                        except (KeyError, ValueError, TypeError):
                            continue

            return {"status": "success", "data": result}

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Aria API error: {str(e)}"}

    def get_idle_vms(self, cpu_threshold: float = 20, memory_threshold: float = 20, duration_days: int = 7):
        resource_ids = self.get_vm_resource_ids()
        if not resource_ids:
            return {"status": "error", "message": "No se pudieron obtener resourceIds de las VMs."}

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
            response = self.request("POST", "/suite-api/api/resources/stats/query", json=payload)
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
        try:
            response = self.request("GET", "/suite-api/api/resources", params={"resourceKind": "HostSystem"})
            hosts = response.json().get("resourceList", [])
            resource_ids = [host["identifier"] for host in hosts]
        except Exception as e:
            return {"status": "error", "message": f"No se pudieron obtener hosts: {str(e)}"}

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
            stats_response = self.request("POST", "/suite-api/api/resources/stats/query", json=payload)
            stats_data = stats_response.json()
        except Exception as e:
            return {"status": "error", "message": f"Error al obtener estadísticas: {str(e)}"}

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

    def get_vm_resource_ids(self):
        params = {"resourceKind": "VirtualMachine"}
        try:
            response = self.request("GET", "/suite-api/api/resources", params=params)
            resources = response.json().get("resourceList", [])

            vm_resources = [
                {"id": res.get("identifier"), "name": res.get("resourceKey", {}).get("name")}
                for res in resources
                if res.get("resourceKey", {}).get("name") is not None
            ]

            return vm_resources

        except requests.exceptions.RequestException as e:
            return {"status": "error", "message": f"Error getting VM resource IDs: {str(e)}"}

    def _compare(self, a: float, operator: str, b: float) -> bool:
        if operator == ">": return a > b
        if operator == "<": return a < b
        if operator == ">=": return a >= b
        if operator == "<=": return a <= b
        return False

    def get_vm_name_by_id(self, resource_id: str):
        try:
            response = self.request("GET", f"/suite-api/api/resources/{resource_id}")
            data = response.json()
            return data.get("resourceKey", {}).get("name", resource_id)
        except requests.exceptions.RequestException:
            return f"VM ({resource_id})"

# class VmwareClient:
#     def __init__(self):
#         pass  # No hace falta cargar nada

#     def authenticate(self):
#         print("[Mock] Autenticación simulada (mock)")

#     def get_headers(self):
#         return {}

#     def get_resource_id(self, resource_name):
#         # Simula que siempre encuentra el resource_id "fake-id" para cualquier VM
#         print(f"[Mock] Buscando resource_id para {resource_name}")
#         return "fake-id"

#     def get_metric(self, resource_id, metric_key):
#         # Devuelve un resultado simulado para cualquier métrica
#         print(f"[Mock] Consultando métrica '{metric_key}' para '{resource_id}'")
#         return {"metric_key": metric_key, "value": 92.3, "resource_id": resource_id}

#     def execute_metric_action(self, resource_name, action):
#         print(f"[Mock] Ejecutando acción '{action}' en recurso '{resource_name}'")
#         return self.get_metric("fake-id", action)
import random

class VmwareClient:
    def __init__(self):
        pass  # No hace falta cargar nada

    def execute_metric_action(self, resource_name, action):
        """
        Simula la consulta de una métrica en VMware según la acción.
        Devuelve un diccionario con metric_key y value como espera el backend.
        """
        # Mapea acciones a métricas conocidas
        action_map = {
            "get_cpu_metrics":       "cpu|usage_average",
            "get_memory_metrics":    "mem|usage_average",
            "get_network_traffic":   "net|usage_average",
            "get_disk_usage":        "diskspace|usage",
        }
        metric_key = action_map.get(action, "cpu|usage_average")

        # Simula valores de prueba para cada métrica
        # (puedes personalizar para probar severidad)
        test_values = {
            "cpu|usage_average":       67.5,
            "mem|usage_average":       87.2,
            "net|usage_average":       92.3,
            "diskspace|usage":         54.0,
        }
        value = test_values.get(metric_key, 50.0)

        # Puedes forzar otros valores para probar warning/critical
        # value = random.choice([50.0, 75.0, 92.0])

        return {
            "metric_key": metric_key,
            "value": value
        }

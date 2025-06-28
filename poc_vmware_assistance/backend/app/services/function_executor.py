"""
Módulo que ejecuta funciones específicas basadas en el nombre y los argumentos
recibidos desde OpenAI mediante function calling.
"""

from app.services.aria_client import AriaClient

class FunctionExecutor:
    """
    Clase para ejecutar funciones específicas de Aria Operations según el nombre recibido
    desde el asistente de OpenAI. Actúa como intermediario que llama al método correspondiente
    de AriaClient usando los argumentos proporcionados.
    """

    def __init__(self):
        self.aria_client = AriaClient()

    def execute(self, function_name: str, arguments: dict):
        """
        Ejecuta la función correspondiente según el nombre recibido y los argumentos provistos.
        """
        if function_name == "get_top_vms_by_metric":
            # Llama a la función para obtener las VMs con mayor valor en una métrica
            return self.aria_client.get_top_vms_by_metric(
                metric=arguments["metric"],
                limit=arguments["limit"],
                time_range=arguments.get("time_range", "last_1h")
            )

        elif function_name == "get_vms_with_metric_threshold":
            # Llama a la función para obtener VMs que cumplen con un umbral en una métrica
            return self.aria_client.get_vms_with_metric_threshold(
                metric=arguments["metric"],
                operator=arguments["operator"],
                value=arguments["value"],
                time_range=arguments.get("time_range", "last_1h")
            )

        elif function_name == "get_vms_with_snapshots_older_than":
            # Llama a la función para obtener VMs con snapshots más antiguos que N días
            return self.aria_client.get_vms_with_snapshots_older_than(
                days=arguments["days"]
            )

        elif function_name == "get_idle_vms":
            # Llama a la función para obtener VMs inactivas (bajo uso de CPU y memoria)
            return self.aria_client.get_idle_vms(
                cpu_threshold=arguments.get("cpu_threshold", 20),
                memory_threshold=arguments.get("memory_threshold", 20),
                duration_days=arguments.get("duration_days", 7)
            )

        elif function_name == "get_host_metric_info":
            # Llama a la función para obtener métricas específicas de hosts
            return self.aria_client.get_host_metric_info(
                metric=arguments["metric"],
                operator=arguments.get("operator"),
                value=arguments.get("value"),
                time_range=arguments.get("time_range", "last_1h")
            )

        else:
            # Lanza error si la función no está soportada
            raise ValueError(f"Function '{function_name}' is not supported.")

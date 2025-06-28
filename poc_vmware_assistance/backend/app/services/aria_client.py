class AriaClient:
    """
    Clase para interactuar con la API de Aria Operations.
    """

    def get_top_vms_by_metric(self, metric: str, limit: int, time_range: str = "last_1h"):
        # TODO: Implementar la lógica para consultar la API de Aria Operations (o un mock)
        # y devolver las VMs con mayor valor en una métrica específica dentro de un rango de tiempo
        return {
            "status": "success",
            "data": f"Top {limit} VMs by {metric} in {time_range}"
        }

    def get_vms_with_metric_threshold(self, metric: str, operator: str, value: float, time_range: str = "last_1h"):
        # TODO: Implementar la lógica para filtrar VMs que cumplan una condición (operador y valor) 
        # en una métrica determinada, dentro de un rango de tiempo
        return {
            "status": "success",
            "data": f"VMs with {metric} {operator} {value} in {time_range}"
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

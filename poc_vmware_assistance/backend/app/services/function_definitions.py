functions = [
        {
        "name": "get_top_vms_by_metric",
        "description": "Devuelve las N VMs con el mayor valor de una métrica específica en un rango de tiempo.",
        "parameters": {
            "type": "object",
            "properties": {
                "metric": {
                    "type": "string",
                    "enum": [
                        "cpu_usage", "cpu|usage_average",
                        "memory_usage", "mem|usage_average",
                        "disk_read", "disk|read_average",
                        "network_usage", "net|usage_average",
                        "cpu_ready", "cpu|ready_summation",
                        "memory_active", "mem|active_average"
                    ],
                    "description": "Tipo de métrica a analizar (ej: uso de CPU, memoria, disco o red)."
                },
                "limit": {
                    "type": "integer",
                    "description": "Número de VMs a listar."
                },
                "time_range": {
                    "type": "string",
                    "description": "Rango de tiempo (ej: 'last_1h', 'last_3d')."
                }
            },
            "required": ["metric", "limit"]
        }
    },
    {
        "name": "get_vms_with_metric_threshold",
        "description": "Lista VMs que cumplen una condición con una métrica determinada.",
        "parameters": {
            "type": "object",
            "properties": {
                "metric": {
                    "type": "string",
                    "enum": [
                        "cpu_usage", "cpu|usage_average",
                        "memory_usage", "mem|usage_average",
                        "cpu_ready", "cpu|ready_summation",
                        "memory_active", "mem|active_average",
                        "disk_read", "disk|read_average",
                        "network_usage", "net|usage_average"
                    ],
                    "description": "Métrica a evaluar (ej: uso de CPU, memoria, etc.)."
                },
                "operator": {
                    "type": "string",
                    "enum": [">", "<", ">=", "<="],
                    "description": "Comparador lógico."
                },
                "value": {
                    "type": "number",
                    "description": "Valor umbral para filtrar."
                },
                "time_range": {
                    "type": "string",
                    "description": "Rango de tiempo (opcional)."
                }
            },
            "required": ["metric", "operator", "value"]
        }
    },
    {
        "name": "get_vms_with_snapshots_older_than",
        "description": "Devuelve las VMs con snapshots activos más antiguos que una cantidad de días.",
        "parameters": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "description": "Número de días como umbral para considerar snapshots viejos."
                }
            },
            "required": ["days"]
        }
    },
    {
        "name": "get_idle_vms",
        "description": "Devuelve VMs con bajo uso de CPU y memoria de forma sostenida, candidatas a consolidación.",
        "parameters": {
            "type": "object",
            "properties": {
                "cpu_threshold": {
                    "type": "number",
                    "default": 20,
                    "description": "Umbral máximo de uso de CPU para considerar una VM inactiva."
                },
                "memory_threshold": {
                    "type": "number",
                    "default": 20,
                    "description": "Umbral máximo de uso de memoria para considerar una VM inactiva."
                },
                "duration_days": {
                    "type": "integer",
                    "default": 7,
                    "description": "Cantidad de días a evaluar."
                }
            }
        }
    },
    {
        "name": "get_host_metric_info",
        "description": "Devuelve información sobre métricas específicas de hosts (uso de CPU, RAM, tráfico de red, etc.).",
        "parameters": {
            "type": "object",
            "properties": {
                "metric": {
                    "type": "string",
                    "enum": ["cpu_usage", "memory_usage", "disk_latency", "network_usage", "cpu_ready", "vm_count"],
                    "description": "Métrica del host a analizar."
                },
                "operator": {
                    "type": "string",
                    "enum": [">", "<", ">=", "<="],
                    "description": "Operador de comparación lógica (opcional)."
                },
                "value": {
                    "type": "number",
                    "description": "Valor umbral (opcional)."
                },
                "time_range": {
                    "type": "string",
                    "description": "Rango de tiempo (opcional)."
                }
            },
            "required": ["metric"]
        }
    }
]
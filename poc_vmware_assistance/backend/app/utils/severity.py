# Diccionario con umbrales por métrica
THRESHOLDS = {
    "cpu|usage_average":       {"healthy": (0, 70),  "warning": (71, 85),    "critical": (86, 100)},
    "cpu|demand_average":      {"healthy": (0, 70),  "warning": (71, 85),    "critical": (86, 100)},
    "cpu|ready_summation":     {"healthy": (0, 1000), "warning": (1001, 3000), "critical": (3001, float("inf"))},
    "mem|usage_average":       {"healthy": (0, 70),  "warning": (71, 85),    "critical": (86, 100)},
    "diskspace|usage":         {"healthy": (0, 70),  "warning": (71, 85),    "critical": (86, 100)},
    "disk|read_average":       {"healthy": (0, 50),  "warning": (51, 150),   "critical": (151, float("inf"))},
    "disk|write_average":      {"healthy": (0, 50),  "warning": (51, 150),   "critical": (151, float("inf"))},
    "net|usage_average":       {"healthy": (0, 20),  "warning": (21, 50),    "critical": (51, float("inf"))},
    "net|received_average":    {"healthy": (0, 20),  "warning": (21, 50),    "critical": (51, float("inf"))},
    "net|transmitted_average": {"healthy": (0, 20),  "warning": (21, 50),    "critical": (51, float("inf"))},
    # Agregar más métricas de ser necesario...
}

def calcular_severidad(metric_key, valor):
    """
    Devuelve 'healthy', 'warning' o 'critical' según el valor y los umbrales definidos.
    """
    try:
        thresholds = THRESHOLDS[metric_key]
        if thresholds["healthy"][0] <= valor <= thresholds["healthy"][1]:
            return "healthy"
        elif thresholds["warning"][0] <= valor <= thresholds["warning"][1]:
            return "warning"
        elif thresholds["critical"][0] <= valor:
            return "critical"
    except Exception:
        # Si la métrica no está definida, devuelve 'info'
        return "info"
    return "info"

def get_severity_emoji(value: float) -> str:
    """
    Devuelve un emoji de severidad según el valor numérico.
    Umbrales usados (por ahora comunes para CPU, RAM, etc.):
    0 a 70   🟢 saludable
    71 a 85  🟡 advertencia
    86+    🔴 crítico
    """
    if value <= 70:
        return "🟢"
    elif value <= 85:
        return "🟡"
    else:
        return "🔴"

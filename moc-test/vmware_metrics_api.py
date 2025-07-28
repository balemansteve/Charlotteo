import json
import random
from typing import Dict, List

def generate_random_metrics(metrics_template: List[Dict]) -> List[Dict]:
    updated_metrics = []
    for metric in metrics_template:
        random_value = random.randint(0, 100)
        updated_metric = metric.copy()
        updated_metric["current_value"] = f"{random_value}%"
        if random_value <= 70:
            status = "healthy"
        elif random_value <= 85:
            status = "warning"
        else:
            status = "critical"
        updated_metric["status"] = status
        updated_metrics.append(updated_metric)
    return updated_metrics

def get_vmware_metrics() -> str:
    with open('metrics.py', 'r') as f:
        metrics_template = json.load(f)
    updated_metrics = generate_random_metrics(metrics_template)
    return json.dumps(updated_metrics, indent=2)

if __name__ == "__main__":
    print(get_vmware_metrics()) 
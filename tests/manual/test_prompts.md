## Prompts de prueba por función de 'AriaClient'

🔹 1. get_top_vms_by_metric
¿Cuáles son las 3 VMs con mayor uso de CPU?
→ metric="cpu|usage_average", limit=3

🔹 2. get_vms_with_metric_threshold
¿Hay VMs que tengan más de 85% de uso de memoria?
→ metric="mem|usage_average", operator=">", value=85

🔹 3. get_vms_with_snapshots_older_than
¿Existen VMs con snapshots más antiguos que 7 días?
→ days=7

🔹 4. get_idle_vms
¿Hay VMs inactivas con poco uso de CPU y memoria?
→ cpu_threshold=20, memory_threshold=20, duration_days=7

🔹 5. get_host_metric_info
¿Hay hosts con más del 80% de uso de CPU en la última hora?
→ metric="cpu|usage_average", operator=">", value=80, time_range="last_1h"
# Documentación de Pruebas del MVP - VMware Assistant

## Descripción General

**Nombre del Proyecto:** VMware Assistant  
**Fecha de Pruebas:** 6 de julio de 2025  
**Autor:** Bryan Alemán  
**Versión:** 1.0 (MVP)

**Objetivo de la Prueba:**  
Validar el comportamiento de los 5 métodos principales del backend que consultan métricas de VMware Aria Operations según los prompts en lenguaje natural.  
Todas las pruebas consumen el unico endpoint de entrada al chatbot: **POST** `/api/v1/prompt/`

---

## 🧪 Pruebas de métodos para consumir Aria Operations API

| **Método** | Funcionalidad | Resultado del test |
|--------------|-------------------------|--------------------|
| **`get_top_vms_by_metric`** | Retorna las VMs con mayor valor en una métrica específica (CPU, RAM, etc.) en un rango de tiempo. | EN DESARROLLO |
| **`get_vms_with_metric_threshold`** | Devuelve VMs que superan o están por debajo de un umbral para una métrica dada (ej: CPU > 80%). | PASS |
| **`get_vms_with_snapshots_older_than`** | Lista las VMs que tienen snapshots más antiguos que una cantidad de días definida. | EN DESARROLLO |
| **`get_idle_vms`** | Identifica máquinas virtuales inactivas (sin actividad significativa de CPU y RAM). | EN DESARROLLO |
| **`get_host_metric_info`** | Obtiene una métrica agregada (ej: promedio de CPU) para todos los hosts del sistema. | PASS |

---

## Prueba 1: get_top_vms_by_metric

| **Endpoint** | `/api/v1/prompt/` |
|--------------|-------------------|
| **Descripción** | Devuelve las VMs con mayor uso de una métrica dada. |
| **Tipo de Petición** | POST |

- **Prompt de Entrada:**  
  `"¿Cuáles son las 3 VMs con mayor uso de CPU?"`

- **Ejemplo curl:**
```bash
curl -X POST http://localhost:8000/api/v1/prompt/ \
-H "Content-Type: application/json" \
-d '{"prompt": "¿Cuáles son las 3 VMs con mayor uso de CPU?"}'
```

- **Resultado esperado:**  
  Código de estado: `200 OK`  
  **Resultado actual:** respuesta técnica sin formatear  
  **Estado:** EN DESARROLLO

---

## Prueba 2: get_vms_with_metric_threshold 

| **Endpoint** | `/api/v1/prompt/` |
|--------------|-------------------|
| **Descripción** | Devuelve VMs que superan un umbral definido para una métrica. |
| **Tipo de Petición** | POST |

- **Prompt de Entrada:**  
  `"¿Hay VMs que tengan más de 85% de uso de memoria?"`

- **Ejemplo curl:**
```bash
curl -X POST http://localhost:8000/api/v1/prompt/ \
-H "Content-Type: application/json" \
-d '{"prompt": "¿Hay VMs que tengan más de 85% de uso de memoria?"}'
```

- **Respuesta esperada:**  
```json
{
  "response": "Hay 2 VMs con uso de memoria superior al 85%."
}
```

- **Resultado actual:** PASS  
Código de estado: `200 OK`

---

## Prueba 3: get_vms_with_snapshots_older_than

| **Endpoint** | `/api/v1/prompt/` |
|--------------|-------------------|
| **Descripción** | Retorna VMs con snapshots más antiguos que cierto número de días. |
| **Tipo de Petición** | POST |

- **Prompt:**  
  `"¿Existen VMs con snapshots más antiguos que 7 días?"`

- **Ejemplo curl:**
```bash
curl -X POST http://localhost:8000/api/v1/prompt/ \
-H "Content-Type: application/json" \
-d '{"prompt": "¿Existen VMs con snapshots más antiguos que 7 días?"}'
```

- **Resultado actual:**  
  Respuesta técnica, no entendible para el usuario final  
  **Estado:** EN DESARROLLO

---

## Prueba 4: get_idle_vms

| **Endpoint** | `/api/v1/prompt/` |
|--------------|-------------------|
| **Descripción** | Identifica VMs inactivas por bajo uso de CPU y memoria. |
| **Tipo de Petición** | POST |

- **Prompt:**  
  `"¿Hay VMs inactivas con poco uso de CPU y memoria?"`


- **Ejemplo curl:**
```bash
curl -X POST http://localhost:8000/api/v1/prompt/ \
-H "Content-Type: application/json" \
-d '{"prompt": "¿Hay VMs inactivas con poco uso de CPU y memoria?"}'
```

- **Resultado actual:**  
  Respuesta técnica, no entendible para el usuario final   
  **Estado:** EN DESARROLLO

---

## Prueba 5: get_host_metric_info 

| **Endpoint** | `/api/v1/prompt/` |
|--------------|-------------------|
| **Descripción** | Devuelve una métrica agregada por host con evaluación de severidad. |
| **Tipo de Petición** | POST |

- **Prompt:**  
  `"¿Hay hosts con más del 80% de uso de CPU en la última hora?"`

- **Ejemplo curl:**
```bash
curl -X POST http://localhost:8000/api/v1/prompt/ \
-H "Content-Type: application/json" \
-d '{"prompt": "¿Hay hosts con más del 80% de uso de CPU en la última hora?"}'
```

- **Respuesta esperada:**
```json
{
  "response": "3 hosts tienen uso de CPU mayor al 80% en la última hora. Severidad: warning."
}
```

- **Resultado actual:** PASS  
Código de estado: `200 OK`

---

## Consideraciones Técnicas

- Las pruebas se realizaron en entorno local con las variables del archivo `.env`
- Se utilizó Swagger en `/docs` para validar los formatos y respuestas de los endpoints

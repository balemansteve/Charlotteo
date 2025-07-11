<a id="readme-top"></a>
# Charlotteo (VMware Assistance) - MVP

Este proyecto es un asistente conversacional basado en lenguaje natural que permite consultar métricas de VMware Aria Operations a través de una API RESTful. El chatbot utiliza OpenAI como LLM para interpretar la intención del usuario y consultar métricas a la API de VMware.

## 📝 Notas
- El proyecto requiere credenciales reales para funcionar correctamente.
- El entorno productivo no está disponible públicamente por motivos de seguridad.

---

## 📚 Tabla de Contenidos

- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Requisitos previos](#requisitos-previos)
- [Instalación y configuración](#instalación-y-configuración)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Swagger](#uso-de-swagger)
- [Pruebas](#pruebas)
- [Equipo](#equipo)

---

## Tecnologías utilizadas
### 🖥️ Backend 
- Python 3.10 + (FastAPI, Pydantic)
- OpenAI API (function calling)
- VMware Aria Operations API
### 🌐 Frontend
- HTML y CSS
- JavaScript
- Node.js
### 🧪 Testing
- Pytest
### 🔀 Control de versiones
- Git

---

## Requisitos previos

- Python 3.10+
- Node.js 18+
- pip
- Git

---

## 🔧 Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/balemansteve/vmware-assistant.git
```

### 2. Backend (Python - FastAPI)

#### Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate      # En Linux/Mac
venv\Scripts\activate.bat   # En Windows
```

#### Instalar dependencias

```bash
pip install -r poc_vmware_assistance/backend/requirements.txt
```

#### Crear archivo de entorno

Crear un archivo `.env` en la raíz del backend `poc_vmware_assistance/backend` con las siguientes variables y cambiar por los valores reales:

```dotenv
OPENAI_API_KEY=sk-xxxx
ARIA_USERNAME=usuario
ARIA_PASSWORD=contraseña
ARIA_HOST=https://mi-aria.local
```

---

### 3. Levantar el backend

Ejecutar el script incluido en la raíz del backend:

```bash
cd poc_vmware_assistance/backend
bash start_server.sh
```

Esto iniciará FastAPI en:  
http://localhost:8000

---

### 4. Frontend (Node.js)

```bash
cd poc_vmware_assistance/frontend
npm install
npm run dev
```

Esto levantará el frontend en:  
http://localhost:3000

---

## 📦 Estructura del proyecto

```plaintext
poc_vmware_assistance/
├── backend/               # Código principal del backend
│   ├── app/               
│   ├── start_server.sh    # Script para levantar FastAPI
│   └── .env               # Variables de entorno
├── frontend/              # Código principal del frontend
├── test/                  # Testing
```

---

## 📖 Uso de Swagger

El backend implementado con FastAPI expone una documentación automática de todos los endpoints utilizando **Swagger UI**.

### Acceso

Una vez que el servidor esté corriendo, luego de ejecutar `start_server.sh`, podés acceder a la interfaz de Swagger en:

```
http://localhost:8000/docs
```

### Utilidades

- Probar endpoints manualmente, en este proyecto solo se expone `/api/v1/prompt`
- Visualizar los parámetros esperados por la API
- Ver ejemplos de respuestas estructuradas
- Verificar si los servicios están activos sin usar Postman ni curl
- Para QA y debugging durante el desarrollo

---

## Pruebas

- Pruebas manuales con `curl`.
- Pruebas automatizadas con `pytest`.

---

## 👥 Equipo

- **Bryan Alemán** - Backend Developer
- **Ignacio Devita** - Frontend Developer
- **Marcos Pessano** - Project Manager
<p align="right">(<a href="#readme-top">back to top</a>)</p>

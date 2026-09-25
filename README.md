# PasteleríaUSPG - Motor de Inferencia en CLIPSpy

Sistema Experto basado en reglas para la recomendación y personalización de pasteles, expuesto a través de una API REST utilizando **FastAPI**, **CLIPSpy** y **Python**.

## Tecnologías Utilizadas
- **Python 3.10+**
- **CLIPS** (Motor de inferencia basado en reglas)
- **CLIPSpy** (Integración Python ↔ CLIPS)
- **FastAPI** (Framework web para construir la API REST)
- **Uvicorn** (Servidor web ASGI)
- **Pydantic** (Validación de esquemas y modelos de datos)
- **pytest** (Framework de pruebas automatizadas)

## Estructura del Repositorio
```text
├── backend/
│   ├── pasteleria.clp      # Base de conocimiento (deftemplates y defrules)
│   ├── motor.py            # Clase de inferencia en Python (CLIPSpy)
│   ├── modelos.py          # Modelos de validación Pydantic
│   └── main.py             # Endpoints HTTP con FastAPI
├── tests/
│   ├── test_motor.py       # Pruebas unitarias directas del motor CLIPS
│   └── test_api.py         # Pruebas HTTP automatizadas de los endpoints
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación


## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/powicho/pasteleria-uspg-se.git
cd pasteleria-uspg-se


## Crear y activar un entorno virtual:

# Windows
python -m venv .venv
.venv\Scripts\activate

Nota: Si PowerShell muestra una restricción de ejecución de scripts, ejecuta primero:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass y vuelve a activar el entorno.

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate



## Instalar dependencias:

Asegúrate de tener tu terminal con `(.venv)` activado y ejecuta:

# powershell
pip install -r requirements.txt
uvicorn backend.main:app --reload


## Ejecución de Pruebas Automatizadas
Ejecuta en tu terminal lo siguiente:
pytest -v


## Extras:
FastAPI genera automáticamente la documentación interactiva sin necesidad de crear un frontend adicional. Con el servidor corriendo, abre en tu navegador:
👉 http://127.0.0.1:8000/docs

Desde esta interfaz podrás:
1. Probar el endpoint GET /api/v1/health.
2. Consultar el catálogo con GET /api/v1/ingredientes.
3. Enviar peticiones en tiempo real con POST /api/v1/recomendar y observar cómo razona el motor CLIPSpy devolviendo la recomendación en formato JSON.
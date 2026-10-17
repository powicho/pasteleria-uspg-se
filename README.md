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

## Ejecución del Frontend (Interfaz de Usuario)

Con el backend en ejecución:
1. Dirígete a la carpeta `frontend/Vista 1/`.
2. Abre el archivo **`index.html`** con la extensión **Live Server** de VS Code (o haz doble clic sobre él para abrirlo en el navegador).
3. La interfaz se conectará en tiempo real al backend mostrando el indicador **`● API Online`** en verde.

---

## 🧪 Ejecución de Pruebas Automatizadas
Para verificar que las reglas de inferencia, restricciones y endpoints sigan pasando al 100%:
en bash
pytest -v



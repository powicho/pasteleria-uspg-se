# PasteleríaUSPG - Sistema Experto (Backend, Frontend y Base de Datos)

Sistema Experto basado en reglas para la recomendación y personalización de pasteles, expuesto a través de una API REST (**FastAPI** + **CLIPSpy**) con interfaz gráfica web interactiva (**HTML5 / CSS3 / JavaScript**) y persistencia en **SQL Server**.

---

## 🛠️ Tecnologías Utilizadas
- **CLIPS / CLIPSpy** (Motor de inferencia basado en reglas y agenda con salience)
- **Python 3.10+** (Lenguaje anfitrión y puente)
- **FastAPI & Uvicorn** (API REST y servidor web ASGI)
- **Pydantic** (Validación de esquemas y modelos de datos)
- **HTML5, CSS3 y JavaScript ES6** (Frontend interactivo con visualizador de pastel en tiempo real)
- **Microsoft SQL Server & SSMS 19** (Base de datos relacional para usuarios, catálogo e historial)
- **pytest & httpx** (Suite de pruebas automatizadas)

---

## 📁 Estructura del Repositorio
```text
pasteleria-uspg-se/
├── backend/
│   ├── pasteleria.clp      # Base de conocimiento (deftemplates y defrules de CLIPS)
│   ├── motor.py            # Clase MotorPasteleria en Python (CLIPSpy)
│   ├── modelos.py          # Modelos de validación JSON con Pydantic
│   └── main.py             # Endpoints HTTP con FastAPI
├── db/
│   └── pasteleria_schema.sql  # Script DDL/DML de Microsoft SQL Server
├── frontend/
│   ├── logo.png            # Logotipo oficial de Pastelería USPG
│   ├── Vista 1/            # Recomendación Guiada (Filtro General)
│   │   ├── index.html
│   │   ├── vista1.css
│   │   └── vista1.js
│   ├── Vista 2/            # Personalización Libre Capa por Capa (Con Preview)
│   │   ├── vista2.html
│   │   ├── vista2.css
│   │   └── vista2.js
│   ├── Vista 3/            # Veredicto del Experto (Explicabilidad XAI)
│   │   ├── vista3.html
│   │   ├── vista3.css
│   │   └── vista3.js
│   └── Vista 4/            # Resumen del Pastel y Edición Interactiva
│       ├── vista4.html
│       ├── vista4.css
│       └── vista4.js
├── tests/
│   ├── test_motor.py       # Pruebas unitarias directas del motor CLIPS
│   └── test_api.py         # Pruebas HTTP de los endpoints de la API
├── requirements.txt        # Dependencias del proyecto
└── README.md
```

---

## 🚀 Instalación y Puesta en Marcha

### 1. Activar el entorno virtual e instalar dependencias
```bash
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Iniciar el Backend (API con CLIPS)
```bash
uvicorn backend.main:app --reload
```
* **API Activa en:** `http://127.0.0.1:8000`
* **Swagger UI (/docs):** `http://127.0.0.1:8000/docs`

<<<<<<< HEAD
---

## 🎨 Ejecución del Frontend (Interfaz de Usuario)

Con el backend en ejecución:
1. Dirígete a la carpeta `frontend/Vista 1/`.
2. Abre el archivo **`index.html`** con la extensión **Live Server** de VS Code (o haz doble clic sobre él para abrirlo en el navegador).
3. La interfaz se conectará en tiempo real al backend mostrando el indicador **`● API Online`** en verde.

---

## 🧪 Ejecución de Pruebas Automatizadas
Para verificar que las reglas de inferencia, restricciones y endpoints sigan pasando al 100%:
```bash
pytest -v
```
=======
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
>>>>>>> cd564b6 (feat: sistema de usuarios completo, login en texto plano, historial y recomendacion dinamica por frecuencia)

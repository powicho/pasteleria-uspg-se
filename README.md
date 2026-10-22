# PasteleríaUSPG - Sistema Experto (Backend, Frontend y Base de Datos)

Sistema Experto basado en reglas para la recomendación y personalización de pasteles según restricciones dietéticas, consistencia física y perfiles de sabor. 

El sistema está expuesto a través de una API REST (**FastAPI** + **CLIPSpy**), cuenta con persistencia y memoria de usuario en **Microsoft SQL Server** y una interfaz web interactiva multi-vista (**HTML5 / CSS3 / JavaScript**).

---

## 🛠️ Tecnologías Utilizadas

- **CLIPS / CLIPSpy:** Motor de inferencia basado en reglas (algoritmo Rete), manejo de memoria de trabajo, prioridades con `salience` y guardas de no duplicidad `(not (resultado))`.
- **Python 3.10+:** Lenguaje anfitrión, orquestación del sistema y puente de inferencia.
- **FastAPI & Uvicorn:** Framework web moderno y servidor ASGI de alto rendimiento para exponer la API REST.
- **Pydantic:** Validación estricta de contratos de datos y esquemas JSON.
- **Microsoft SQL Server & SSMS 19:** Persistencia relacional de cuentas de usuario, catálogo de ingredientes e historial de recomendaciones.
- **pyodbc:** Conector de base de datos en Python con detección automática de instancias locales.
- **HTML5, CSS3 y JavaScript ES6:** Frontend interactivo con previsualización del pastel en tiempo real y arquitectura multi-página.
- **pytest & httpx:** Suite de pruebas automatizadas para validación unitaria y pruebas de integración de endpoints.

---

## 📁 Estructura del Repositorio

```text
pasteleria-uspg-se/
├── backend/
│   ├── pasteleria.clp        # Base de conocimiento (deftemplates y defrules de CLIPS)
│   ├── motor.py              # Clase MotorPasteleria en Python (CLIPSpy)
│   ├── database.py           # Conexión y operaciones directas con SQL Server (pyodbc)
│   ├── modelos.py            # Modelos de datos y validación JSON con Pydantic
│   └── main.py               # Endpoints de la API REST (FastAPI)
├── db/
│   └── pasteleria_schema.sql    # Script DDL/DML para crear y poblar la base de datos
├── frontend/
│   ├── logo.png              # Logotipo oficial de Pastelería USPG
│   ├── Login/                # Vista de Acceso y Registro de Usuarios
│   │   ├── login.html
│   │   ├── login.css
│   │   └── login.js
│   ├── Historial/            # Vista de Pasteles Anteriores del Usuario
│   │   ├── historial.html
│   ├── Vista 1/              # Recomendación Guiada (Filtro General y Banner VIP)
│   │   ├── index.html
│   │   ├── vista1.css
│   │   └── vista1.js
│   ├── Vista 2/              # Personalización Libre Capa por Capa (Con Preview en vivo)
│   │   ├── vista2.html
│   │   ├── vista2.css
│   │   └── vista2.js
│   ├── Vista 3/              # Veredicto del Experto (Ficha Técnica y Explicabilidad XAI)
│   │   ├── vista3.html
│   │   ├── vista3.css
│   │   └── vista3.js
│   └── Vista 4/              # Resumen del Pastel y Edición Rápida de Componentes
│       ├── vista4.html
│       ├── vista4.css
│       └── vista4.js
├── tests/
│   ├── test_motor.py         # Pruebas unitarias de las reglas del motor CLIPS
│   └── test_api.py           # Pruebas de integración HTTP de los endpoints
├── requirements.txt          # Librerías y dependencias del entorno
└── README.md                 # Documentación técnica del proyecto

🚀 Instalación y Puesta en Marcha
1. Clonar el repositorio

git clone https://github.com/powicho/pasteleria-uspg-se.git
cd pasteleria-uspg-se

2. Activar el entorno virtual e instalar dependencias
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3. Configuración de la Base de Datos (SQL Server)
Abrir SQL Server Management Studio (SSMS 19).
Abrir y ejecutar el script ubicado en: db/pasteleria_schema.sql.
Esto creará la base de datos PasteleriaUSPG, las tablas Usuarios, CatalogoIngredientes, HistorialRecomendaciones y cargará los registros iniciales.

🖥️ Ejecución del Backend (API REST)
Para levantar el servidor web con recarga automática:
uvicorn backend.main:app --reload
- API activa en: http://127.0.0.1:8000
- Documentación interactiva (Swagger UI): http://127.0.0.1:8000/docs

🎨 Ejecución del Frontend (Interfaz Web)
Con el backend en ejecución:
En VS Code, navega a la carpeta frontend/Login/.
Haz clic derecho sobre login.html y selecciona "Open with Live Server" (o ábrelo directamente en tu navegador).
Flujo de Usuario:
Puedes registrar una cuenta nueva o ingresar con las credenciales demo:
Correo: leavilab@alumno.uspg.edu.gt
Contraseña: hash_pass_123
Al autenticarte, el sistema te redirigirá a la tienda y cargará tu recomendación exclusiva personalizada según tu historial registrado en SQL Server.
Puedes consultar el historial completo de inferencias haciendo clic sobre tu nombre de usuario en el banner o visitando frontend/Historial/historial.html.

🧪 Ejecución de Pruebas Automatizadas
Para validar que las reglas de inferencia, las restricciones dietéticas y los endpoints HTTP funcionen al 100%:

pytest -v





























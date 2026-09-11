# PasteleríaUSPG - Motor de Inferencia en CLIPSpy

Sistema Experto basado en reglas para la recomendación y personalización de pasteles según perfiles de sabor, consistencia física y restricciones alimentarias.

## Tecnologías Utilizadas
- Python 3.10+
- CLIPS (Motor de inferencia basado en reglas)
- clipspy (Librería de enlace Python-CLIPS)
- pytest (Framework de pruebas automatizadas)

## Estructura del Repositorio
```text
pasteleria-uspg-se/
├── backend/
│   ├── pasteleria.clp    # Base de conocimientos (deftemplates y defrules)
│   └── motor.py          # Clase MotorPasteleria en Python
├── tests/
│   └── test_motor.py     # Suite de pruebas unitarias
├── requirements.txt      # Dependencias del proyecto
└── README.md
```
Instalación y Configuración

Clonar el repositorio:
git clone https://github.com/powicho/pasteleria-uspg-se.git
cd pasteleria-uspg-se

## Crear y activar un entorno virtual:

# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

## Instalar dependencias:

pip install -r requirements.txt

## Ejecución de Pruebas Automatizadas

Para validar que los hechos se ingresen correctamente, las reglas se disparen por prioridad y los resultados esperados se generen con éxito:

pytest -v


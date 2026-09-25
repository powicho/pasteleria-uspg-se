from backend.modelos import HealthCheck, ResultadoOutput, SolicitudRecomendacion
from backend.motor import MotorPasteleria
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PasteleríaUSPG - API del Sistema Experto",
    description=(
        "API REST para la recomendación y personalización de pasteles mediante"
        " inferencia basada en reglas (CLIPSpy)."
    ),
    version="1.0.0",
)

# Permitir CORS para futuras integraciones frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia singleton del motor de inferencia
motor = MotorPasteleria()


@app.get("/", tags=["General"])
def inicio():
  return {
      "mensaje": "Bienvenido a la API del Sistema Experto PasteleríaUSPG",
      "docs": "/docs",
      "health": "/api/v1/health",
  }


@app.get("/api/v1/health", response_model=HealthCheck, tags=["Sistema"])
def health_check():
  """Endpoint de monitoreo (Diapositiva 7)."""
  return {
      "estado": "OK",
      "sistema": "PasteleriaUSPG",
      "motor": "CLIPS",
      "integracion": "clipspy",
  }


@app.get("/api/v1/ingredientes", tags=["Catálogo"])
def listar_ingredientes():
  """Retorna el catálogo base de componentes reconocidos por el sistema (Diapositiva 6)."""
  return {
      "bizcochos": [
          {"nombre": "limon", "categoria": "citrico", "densidad": "ligera"},
          {
              "nombre": "chocolate-humedo",
              "categoria": "amargo",
              "densidad": "densa",
          },
          {
              "nombre": "vainilla",
              "categoria": "dulce",
              "densidad": "ligera",
              "opcion_vegetal": True,
          },
      ],
      "rellenos": [
          {"nombre": "maracuya", "categoria": "frutal", "lactosa": False},
          {"nombre": "frutos-rojos", "categoria": "frutal", "lactosa": False},
          {"nombre": "tres-leches", "categoria": "cremoso", "lactosa": True},
          {"nombre": "dulce-de-leche", "categoria": "cremoso", "lactosa": True},
      ],
      "coberturas": [
          {
              "nombre": "merengue-italiano",
              "categoria": "ligera",
              "densidad": "ligera",
              "lactosa": False,
          },
          {
              "nombre": "chantilly",
              "categoria": "ligera",
              "densidad": "ligera",
              "lactosa": True,
          },
          {
              "nombre": "ganache",
              "categoria": "densa",
              "densidad": "densa",
              "lactosa": False,
          },
          {
              "nombre": "crema-vegetal",
              "categoria": "vegetal",
              "densidad": "ligera",
              "lactosa": False,
          },
      ],
  }


@app.post("/api/v1/recomendar", response_model=ResultadoOutput, tags=["Motor"])
def recomendar_pastel(solicitud: SolicitudRecomendacion):
  """Endpoint principal: recibe la solicitud, invoca a CLIPS y devuelve la inferencia (Diapositiva 8)."""
  try:
    resultado = motor.procesar_peticion(solicitud)
    return resultado
  except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=f"Error en la ejecución de la inferencia: {str(e)}",
    )
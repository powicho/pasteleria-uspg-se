from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Importación de la lógica del Sistema Experto (CLIPS)
from backend.motor import MotorPasteleria

# Modelos Pydantic para validar entradas y salidas JSON
from backend.modelos import (
    HealthCheck,
    ResultadoOutput,
    SolicitudRecomendacion,
    UsuarioRegistro,
    UsuarioLogin
)

# Conexión y operaciones directas con Microsoft SQL Server
from backend.database import (
    registrar_usuario,
    autenticar_usuario,
    obtener_recomendacion_personalizada,
    obtener_historial_usuario,
    guardar_historial_recomendacion
)

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="PasteleríaUSPG - API del Sistema Experto",
    description="API REST para la recomendación y personalización de pasteles mediante inferencia basada en reglas (CLIPSpy) y persistencia en SQL Server.",
    version="1.0.0"
)

# Permitir CORS para comunicación fluida con el frontend (Live Server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia singleton del motor de inferencia CLIPS
motor = MotorPasteleria()


# -----------------------------------------------------------------------------
# ENDPOINTS GENERALES Y MONITOREO
# -----------------------------------------------------------------------------
@app.get("/", tags=["General"])
def inicio():
    return {
        "mensaje": "Bienvenido a la API del Sistema Experto PasteleríaUSPG",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.get("/api/v1/health", response_model=HealthCheck, tags=["Sistema"])
def health_check():
    """Endpoint de monitoreo de estado para el indicador del frontend."""
    return {
        "estado": "OK",
        "sistema": "PasteleriaUSPG",
        "motor": "CLIPS",
        "integracion": "clipspy"
    }


@app.get("/api/v1/ingredientes", tags=["Catálogo"])
def listar_ingredientes():
    """Retorna el catálogo base de componentes reconocidos por el sistema."""
    return {
        "bizcochos": [
            {"nombre": "limon", "categoria": "citrico", "densidad": "ligera"},
            {"nombre": "chocolate-humedo", "categoria": "amargo", "densidad": "densa"},
            {"nombre": "vainilla", "categoria": "dulce", "densidad": "ligera", "opcion_vegetal": True},
            {"nombre": "zanahoria", "categoria": "dulce", "densidad": "densa"}
        ],
        "rellenos": [
            {"nombre": "maracuya", "categoria": "frutal", "lactosa": False},
            {"nombre": "frutos-rojos", "categoria": "frutal", "lactosa": False},
            {"nombre": "tres-leches", "categoria": "cremoso", "lactosa": True},
            {"nombre": "dulce-de-leche", "categoria": "cremoso", "lactosa": True}
        ],
        "coberturas": [
            {"nombre": "merengue-italiano", "categoria": "ligera", "densidad": "ligera", "lactosa": False},
            {"nombre": "chantilly", "categoria": "ligera", "densidad": "ligera", "lactosa": True},
            {"nombre": "ganache", "categoria": "densa", "densidad": "densa", "lactosa": False},
            {"nombre": "crema-vegetal", "categoria": "vegetal", "densidad": "ligera", "lactosa": False}
        ]
    }


# -----------------------------------------------------------------------------
# ENDPOINTS DE AUTENTICACIÓN Y USUARIOS (SQL SERVER)
# -----------------------------------------------------------------------------
@app.post("/api/v1/auth/registro", tags=["Autenticación"])
def registro(datos: UsuarioRegistro):
  try:
    usuario = registrar_usuario(
        nombre=datos.nombre,
        correo=datos.correo,
        password=datos.password,
        restriccion=datos.restriccion_predeterminada,
        perfil=datos.perfil_favorito,
    )
    if not usuario:
      raise HTTPException(
          status_code=400, detail="No se pudo registrar el usuario."
      )
    return {"mensaje": "Usuario registrado con éxito", "usuario": usuario}
  except Exception as e:
    # 📢 Imprimir el error exacto en tu consola de PowerShell:
    print(f"\n❌ ERROR REAL AL REGISTRAR: {str(e)}\n")
    raise HTTPException(
        status_code=400, detail=f"Error al registrar usuario: {str(e)}"
    )


@app.post("/api/v1/auth/login", tags=["Autenticación"])
def login(credenciales: UsuarioLogin):
    """Verifica correo/contraseña y devuelve su recomendación personalizada inmediata."""
    usuario = autenticar_usuario(credenciales.correo, credenciales.password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos.")

    # Al autenticarse, recuperamos su pastel por defecto según historial o perfil
    recomendacion = obtener_recomendacion_personalizada(usuario["id_usuario"])

    return {
        "mensaje": "Inicio de sesión exitoso",
        "usuario": usuario,
        "recomendacion_predeterminada": recomendacion
    }


@app.get("/api/v1/usuarios/{id_usuario}/recomendacion", tags=["Personalización"])
def recomendacion_usuario(id_usuario: int):
    """Retorna la recomendación por defecto para el usuario según su memoria en la DB."""
    rec = obtener_recomendacion_personalizada(id_usuario)
    if not rec:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return rec


@app.get("/api/v1/usuarios/{id_usuario}/historial", tags=["Personalización"])
def historial_usuario(id_usuario: int):
    """Retorna el listado de pasteles previos evaluados por CLIPS para este usuario."""
    return obtener_historial_usuario(id_usuario)


# -----------------------------------------------------------------------------
# ENDPOINT PRINCIPAL DEL MOTOR DE INFERENCIA
# -----------------------------------------------------------------------------
@app.post("/api/v1/recomendar", response_model=ResultadoOutput, tags=["Motor"])
def recomendar_pastel(solicitud: SolicitudRecomendacion, id_usuario: Optional[int] = None):
    """
    Recibe la solicitud, ejecuta el motor CLIPSpy y, si se envía un id_usuario,
    guarda automáticamente la inferencia en la tabla HistorialRecomendaciones de SQL Server.
    """
    try:
        # 1. Ejecutar inferencia en CLIPS
        resultado = motor.procesar_peticion(solicitud)

        # 2. Persistir en SQL Server si hay usuario asociado
        try:
            guardar_historial_recomendacion(
                id_usuario=id_usuario,
                modo=solicitud.modo,
                restriccion=solicitud.restriccion or "ninguna",
                perfil=solicitud.perfil,
                resultado=resultado
            )
        except Exception as db_err:
            print(f"[Aviso DB] No se pudo guardar en SQL Server: {db_err}")

        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la ejecución de la inferencia: {str(e)}")
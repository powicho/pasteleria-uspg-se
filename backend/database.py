import hashlib
import os
from typing import Any, Dict, List, Optional
import pyodbc

# 1. Servidores locales ordenados
SERVIDORES_LOCALES = [
    r"powicho\SQLEXPRESS",  # 1. Tu máquina actual
    r".\SQLEXPRESS",  # 2. Máquina de la presentación
    r"localhost\SQLEXPRESS",
    "localhost",
    r".",
]


def get_conexion():
  """Prueba y conecta con la instancia de SQL Server disponible en la máquina."""
  ultimo_error = None
  for server in SERVIDORES_LOCALES:
    cadena = (
        f"DRIVER={{ODBC Driver 17 for SQL"
        f" Server}};SERVER={server};DATABASE=PasteleriaUSPG;Trusted_Connection=yes;TrustServerCertificate=yes;"
    )
    try:
      return pyodbc.connect(cadena, timeout=2)
    except Exception as e:
      ultimo_error = e
      continue
  raise ultimo_error


# 🔐 AGREGA ESTA FUNCIÓN AQUÍ:
def hash_password(password: str) -> str:
  """Genera un hash SHA-256 para guardar contraseñas de forma segura."""
  return hashlib.sha256(password.encode("utf-8")).hexdigest()

# -----------------------------------------------------------------------------
# GESTIÓN DE USUARIOS
# -----------------------------------------------------------------------------


# 1. REGISTRAR CON CONTRASEÑA NORMAL (Texto plano)
def registrar_usuario(
    nombre: str,
    correo: str,
    password: str,
    restriccion: str = "ninguna",
    perfil: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
  conn = get_conexion()
  cursor = conn.cursor()

  try:
    pass_directa = password.strip()  # Guardamos la contraseña tal cual la escribes
    cursor.execute(
        """
            INSERT INTO Usuarios (nombre, correo, password_hash, restriccion_predeterminada, perfil_favorito)
            OUTPUT INSERTED.id_usuario, INSERTED.nombre, INSERTED.correo, INSERTED.restriccion_predeterminada, INSERTED.perfil_favorito
            VALUES (?, ?, ?, ?, ?)
        """,
        (nombre, correo.lower().strip(), pass_directa, restriccion, perfil),
    )
    fila = cursor.fetchone()
    conn.commit()
    if fila:
      return {
          "id_usuario": fila[0],
          "nombre": fila[1],
          "correo": fila[2],
          "restriccion": fila[3],
          "perfil_favorito": fila[4],
      }
    return None
  except Exception as e:
    conn.rollback()
    raise e
  finally:
    conn.close()


# 2. LOGIN CON CONTRASEÑA NORMAL (Comparación directa)
def autenticar_usuario(correo: str, password: str) -> Optional[Dict[str, Any]]:
  conn = get_conexion()
  cursor = conn.cursor()
  pass_directa = password.strip()

  cursor.execute(
      """
        SELECT id_usuario, nombre, correo, restriccion_predeterminada, perfil_favorito
        FROM Usuarios
        WHERE correo = ? AND password_hash = ?
    """,
      (correo.lower().strip(), pass_directa),
  )

  fila = cursor.fetchone()
  conn.close()

  if fila:
    return {
        "id_usuario": fila[0],
        "nombre": fila[1],
        "correo": fila[2],
        "restriccion": fila[3],
        "perfil_favorito": fila[4],
    }
  return None

# -----------------------------------------------------------------------------
# HISTORIAL Y RECOMENDACIÓN PERSONALIZADA
# -----------------------------------------------------------------------------


def guardar_historial_recomendacion(
    id_usuario: Optional[int],
    modo: str,
    restriccion: str,
    perfil: Optional[str],
    resultado: Dict[str, Any],
):
  conn = get_conexion()
  cursor = conn.cursor()

  comps = resultado.get("componentes", [])
  b_final = comps[0] if len(comps) > 0 else None
  r_final = comps[1] if len(comps) > 1 else None
  c_final = comps[2] if len(comps) > 2 else None

  cursor.execute(
      """
        INSERT INTO HistorialRecomendaciones 
        (id_usuario, modo, restriccion, perfil_solicitado, bizcocho_final, relleno_final, cobertura_final, estado, tipo_receta, mensaje, justificacion, regla_activada)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
      (
          id_usuario,
          modo,
          restriccion,
          perfil,
          b_final,
          r_final,
          c_final,
          resultado.get("estado", "desconocido"),
          resultado.get("tipo_receta", "error"),
          resultado.get("mensaje", ""),
          resultado.get("justificacion", ""),
          resultado.get("regla", "NINGUNA"),
      ),
  )

  # Si el usuario eligió un pastel viable en filtro-general, actualizar su perfil favorito
  if (
      id_usuario
      and perfil
      and perfil != "ninguno"
      and resultado.get("estado") == "viable"
  ):
    cursor.execute(
        """
            UPDATE Usuarios 
            SET perfil_favorito = ?, restriccion_predeterminada = ?
            WHERE id_usuario = ?
        """,
        (perfil, restriccion, id_usuario),
    )

  conn.commit()
  conn.close()


def obtener_recomendacion_personalizada(
    id_usuario: int,) -> Optional[Dict[str, Any]]:
  """Calcula dinámicamente el pastel MÁS PEDIDO por el usuario en su historial."""
  conn = get_conexion()
  cursor = conn.cursor()

  # 1. Obtener nombre y restricción del usuario
  cursor.execute(
      "SELECT nombre, restriccion_predeterminada FROM Usuarios WHERE"
      " id_usuario = ?",
      (id_usuario,),
  )
  user = cursor.fetchone()
  if not user:
    conn.close()
    return None

  nombre_usuario, restriccion = user[0], user[1]

  # 2. SQL GROUP BY: Encontrar la combinación exacta con más pedidos exitosos (viable)
  cursor.execute(
      """
        SELECT TOP 1 
            bizcocho_final, 
            relleno_final, 
            cobertura_final, 
            COUNT(*) AS total_pedidos,
            MAX(mensaje) AS mensaje,
            MAX(regla_activada) AS regla_activada,
            MAX(fecha_consulta) AS ultima_fecha
        FROM HistorialRecomendaciones
        WHERE id_usuario = ? 
          AND estado = 'viable' 
          AND bizcocho_final IS NOT NULL
        GROUP BY bizcocho_final, relleno_final, cobertura_final
        ORDER BY total_pedidos DESC, MAX(fecha_consulta) DESC
    """,
      (id_usuario,),
  )

  favorito = cursor.fetchone()
  conn.close()

  # Si el usuario tiene al menos 1 pastel en su historial, devolvemos el más pedido
  if favorito:
    return {
        "usuario": nombre_usuario,
        "restriccion": restriccion,
        "bizcocho": favorito[0],
        "relleno": favorito[1],
        "cobertura": favorito[2],
        "total_pedidos": favorito[3],
        "mensaje": favorito[4],
        "regla": favorito[5],
        "fecha": str(favorito[6])[:19],
    }

  # Si es un usuario nuevo sin historial, retornamos None (la recomendación nacerá cuando cree su primer pastel)
  return None

def obtener_historial_usuario(id_usuario: int) -> List[Dict[str, Any]]:
  conn = get_conexion()
  cursor = conn.cursor()
  cursor.execute(
      """
        SELECT id_recomendacion, modo, restriccion, bizcocho_final, relleno_final, cobertura_final, estado, tipo_receta, mensaje, regla_activada, fecha_consulta
        FROM HistorialRecomendaciones
        WHERE id_usuario = ?
        ORDER BY fecha_consulta DESC
    """,
      (id_usuario,),
  )

  filas = cursor.fetchall()
  conn.close()

  return [{
      "id": f[0],
      "modo": f[1],
      "restriccion": f[2],
      "bizcocho": f[3],
      "relleno": f[4],
      "cobertura": f[5],
      "estado": f[6],
      "tipo_receta": f[7],
      "mensaje": f[8],
      "regla": f[9],
      "fecha": str(f[10])[:19],
  } for f in filas]
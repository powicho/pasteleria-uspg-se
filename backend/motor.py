import os
from typing import Any, Dict
import clips
from backend.modelos import SolicitudRecomendacion


class MotorPasteleria:

  def __init__(self, clp_path: str = None):
    self.env = clips.Environment()
    if clp_path is None:
      base_dir = os.path.dirname(os.path.abspath(__file__))
      clp_path = os.path.join(base_dir, "pasteleria.clp")
    self.clp_path = clp_path
    self._inicializar_motor()

  def _inicializar_motor(self):
    self.env.clear()
    self.env.load(self.clp_path)
    self.env.reset()

  def reiniciar(self):
    self.env.reset()

  def establecer_solicitud(
      self,
      modo: str,
      restriccion: str = "ninguna",
      perfil: str = "ninguno",
  ):
    fact_str = (
        f"(solicitud (modo {modo}) (restriccion {restriccion}) (perfil"
        f" {perfil}))"
    )
    self.env.assert_string(fact_str)

  def agregar_componente(
      self,
      tipo: str,
      nombre: str,
      categoria: str,
      densidad: str = "ligera",
      contiene_lactosa: str = "no",
  ):
    fact_str = (
        f"(componente (tipo {tipo}) (nombre {nombre}) (categoria {categoria})"
        f" (densidad {densidad}) (contiene-lactosa {contiene_lactosa}))"
    )
    self.env.assert_string(fact_str)

  def resolver(self) -> Dict[str, Any]:
    """Ejecuta la inferencia y extrae el hecho 'resultado' generado por CLIPS."""
    self.env.run()

    for fact in self.env.facts():
      if fact.template.name == "resultado":
        return {
            "estado": str(fact["estado"]),
            "tipo_receta": str(fact["tipo-receta"]),
            "componentes": [str(c) for c in fact["componentes"]],
            "mensaje": str(fact["mensaje"]),
            "justificacion": str(fact["justificacion"]),
            "regla": str(fact["regla"]),
        }

    return {
        "estado": "desconocido",
        "tipo_receta": "error",
        "componentes": [],
        "mensaje": "No se activó ninguna regla para esta combinación.",
        "justificacion": "Entrada fuera de cobertura de reglas.",
        "regla": "NINGUNA",
    }

  def procesar_peticion(
      self, solicitud: SolicitudRecomendacion
  ) -> Dict[str, Any]:
    """Método directo para atender solicitudes desde FastAPI limpiando el entorno."""
    self.reiniciar()
    self.establecer_solicitud(
        modo=solicitud.modo,
        restriccion=solicitud.restriccion or "ninguna",
        perfil=solicitud.perfil or "ninguno",
    )

    if solicitud.componentes:
      for comp in solicitud.componentes:
        self.agregar_componente(
            tipo=comp.tipo,
            nombre=comp.nombre,
            categoria=comp.categoria,
            densidad=comp.densidad or "ligera",
            contiene_lactosa=comp.contiene_lactosa or "no",
        )

    return self.resolver()
import os
import clips


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

  def resolver(self) -> dict:
    """Ejecuta la inferencia y retorna el hecho resultado como diccionario."""
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
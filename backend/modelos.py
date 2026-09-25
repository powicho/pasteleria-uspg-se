from typing import List, Optional
from pydantic import BaseModel, Field


# Modelo para un componente individual ingresado por el usuario
class ComponenteInput(BaseModel):
  tipo: str = Field(
      ...,
      description="Tipo de capa: bizcocho, relleno o cobertura",
      example="bizcocho",
  )
  nombre: str = Field(
      ..., description="Nombre del ingrediente", example="limon"
  )
  categoria: str = Field(
      ...,
      description=(
          "Categoría organoléptica: citrico, amargo, dulce, frutal, cremoso,"
          " ligera, densa, vegetal"
      ),
      example="citrico",
  )
  densidad: Optional[str] = Field(
      "ligera", description="Densidad física: ligera o densa", example="ligera"
  )
  contiene_lactosa: Optional[str] = Field(
      "no",
      description="Indica si contiene derivados lácteos: si o no",
      example="no",
  )


# Modelo para la solicitud enviada por el cliente
class SolicitudRecomendacion(BaseModel):
  modo: str = Field(
      ...,
      description="Modo de consulta: 'filtro-general' o 'individual'",
      example="filtro-general",
  )
  restriccion: Optional[str] = Field(
      "ninguna",
      description="Restricción dietética: 'ninguna' o 'sin-lactosa'",
      example="ninguna",
  )
  perfil: Optional[str] = Field(
      "ninguno",
      description=(
          "Perfil de sabor (en modo filtro-general): citrico-ligero,"
          " chocolatoso-denso, frutal-saludable"
      ),
      example="citrico-ligero",
  )
  componentes: Optional[List[ComponenteInput]] = Field(
      default_factory=list,
      description=(
          "Lista de componentes seleccionados (requerido en modo individual)"
      ),
  )


# Modelo para la respuesta generada por el motor de inferencia
class ResultadoOutput(BaseModel):
  estado: str = Field(
      ...,
      description="Estado de la combinación: viable, incompatible o incompleto",
  )
  tipo_receta: str = Field(
      ..., description="Tipo de resultado: exacta, ajustada o error"
  )
  componentes: List[str] = Field(
      default_factory=list, description="Lista de componentes finales del pastel"
  )
  mensaje: str = Field(..., description="Explicación clara para el cliente")
  justificacion: str = Field(
      ..., description="Rastro de inferencia técnica del sistema experto"
  )
  regla: str = Field(
      ..., description="Identificador de la regla CLIPS que se activó"
  )


# Modelo de estado de salud del sistema
class HealthCheck(BaseModel):
  estado: str
  sistema: str
  motor: str
  integracion: str
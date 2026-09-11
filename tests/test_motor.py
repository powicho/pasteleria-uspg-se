import pytest
from backend.motor import MotorPasteleria


@pytest.fixture
def motor():
  """Crea una instancia fresca del motor antes de cada prueba."""
  m = MotorPasteleria()
  m.reiniciar()
  return m


# -----------------------------------------------------------------------------
# ESCENARIOS DE PRUEBA
# -----------------------------------------------------------------------------


def test_filtro_general_citrico_ligero(motor):
  """Comprueba que el perfil cítrico ligero recomiende Limón + Maracuyá + Merengue."""
  motor.establecer_solicitud(
      modo="filtro-general", restriccion="ninguna", perfil="citrico-ligero"
  )
  resultado = motor.resolver()

  assert resultado["estado"] == "viable"
  assert resultado["tipo_receta"] == "exacta"
  assert resultado["regla"] == "R05-Filtro-Citrico-Ligero"
  assert "limon" in resultado["componentes"]
  assert "maracuya" in resultado["componentes"]
  assert "merengue-italiano" in resultado["componentes"]


def test_filtro_general_sin_lactosa(motor):
  """Comprueba que una solicitud sin lactosa recomiende la receta vegetal frutal."""
  motor.establecer_solicitud(
      modo="filtro-general",
      restriccion="sin-lactosa",
      perfil="frutal-saludable",
  )
  resultado = motor.resolver()

  assert resultado["estado"] == "viable"
  assert resultado["tipo_receta"] == "exacta"
  assert resultado["regla"] == "R07-Filtro-Sin-Lactosa-Frutal"
  assert "vainilla-vegetal" in resultado["componentes"]


def test_configuracion_incompleta(motor):
  """Comprueba que falte un componente (ej. falta cobertura) active la regla de terna incompleta."""
  motor.establecer_solicitud(modo="individual", restriccion="ninguna")
  # Solo bizcocho y relleno, falta cobertura
  motor.agregar_componente(
      tipo="bizcocho", nombre="vainilla", categoria="dulce"
  )
  motor.agregar_componente(
      tipo="relleno", nombre="dulce-de-leche", categoria="cremoso"
  )

  resultado = motor.resolver()
  assert resultado["estado"] == "incompleto"
  assert resultado["tipo_receta"] == "error"
  assert resultado["regla"] == "R01-Configuracion-Incompleta"


def test_conflicto_lactosa_en_seleccion_individual(motor):
  """Comprueba que si el usuario pide sin-lactosa pero incluye un lácteo, se active R02."""
  motor.establecer_solicitud(modo="individual", restriccion="sin-lactosa")
  motor.agregar_componente(
      tipo="bizcocho",
      nombre="vainilla",
      categoria="dulce",
      contiene_lactosa="no",
  )
  motor.agregar_componente(
      tipo="relleno",
      nombre="tres-leches",
      categoria="cremoso",
      contiene_lactosa="si",
  )  # Lácteo
  motor.agregar_componente(
      tipo="cobertura",
      nombre="crema-vegetal",
      categoria="vegetal",
      contiene_lactosa="no",
  )

  resultado = motor.resolver()
  assert resultado["estado"] == "incompatible"
  assert resultado["tipo_receta"] == "ajustada"
  assert resultado["regla"] == "R02-Prioridad-Restriccion-Lactosa"


def test_conflicto_organoleptico_limon_con_cremoso(motor):
  """Comprueba que Bizcocho de Limón con Relleno Cremoso dispare ajuste de sabor."""
  motor.establecer_solicitud(modo="individual", restriccion="ninguna")
  motor.agregar_componente(
      tipo="bizcocho", nombre="limon", categoria="citrico", densidad="ligera"
  )
  motor.agregar_componente(
      tipo="relleno",
      nombre="tres-leches",
      categoria="cremoso",
      densidad="ligera",
  )
  motor.agregar_componente(
      tipo="cobertura",
      nombre="merengue",
      categoria="ligera",
      densidad="ligera",
  )

  resultado = motor.resolver()
  assert resultado["estado"] == "incompatible"
  assert resultado["tipo_receta"] == "ajustada"
  assert resultado["regla"] == "R04-Conflicto-Limon-Cremoso"


def test_seleccion_individual_viable_exacta(motor):
  """Comprueba que una terna armónica y completa devuelva Receta Exacta viable."""
  motor.establecer_solicitud(modo="individual", restriccion="ninguna")
  motor.agregar_componente(
      tipo="bizcocho", nombre="vainilla", categoria="dulce", densidad="ligera"
  )
  motor.agregar_componente(
      tipo="relleno",
      nombre="dulce-de-leche",
      categoria="cremoso",
      densidad="ligera",
  )
  motor.agregar_componente(
      tipo="cobertura",
      nombre="chantilly",
      categoria="ligera",
      densidad="ligera",
  )

  resultado = motor.resolver()
  assert resultado["estado"] == "viable"
  assert resultado["tipo_receta"] == "exacta"
  assert resultado["regla"] == "R08-Seleccion-Individual-Viable"
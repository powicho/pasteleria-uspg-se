from backend.main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)


def test_api_health_check():
  """Verifica que el endpoint GET /api/v1/health responda con los datos esperados (Diapositiva 7)."""
  response = client.get("/api/v1/health")
  assert response.status_code == 200
  data = response.json()
  assert data["estado"] == "OK"
  assert data["sistema"] == "PasteleriaUSPG"
  assert data["motor"] == "CLIPS"
  assert data["integracion"] == "clipspy"


def test_api_filtro_citrico_ligero():
  """Verifica que POST /api/v1/recomendar responda con receta exacta cítrica."""
  payload = {
      "modo": "filtro-general",
      "restriccion": "ninguna",
      "perfil": "citrico-ligero",
  }
  response = client.post("/api/v1/recomendar", json=payload)
  assert response.status_code == 200
  data = response.json()
  assert data["estado"] == "viable"
  assert data["tipo_receta"] == "exacta"
  assert data["regla"] == "R05-Filtro-Citrico-Ligero"
  assert "limon" in data["componentes"]


def test_api_filtro_sin_lactosa():
  """Verifica que la restricción sin lactosa devuelva receta vegetal en la API."""
  payload = {
      "modo": "filtro-general",
      "restriccion": "sin-lactosa",
      "perfil": "frutal-saludable",
  }
  response = client.post("/api/v1/recomendar", json=payload)
  assert response.status_code == 200
  data = response.json()
  assert data["estado"] == "viable"
  assert data["regla"] == "R07-Filtro-Sin-Lactosa-Frutal"


def test_api_configuracion_incompleta():
  """Verifica que si faltan componentes en modo individual, la API retorne estado incompleto."""
  payload = {
      "modo": "individual",
      "restriccion": "ninguna",
      "componentes": [
          {"tipo": "bizcocho", "nombre": "vainilla", "categoria": "dulce"}
      ],
  }
  response = client.post("/api/v1/recomendar", json=payload)
  assert response.status_code == 200
  data = response.json()
  assert data["estado"] == "incompleto"
  assert data["tipo_receta"] == "error"
  assert data["regla"] == "R01-Configuracion-Incompleta"


def test_api_conflicto_lactosa_genera_ajuste():
  """Verifica que la API detecte violación de alérgenos y retorne receta ajustada."""
  payload = {
      "modo": "individual",
      "restriccion": "sin-lactosa",
      "componentes": [
          {
              "tipo": "bizcocho",
              "nombre": "vainilla",
              "categoria": "dulce",
              "contiene_lactosa": "no",
          },
          {
              "tipo": "relleno",
              "nombre": "tres-leches",
              "categoria": "cremoso",
              "contiene_lactosa": "si",
          },
          {
              "tipo": "cobertura",
              "nombre": "crema-vegetal",
              "categoria": "vegetal",
              "contiene_lactosa": "no",
          },
      ],
  }
  response = client.post("/api/v1/recomendar", json=payload)
  assert response.status_code == 200
  data = response.json()
  assert data["estado"] == "incompatible"
  assert data["tipo_receta"] == "ajustada"
  assert data["regla"] == "R02-Prioridad-Restriccion-Lactosa"
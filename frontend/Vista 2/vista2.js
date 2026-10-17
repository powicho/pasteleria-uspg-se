const API_URL = "http://127.0.0.1:8000/api/v1";

let seleccion = {
  restriccion: "ninguna",
  bizcocho: { nombre: "limon", categoria: "citrico", densidad: "ligera", lactosa: "no" },
  relleno: { nombre: "frutos-rojos", categoria: "frutal", densidad: "ligera", lactosa: "no" },
  cobertura: { nombre: "crema-vegetal", categoria: "vegetal", densidad: "ligera", lactosa: "no" }
};

function toggleLactosa(checked) {
  seleccion.restriccion = checked ? "sin-lactosa" : "ninguna";
  document.getElementById("lbl-lactosa").innerText = checked ? "Activado" : "Desactivado";
  document.querySelectorAll(".lacteo").forEach(el => el.classList.toggle("disabled", checked));
}

function seleccionar(tipo, nombre, categoria, densidad, lactosa, color, elemento) {
  elemento.parentElement.querySelectorAll(".option-card").forEach(el => el.classList.remove("active"));
  elemento.classList.add("active");

  seleccion[tipo] = { nombre, categoria, densidad, lactosa };
  document.getElementById(`prev-${tipo}`).style.background = color;
}

async function validarCombinacion() {
  const payload = {
    modo: "individual",
    restriccion: seleccion.restriccion,
    perfil: "ninguno",
    componentes: [
      { tipo: "bizcocho", nombre: seleccion.bizcocho.nombre, categoria: seleccion.bizcocho.categoria, densidad: seleccion.bizcocho.densidad, contiene_lactosa: seleccion.bizcocho.lactosa },
      { tipo: "relleno", nombre: seleccion.relleno.nombre, categoria: seleccion.relleno.categoria, densidad: seleccion.relleno.densidad, contiene_lactosa: seleccion.relleno.lactosa },
      { tipo: "cobertura", nombre: seleccion.cobertura.nombre, categoria: seleccion.cobertura.categoria, densidad: seleccion.cobertura.densidad, contiene_lactosa: seleccion.cobertura.lactosa }
    ]
  };

  try {
    const res = await fetch(`${API_URL}/recomendar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    
    // Guardar en sesión y viajar a Vista 4 (el resumen interactivo)
    sessionStorage.setItem("resultadoPastel", JSON.stringify(data));
    sessionStorage.setItem("seleccionActual", JSON.stringify(seleccion));
    window.location.href = "../Vista 4/vista4.html";
  } catch (error) {
    alert("Error conectando con la API de FastAPI.");
  }
}
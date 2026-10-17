const API_URL = "http://127.0.0.1:8000/api/v1";

let seleccion = {
  restriccion: "ninguna",
  perfil: "citrico-ligero"
};

// Verificar API
fetch(`${API_URL}/health`).catch(() => {
  const dot = document.querySelector(".status-dot");
  const txt = document.getElementById("api-status-text");
  if (dot) dot.style.background = "#C0392B";
  if (txt) { txt.innerText = "API Offline"; txt.parentElement.style.color = "#C0392B"; }
});

function seleccionarRestriccion(tipo) {
  seleccion.restriccion = tipo;
  document.getElementById("btn-rest-ninguna").classList.toggle("active", tipo === "ninguna");
  document.getElementById("btn-rest-lactosa").classList.toggle("active", tipo === "sin-lactosa");
}

function seleccionarPerfil(perfil, card) {
  seleccion.perfil = perfil;
  document.querySelectorAll(".profile-card").forEach(c => c.classList.remove("active"));
  card.classList.add("active");

  const btnNinguna = document.getElementById("btn-rest-ninguna");
  const btnLactosa = document.getElementById("btn-rest-lactosa");

  if (perfil === "frutal-saludable") {
    // 1. Poner en automático 'Sin lactosa'
    seleccionarRestriccion("sin-lactosa");

    // 2. Bloquear botones para que no se puedan cambiar
    btnNinguna.style.pointerEvents = "none";
    btnNinguna.style.opacity = "0.35";
    btnLactosa.style.pointerEvents = "none";
  } else {
    // 3. Desbloquear cuando elija Cítrico o Chocolatoso
    btnNinguna.style.pointerEvents = "auto";
    btnNinguna.style.opacity = "1";
    btnLactosa.style.pointerEvents = "auto";
    
    // 4. Regresar automáticamente a 'Ninguna'
   seleccionarRestriccion("ninguna");
  }
}


async function consultarExperto() {
  const payload = {
    modo: "filtro-general",
    restriccion: seleccion.restriccion,
    perfil: seleccion.perfil,
    componentes: []
  };

  try {
    const res = await fetch(`${API_URL}/recomendar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    
    // Guardar en sesión y viajar a Vista 3
    sessionStorage.setItem("resultadoPastel", JSON.stringify(data));
    sessionStorage.setItem("origenVista", "../Vista 1/index.html");
    window.location.href = "../Vista 3/vista3.html";
  } catch (error) {
    alert("No se pudo conectar con el motor de CLIPS. Asegúrate de ejecutar: uvicorn backend.main:app --reload");
  }
}
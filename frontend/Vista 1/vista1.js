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

window.addEventListener("DOMContentLoaded", async () => {
  const userRaw = localStorage.getItem("usuarioActivo");
  if (!userRaw) return;

  const user = JSON.parse(userRaw);

  // 1. Mostrar botón de salir
  const btnLogout = document.getElementById("btn-logout");
  if (btnLogout) btnLogout.style.display = "inline-flex";

  // 2. Consultar en vivo a SQL Server cuál es el pastel más pedido de este usuario
  try {
    const res = await fetch(`${API_URL}/usuarios/${user.id_usuario}/recomendacion`);
    if (res.ok) {
      const rec = await res.json();
      localStorage.setItem("recomendacionPersonalizada", JSON.stringify(rec));

      // Si SQL Server encontró un pastel favorito, mostramos el banner dorado:
      const banner = document.getElementById("banner-personalizado");
      if (banner && rec && rec.bizcocho) {
        banner.style.display = "block";
        document.getElementById("user-display-name").innerText = `👤 ${user.nombre}`;
        
        const veces = rec.total_pedidos > 1 ? `(Pedido ${rec.total_pedidos} veces)` : `(Tu última creación)`;
        document.getElementById("pb-titulo").innerText = `Tu Pastel Favorito ${veces}`;
        
        document.getElementById("pb-b").innerText = rec.bizcocho;
        document.getElementById("pb-r").innerText = rec.relleno;
        document.getElementById("pb-c").innerText = rec.cobertura;
      }
    }
  } catch (err) {
    console.log("No se pudo cargar la recomendación dinámica:", err);
  }
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


// 1. Cuando consultan con los botones de abajo:
async function consultarExperto() {
  const payload = {
    modo: "filtro-general",
    restriccion: seleccion.restriccion,
    perfil: seleccion.perfil,
    componentes: []
  };

  try {
    // 👤 Adjuntar el ID del usuario si está logueado
    const user = JSON.parse(localStorage.getItem("usuarioActivo") || "{}");
    const urlApi = user.id_usuario 
      ? `${API_URL}/recomendar?id_usuario=${user.id_usuario}` 
      : `${API_URL}/recomendar`;

    const res = await fetch(urlApi, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    sessionStorage.setItem("resultadoPastel", JSON.stringify(data));
    sessionStorage.setItem("origenVista", "../Vista 1/index.html");
    window.location.href = "../Vista 3/vista3.html";
  } catch (error) {
    alert("No se pudo conectar con el motor de CLIPS.");
  }
}

// 2. Cuando hacen clic en el banner dorado "Aprobar este pastel de inmediato":
async function ordenarPersonalizado() {
  const recRaw = localStorage.getItem("recomendacionPersonalizada");
  if (!recRaw) return;
  const rec = JSON.parse(recRaw);

  const payload = {
    modo: "filtro-general",
    restriccion: rec.restriccion || "sin-lactosa",
    perfil: rec.perfil_favorito || "frutal-saludable",
    componentes: []
  };

  try {
    // 👤 Adjuntar el ID del usuario si está logueado
    const user = JSON.parse(localStorage.getItem("usuarioActivo") || "{}");
    const urlApi = user.id_usuario 
      ? `${API_URL}/recomendar?id_usuario=${user.id_usuario}` 
      : `${API_URL}/recomendar`;

    const res = await fetch(urlApi, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    sessionStorage.setItem("resultadoPastel", JSON.stringify(data));
    sessionStorage.setItem("origenVista", "../Vista 1/index.html");
    window.location.href = "../Vista 3/vista3.html";
  } catch (err) {
    alert("Error conectando con CLIPS.");
  }
}

function cerrarSesion() {
  if (confirm("¿Deseas cerrar tu sesión?")) {
    // Limpiar datos del usuario activo
    localStorage.removeItem("usuarioActivo");
    localStorage.removeItem("recomendacionPersonalizada");
    sessionStorage.clear();

    // Redirigir al Login
    window.location.href = "../Login/login.html";
  }
}
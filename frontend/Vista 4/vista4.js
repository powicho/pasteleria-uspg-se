const API_URL = "http://127.0.0.1:8000/api/v1";

window.addEventListener("DOMContentLoaded", () => {
  const dataRaw = sessionStorage.getItem("resultadoPastel");
  if (!dataRaw) {
    window.location.href = "../Vista 2/vista2.html";
    return;
  }

  const data = JSON.parse(dataRaw);
  renderizar(data);
});

function renderizar(data) {
  const banner = document.getElementById("v4-banner");
  const bannerText = document.getElementById("v4-banner-text");

  if (data.estado === "viable") {
    banner.className = "banner-compatible";
    bannerText.innerText = "Combinación completa y compatible — ¡Lista para hornear!";
  } else {
    banner.className = "banner-compatible banner-incompatible";
    bannerText.innerText = "Combinación ajustada por el pastelero para evitar choques de sabor";
  }

  if (data.componentes && data.componentes.length >= 3) {
    document.getElementById("v4-bizcocho").innerText = data.componentes[0];
    document.getElementById("v4-relleno").innerText = data.componentes[1];
    document.getElementById("v4-cobertura").innerText = data.componentes[2];

    document.getElementById("sel-bizcocho").value = data.componentes[0];
    document.getElementById("sel-relleno").value = data.componentes[1];
    document.getElementById("sel-cobertura").value = data.componentes[2];
  }

  document.getElementById("v4-titulo-veredicto").innerText = data.mensaje;
  document.getElementById("v4-desc-veredicto").innerText = data.justificacion;
}

async function recalcular() {
  const b = document.getElementById("sel-bizcocho").value;
  const r = document.getElementById("sel-relleno").value;
  const c = document.getElementById("sel-cobertura").value;

  const payload = {
    modo: "individual",
    restriccion: "ninguna",
    perfil: "ninguno",
    componentes: [
      { tipo: "bizcocho", nombre: b, categoria: "dulce", densidad: "ligera", contiene_lactosa: "no" },
      { tipo: "relleno", nombre: r, categoria: "cremoso", densidad: "ligera", contiene_lactosa: (r === 'tres-leches' || r === 'dulce-de-leche') ? 'si' : 'no' },
      { tipo: "cobertura", nombre: c, categoria: "ligera", densidad: "ligera", contiene_lactosa: c === 'chantilly' ? 'si' : 'no' }
    ]
  };

  try {
    const res = await fetch(`${API_URL}/recomendar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    renderizar(data);
  } catch (err) {
    alert("Error al recalcular con CLIPS.");
  }
}

function confirmar() {
  alert("🎉 ¡Pedido confirmado con éxito!\nTu pastel ha sido enviado a cocina con la Ficha Técnica aprobada por el Maestro Pastelero.");
}
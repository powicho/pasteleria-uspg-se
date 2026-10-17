window.addEventListener("DOMContentLoaded", () => {
  const dataRaw = sessionStorage.getItem("resultadoPastel");
  if (!dataRaw) {
    window.location.href = "../Vista 1/index.html";
    return;
  }

  const data = JSON.parse(dataRaw);
  const banner = document.getElementById("banner-estado");

  if (data.estado === "viable") {
    banner.className = "status-banner banner-viable";
    document.getElementById("banner-icon").innerText = "✔";
    document.getElementById("banner-texto").innerText = "Viable — ¡Combinación perfecta aprobada!";
  } else if (data.estado === "incompatible") {
    banner.className = "status-banner banner-ajustada";
    document.getElementById("banner-icon").innerText = "⚡";
    document.getElementById("banner-texto").innerText = "Incompatible — Receta ajustada por el pastelero";
  } else {
    banner.className = "status-banner banner-incompleto";
    document.getElementById("banner-icon").innerText = "✖";
    document.getElementById("banner-texto").innerText = "Incompleto — Faltan componentes para hornear";
  }

  if (data.componentes && data.componentes.length >= 3) {
    document.getElementById("chip-bizcocho").innerText = data.componentes[0];
    document.getElementById("chip-relleno").innerText = data.componentes[1];
    document.getElementById("chip-cobertura").innerText = data.componentes[2];
  }

  document.getElementById("txt-mensaje").innerText = data.mensaje;
  document.getElementById("txt-justificacion").innerText = data.justificacion;
  document.getElementById("txt-regla").innerText = `Regla activada: ${data.regla}`;
});

function volver() {
  const origen = sessionStorage.getItem("origenVista") || "../Vista 1/index.html";
  window.location.href = origen;
}
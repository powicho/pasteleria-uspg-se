const API_URL = "http://127.0.0.1:8000/api/v1";

function cambiarAuth(tab) {
  document.getElementById("tab-login").classList.toggle("active", tab === "login");
  document.getElementById("tab-registro").classList.toggle("active", tab === "registro");
  document.getElementById("form-login").style.display = tab === "login" ? "block" : "none";
  document.getElementById("form-registro").style.display = tab === "registro" ? "block" : "none";
}

async function hacerLogin(e) {
  e.preventDefault();
  const correo = document.getElementById("log-correo").value;
  const password = document.getElementById("log-pass").value;

  try {
    const res = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correo, password })
    });

    if (!res.ok) {
      alert("❌ Correo o contraseña incorrectos.");
      return;
    }

    const data = await res.json();
    
    // Guardar usuario y su recomendación personalizada en sesión
    localStorage.setItem("usuarioActivo", JSON.stringify(data.usuario));
    localStorage.setItem("recomendacionPersonalizada", JSON.stringify(data.recomendacion_predeterminada));

    // Redirigir a la Vista 1
    window.location.href = "../Vista 1/index.html";
  } catch (err) {
    alert("Error de conexión con el backend.");
  }
}

async function hacerRegistro(e) {
  e.preventDefault();
  const payload = {
    nombre: document.getElementById("reg-nombre").value,
    correo: document.getElementById("reg-correo").value,
    password: document.getElementById("reg-pass").value,
    restriccion_predeterminada: document.getElementById("reg-restriccion").value,
    perfil_favorito: null // <-- Vacío al inicio
  };

  try {
    const res = await fetch(`${API_URL}/auth/registro`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

 if (!res.ok) {
      // 🔍 Leemos el error exacto que mandó Python
      const errData = await res.json();
      alert(`❌ ${errData.detail || "Error al registrar usuario."}`);
      return;
    }

    alert("🎉 ¡Usuario creado con éxito! Ahora inicia sesión.");
    cambiarAuth("login");
  } catch (err) {
    alert("Error de conexión al registrar.");
  }
}
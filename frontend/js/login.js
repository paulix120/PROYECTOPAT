// ==========================================
// CONFIGURACIÓN API
// ==========================================
const API_URL = "http://127.0.0.1:8000";

// ==========================================
// DECODIFICAR JWT
// ==========================================
function parseJwt(token) {
    try {
        const base64Url = token.split(".")[1];
        const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        const jsonPayload = decodeURIComponent(
            window.atob(base64).split("").map(function (c) {
                return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
            }).join("")
        );
        return JSON.parse(jsonPayload);
    } catch (error) {
        console.error("Error al decodificar el token:", error);
        return null;
    }
}

// ==========================================
// LOGIN
// ==========================================
document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {
        alert("Por favor completa todos los campos.");
        return;
    }

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
        });

        const data = await response.json();

        // LOGIN CORRECTO
        if (response.ok) {
            const token = data.access_token;
            localStorage.setItem("token", token);

            const tokenData = parseJwt(token);
            if (!tokenData) {
                alert("No se pudo procesar la información de sesión.");
                localStorage.removeItem("token");
                return;
            }

            // CORRECCIÓN 1: El token de FastAPI devuelve 'id_rol', no 'rol_id'
            const userRole = Number(tokenData.id_rol);

            localStorage.setItem("userRole", userRole);
            localStorage.setItem("userEmail", tokenData.email || email);
            localStorage.setItem("userName", tokenData.nombre || "");

            // CORRECCIÓN 2: Rutas arregladas basándome en tu estructura de carpetas
            if (userRole === 2) {
                // Si llegas a crear una carpeta menu_admin, la ruta sería esta:
                window.location.href = "menu_admin/menu_admin.html";
            } else {
                // Esta es la ruta correcta para ir al menú que me pasaste
                window.location.href = "menu_usuario/menu_usuario.html"; 
            }

        } else {
            alert(data.detail || "Correo o contraseña incorrectos.");
        }

    } catch (error) {
        console.error("Error al iniciar sesión:", error);
        alert("No se pudo conectar con el servidor. Verifica que FastAPI esté ejecutándose.");
    }
});
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

        const base64 = base64Url
            .replace(/-/g, "+")
            .replace(/_/g, "/");

        const jsonPayload = decodeURIComponent(
            window
                .atob(base64)
                .split("")
                .map(function (c) {
                    return (
                        "%" +
                        ("00" + c.charCodeAt(0).toString(16)).slice(-2)
                    );
                })
                .join("")
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

document
    .getElementById("loginForm")
    .addEventListener("submit", async (e) => {

        e.preventDefault();

        const email = document
            .getElementById("email")
            .value
            .trim();

        const password = document
            .getElementById("password")
            .value;


        if (!email || !password) {
            alert("Por favor completa todos los campos.");
            return;
        }


        // FastAPI OAuth2 espera:
        // username
        // password

        const formData = new URLSearchParams();

        formData.append("username", email);
        formData.append("password", password);


        try {

            const response = await fetch(
                `${API_URL}/auth/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    },

                    body: formData
                }
            );


            const data = await response.json();


            // ==========================================
            // LOGIN CORRECTO
            // ==========================================

            if (response.ok) {

                const token = data.access_token;


                // Guardar JWT
                localStorage.setItem(
                    "token",
                    token
                );


                // Decodificar información del usuario
                const tokenData = parseJwt(token);


                if (!tokenData) {

                    alert(
                        "No se pudo procesar la información de sesión."
                    );

                    localStorage.removeItem("token");

                    return;
                }


                const userRole = Number(
                    tokenData.rol_id
                );


                // Guardar algunos datos útiles
                localStorage.setItem(
                    "userRole",
                    userRole
                );

                localStorage.setItem(
                    "userEmail",
                    tokenData.email || email
                );

                localStorage.setItem(
                    "userName",
                    tokenData.nombre || ""
                );


                alert(
                    "¡Inicio de sesión exitoso!"
                );


                // ==========================================
                // REDIRECCIÓN POR ROL
                // ==========================================

                if (userRole === 2) {

                    window.location.href =
                        "menu_admin.html";

                } else {

                    window.location.href =
                        "menu_usuario.html";
                }


            } else {

                alert(
                    data.detail ||
                    "Correo o contraseña incorrectos."
                );
            }


        } catch (error) {

            console.error(
                "Error al iniciar sesión:",
                error
            );

            alert(
                "No se pudo conectar con el servidor. " +
                "Verifica que FastAPI esté ejecutándose."
            );
        }

    });
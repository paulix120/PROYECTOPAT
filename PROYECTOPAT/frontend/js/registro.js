// ==========================================
// CONFIGURACIÓN API
// ==========================================

const API_URL = "http://127.0.0.1:8000";


// ==========================================
// REGISTRO
// ==========================================

document
    .getElementById("registerForm")
    .addEventListener("submit", async (e) => {

        e.preventDefault();


        const nombre = document
            .getElementById("nombre")
            .value
            .trim();

        const apellido = document
            .getElementById("apellido")
            .value
            .trim();

        const email = document
            .getElementById("email")
            .value
            .trim();

        const password = document
            .getElementById("password")
            .value;

        const confirmPassword = document
            .getElementById("confirmPassword")
            .value;


        // ==========================================
        // VALIDACIONES
        // ==========================================

        if (
            !nombre ||
            !apellido ||
            !email ||
            !password ||
            !confirmPassword
        ) {

            alert(
                "Por favor completa todos los campos."
            );

            return;
        }


        if (password !== confirmPassword) {

            alert(
                "Las contraseñas no coinciden."
            );

            return;
        }


        // ==========================================
        // CONEXIÓN CON API
        // ==========================================

        try {

            const response = await fetch(
                `${API_URL}/auth/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        nombre: nombre,

                        apellido: apellido,

                        email: email,

                        password: password

                    })
                }
            );


            const data = await response.json();


            // ==========================================
            // REGISTRO CORRECTO
            // ==========================================

            if (response.ok) {

                alert(
                    "¡Usuario registrado con éxito! " +
                    "Redirigiendo al inicio de sesión..."
                );


                window.location.href =
                    "login.html";


            } else {

                alert(
                    data.detail ||
                    "Ocurrió un error al registrar el usuario."
                );
            }


        } catch (error) {

            console.error(
                "Error al registrar:",
                error
            );

            alert(
                "No se pudo conectar con el servidor. " +
                "Verifica que FastAPI esté ejecutándose."
            );
        }

    });
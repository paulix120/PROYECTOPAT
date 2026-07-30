// Función para decodificar el payload del Token JWT
function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        return JSON.parse(jsonPayload);
    } catch (e) {
        return null;
    }
}

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const response = await fetch('http://127.0.0.1:8000/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // 1. Guardar el token en el navegador
            localStorage.setItem('token', data.access_token);
            
            // 2. Extraer el rol del token
            const tokenData = parseJwt(data.access_token);
            const userRole = tokenData ? tokenData.rol_id : 1;

            alert('¡Inicio de sesión exitoso!');

            // 3. Redirección según la Historia de Usuario por Rol
            if (userRole === 2) {
                // Si es Administrador
                window.location.href = 'menu_admin.html';
            } else {
                // Si es Usuario común / Turista (Rol 1)
                window.location.href = 'menu_usuario.html';
            }

        } else {
            alert(data.detail || 'Credenciales incorrectas');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('No se pudo conectar con el servidor.');
    }
});
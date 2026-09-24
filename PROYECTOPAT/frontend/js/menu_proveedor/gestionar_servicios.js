console.log("🚀 JS de Proveedor Conectado Correctamente");

const API_URL = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");

document.addEventListener("DOMContentLoaded", async () => {
    console.log("Iniciando carga de la página...");

    // Cargar catálogos desde la base de datos
    await cargarCatalogos();

    // Escuchar el formulario
    const form = document.getElementById("formCrearServicio");
    if (form) {
        form.addEventListener("submit", procesarCreacionServicio);
    }
});

// =======================================================
// CARGA DE LISTAS DESPLEGABLES DESDE FASTAPI / MYSQL
// =======================================================
async function cargarCatalogos() {
    console.log("Consultando catálogos en el backend...");

    // 1. Tipos de Turismo
    try {
        const res = await fetch(`${API_URL}/tipos-turismo/`);
        if (res.ok) {
            const data = await res.json();
            console.log("Turismos recibidos:", data);
            const sel = document.getElementById("id_tp_turi");
            sel.innerHTML = '<option value="">-- Selecciona Turismo --</option>' +
                data.map(t => `<option value="${t.id_tp_turi}">${t.nombre}</option>`).join("");
        } else {
            console.warn("Fallo al traer tipos de turismo, status:", res.status);
        }
    } catch (err) {
        console.error("Error conectando a tipos-turismo:", err);
    }

    // 2. Gamas
    try {
        const res = await fetch(`${API_URL}/gamas/`);
        if (res.ok) {
            const data = await res.json();
            console.log("Gamas recibidas:", data);
            const sel = document.getElementById("id_gama");
            sel.innerHTML = '<option value="">-- Selecciona Gama --</option>' +
                data.map(g => `<option value="${g.id_gama}">${g.nombre}</option>`).join("");
        } else {
            console.warn("Fallo al traer gamas, status:", res.status);
        }
    } catch (err) {
        console.error("Error conectando a gamas:", err);
    }

    // 3. Ubicaciones
    try {
        const res = await fetch(`${API_URL}/ubicaciones/`);
        if (res.ok) {
            const data = await res.json();
            console.log("Ubicaciones recibidas:", data);
            const sel = document.getElementById("id_ubi");
            sel.innerHTML = '<option value="">-- Selecciona Ubicación --</option>' +
                data.map(u => `<option value="${u.id_ubi}">${u.direccion || 'Ubicación'} (${u.barrio || 'Centro'})</option>`).join("");
        } else {
            console.warn("Fallo al traer ubicaciones, status:", res.status);
        }
    } catch (err) {
        console.error("Error conectando a ubicaciones:", err);
    }
}

// =======================================================
// ADAPTAR CAMPOS SEGÚN CATEGORÍA SELECCIONADA
// =======================================================
function adaptarFormularioSegunTipo() {
    const tipo = document.getElementById("id_tp_serv").value;
    const contenedor = document.getElementById("contenedorDinamico");
    const titulo = document.getElementById("tituloDinamico");
    const campos = document.getElementById("camposDinamicos");

    if (!tipo) {
        contenedor.style.display = "none";
        campos.innerHTML = "";
        return;
    }

    contenedor.style.display = "block";

    if (tipo === "1") { // HOSPEDAJE
        titulo.textContent = "🏨 Detalles de la Habitación / Espacio Inicial";
        campos.innerHTML = `
            <div>
                <label>Nombre de la Habitación / Unidad: *</label>
                <input type="text" id="nom_unidad" placeholder="Ej: Suite Matrimonial Vista al Mar" required>
            </div>
            <div>
                <label>Capacidad (N° de Personas): *</label>
                <input type="number" id="capacidad_personas" min="1" value="2" required>
            </div>
            <div>
                <label>Valor por Noche ($ COP): *</label>
                <input type="number" id="vlr_noche" min="1" placeholder="Ej: 250000" required>
            </div>
            <div>
                <label>Horario Check-in:</label>
                <input type="text" id="horario_checkin" placeholder="Ej: 15:00">
            </div>
        `;
    } else if (tipo === "2") { // GASTRONOMÍA
        titulo.textContent = "🍽️ Detalle del Menú / Platillo Principal";
        campos.innerHTML = `
            <div>
                <label>Nombre del Platillo o Menú: *</label>
                <input type="text" id="nom_platillo_menu" placeholder="Ej: Bandeja Paisa Especial" required>
            </div>
            <div>
                <label>Porciones que rinde: *</label>
                <input type="number" id="porciones" min="1" value="1" required>
            </div>
            <div>
                <label>Precio Estimado ($ COP): *</label>
                <input type="number" id="vlr_estimado" min="1" placeholder="Ej: 45000" required>
            </div>
            <div>
                <label>Horario de Atención:</label>
                <input type="text" id="horario_atencion" placeholder="Ej: 11:00 AM - 10:00 PM">
            </div>
        `;
    } else if (tipo === "3") { // RECREACIÓN
        titulo.textContent = "🏖️ Detalle de la Actividad / Entrada";
        campos.innerHTML = `
            <div>
                <label>Nombre de la Actividad: *</label>
                <input type="text" id="nom_actividad" placeholder="Ej: Pasaporte Entrada General" required>
            </div>
            <div>
                <label>Valor por Persona ($ COP): *</label>
                <input type="number" id="vlr_persona" min="0" placeholder="Ej: 30000" required>
            </div>
            <div>
                <label>Duración Estimada:</label>
                <input type="text" id="duracion" placeholder="Ej: 3 horas">
            </div>
            <div>
                <label>Horario de Disponibilidad:</label>
                <input type="text" id="horario" placeholder="Ej: 9:00 AM - 5:00 PM">
            </div>
        `;
    } else if (tipo === "4") { // TRANSPORTE
        titulo.textContent = "🚌 Detalle del Vehículo y Tarifa";
        campos.innerHTML = `
            <div>
                <label>Tipo de Vehículo: *</label>
                <input type="text" id="tipo_vehiculo" placeholder="Ej: Van Ejecutiva Mercedes" required>
            </div>
            <div>
                <label>Capacidad de Pasajeros: *</label>
                <input type="number" id="capacidad_pasajeros" min="1" placeholder="Ej: 14" required>
            </div>
            <div>
                <label>Tarifa Base o Pasaje ($ COP): *</label>
                <input type="number" id="tarifa_base" min="0" placeholder="Ej: 85000" required>
            </div>
            <div>
                <label>Valor por Kilómetro (si aplica):</label>
                <input type="number" id="vlr_km" min="0" value="0">
            </div>
        `;
    } else if (tipo === "5") { // GUÍA
        titulo.textContent = "🗺️ Detalle del Tour Guiado";
        campos.innerHTML = `
            <div>
                <label>Nombre del Tour: *</label>
                <input type="text" id="nombre_tour" placeholder="Ej: Tour Histórico por el Centro" required>
            </div>
            <div>
                <label>Valor total del Tour ($ COP): *</label>
                <input type="number" id="vlr_tour" min="1" placeholder="Ej: 120000" required>
            </div>
            <div>
                <label>Duración en Horas: *</label>
                <input type="number" id="duracion_horas" min="1" placeholder="Ej: 4" required>
            </div>
            <div>
                <label>Cupo Máximo del Grupo: *</label>
                <input type="number" id="capacidad_grupo" min="1" placeholder="Ej: 15" required>
            </div>
            <div>
                <label>Dificultad:</label>
                <select id="dificultad">
                    <option value="BAJA">Baja</option>
                    <option value="MEDIA" selected>Media</option>
                    <option value="ALTA">Alta</option>
                </select>
            </div>
        `;
    }
}

// =======================================================
// ENVÍO AL BACKEND
// =======================================================
async function procesarCreacionServicio(e) {
    e.preventDefault();

    const tipo = document.getElementById("id_tp_serv").value;
    const btn = document.getElementById("btnGuardar");
    btn.disabled = true;
    btn.textContent = "Guardando servicio...";

    try {
        let idServicioCreado = null;

        if (tipo === "1") {
            const resBase = await fetch(`${API_URL}/servicios/hospedajes/base`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
                body: JSON.stringify({
                    nombre: document.getElementById("nombre").value.trim(),
                    descripcion: document.getElementById("descripcion").value.trim(),
                    id_tp_turi: parseInt(document.getElementById("id_tp_turi").value),
                    id_gama: parseInt(document.getElementById("id_gama").value),
                    id_ubi: parseInt(document.getElementById("id_ubi").value)
                })
            });
            const dataBase = await resBase.json();
            if (!resBase.ok) throw new Error(dataBase.detail || "Error creando hotel base.");
            idServicioCreado = dataBase.id_servicio;

            const resHijo = await fetch(`${API_URL}/servicios/hospedajes/${idServicioCreado}/espacios`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
                body: JSON.stringify({
                    nom_unidad: document.getElementById("nom_unidad").value.trim(),
                    capacidad_personas: parseInt(document.getElementById("capacidad_personas").value),
                    vlr_noche: parseFloat(document.getElementById("vlr_noche").value),
                    horario_checkin: document.getElementById("horario_checkin")?.value || "15:00",
                    horario_checkout: "11:00"
                })
            });
            if (!resHijo.ok) throw new Error("Se creó el hotel pero falló al registrar la habitación.");
        }
        else if (tipo === "2") {
            const resBase = await fetch(`${API_URL}/servicios/gastronomia/restaurantes/base`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
                body: JSON.stringify({
                    nombre: document.getElementById("nombre").value.trim(),
                    descripcion: document.getElementById("descripcion").value.trim(),
                    id_tp_turi: parseInt(document.getElementById("id_tp_turi").value),
                    id_gama: parseInt(document.getElementById("id_gama").value),
                    id_ubi: parseInt(document.getElementById("id_ubi").value)
                })
            });
            const dataBase = await resBase.json();
            if (!resBase.ok) throw new Error(dataBase.detail || "Error creando restaurante base.");
            idServicioCreado = dataBase.id_servicio;

            const resHijo = await fetch(`${API_URL}/servicios/gastronomia/restaurantes/${idServicioCreado}/platos`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
                body: JSON.stringify({
                    nom_platillo_menu: document.getElementById("nom_platillo_menu").value.trim(),
                    porciones: parseInt(document.getElementById("porciones").value),
                    vlr_estimado: parseFloat(document.getElementById("vlr_estimado").value),
                    horario_atencion: document.getElementById("horario_atencion")?.value || "Todo el día"
                })
            });
            if (!resHijo.ok) throw new Error("Se creó el restaurante pero falló al registrar el menú.");
        }
        else if (tipo === "3") {
            const res = await fetch(`${API_URL}/servicios/recreacion/`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
                body: JSON.stringify({
                    nombre: document.getElementById("nombre").value.trim(),
                    descripcion: document.getElementById("descripcion").value.trim(),
                    id_tp_turi: parseInt(document.getElementById("id_tp_turi").value),
                    id_gama: parseInt(document.getElementById("id_gama").value),
                    id_ubi: parseInt(document.getElementById("id_ubi").value),
                    nom_actividad: document.getElementById("nom_actividad").value.trim(),
                    duracion: document.getElementById("duracion")?.value || "2 horas",
                    horario: document.getElementById("horario")?.value || "Diurno",
                    vlr_persona: parseFloat(document.getElementById("vlr_persona").value),
                    capacidad: 50,
                    es_evento_local: false
                })
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || "Error registrando actividad.");
            idServicioCreado = data.id_servicio;
        }
        else if (tipo === "4") {
            const res = await fetch(`${API_URL}/servicios/transporte/`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
                body: JSON.stringify({
                    nombre: document.getElementById("nombre").value.trim(),
                    descripcion: document.getElementById("descripcion").value.trim(),
                    id_tp_turi: parseInt(document.getElementById("id_tp_turi").value),
                    id_gama: parseInt(document.getElementById("id_gama").value),
                    id_ubi: parseInt(document.getElementById("id_ubi").value),
                    tipo_vehiculo: document.getElementById("tipo_vehiculo").value.trim(),
                    capacidad_pasajeros: parseInt(document.getElementById("capacidad_pasajeros").value),
                    tarifa_base: parseFloat(document.getElementById("tarifa_base").value),
                    vlr_km: parseFloat(document.getElementById("vlr_km")?.value || 0),
                    es_ruta_programada: false
                })
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || "Error registrando transporte.");
            idServicioCreado = data.id_servicio;
        }
        else if (tipo === "5") {
            const res = await fetch(`${API_URL}/servicios/guias/`, {
                method: "POST",
                headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
                body: JSON.stringify({
                    nombre: document.getElementById("nombre").value.trim(),
                    descripcion: document.getElementById("descripcion").value.trim(),
                    id_tp_turi: parseInt(document.getElementById("id_tp_turi").value),
                    id_gama: parseInt(document.getElementById("id_gama").value),
                    id_ubi: parseInt(document.getElementById("id_ubi").value),
                    nombre_tour: document.getElementById("nombre_tour").value.trim(),
                    vlr_tour: parseFloat(document.getElementById("vlr_tour").value),
                    duracion_horas: parseInt(document.getElementById("duracion_horas").value),
                    capacidad_grupo: parseInt(document.getElementById("capacidad_grupo").value),
                    dificultad: document.getElementById("dificultad").value
                })
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || "Error registrando guía.");
            idServicioCreado = data.id_servicio;
        }

        alert("¡Servicio publicado con éxito en la plataforma PAT!");
        document.getElementById("formCrearServicio").reset();
        document.getElementById("contenedorDinamico").style.display = "none";

    } catch (err) {
        console.error(err);
        alert("⚠️ " + err.message);
    } finally {
        btn.disabled = false;
        btn.textContent = "Publicar Servicio en PAT →";
    }
}

function cerrarSesion() {
    localStorage.clear();
    window.location.href = "login.html";
}
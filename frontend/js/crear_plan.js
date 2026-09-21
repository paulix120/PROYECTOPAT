const API_URL = "http://127.0.0.1:8000";
let token = localStorage.getItem("token");
let ubicacionesList = []; 
let todosLosServicios = [];
let planActual = null; 
let tipoServicioActual = "";
let mapaCrearPlanInstance = null; 
let controlRuta = null; 
let serviciosFiltradosMemoria = [];
let servicioSeleccionadoModal = null;

document.addEventListener("DOMContentLoaded", async () => {
    if (!token) { window.location.href = "../login.html"; return; }
    await cargarUbicaciones();
    await cargarCatalogoCompleto();

    // 💡 SOLUCIÓN: Leer la URL si venimos de "Ver planes -> Agregar más servicios"
    const urlParams = new URLSearchParams(window.location.search);
    const planId = urlParams.get('planId');
    if (planId) {
        await cargarPlanExistente(planId);
    }

    document.getElementById("crearPlanForm").addEventListener("submit", crearPlanBase);
    document.getElementById("formAgregarItem").addEventListener("submit", procesarFormularioItem);
});

async function cargarUbicaciones() {
    const res = await fetch(`${API_URL}/ubicaciones/`);
    ubicacionesList = res.ok ? await res.json() : [];
    const opts = `<option value="">-- Selecciona --</option>` + ubicacionesList.map(u => `<option value="${u.id_ubi}">${u.direccion} (${u.ciudad || u.barrio || ''})</option>`).join("");
    document.getElementById("origenPlan").innerHTML = opts;
    document.getElementById("destinoPlan").innerHTML = opts;
}

async function cargarCatalogoCompleto() {
    const res = await fetch(`${API_URL}/servicios/`);
    if (res.ok) todosLosServicios = await res.json();
}

async function cargarPlanExistente(id_plan) {
    const res = await fetch(`${API_URL}/planes-viaje/mis-planes`, { headers: { "Authorization": `Bearer ${token}` } });
    if (res.ok) {
        const misPlanes = await res.json();
        planActual = misPlanes.find(p => p.id_plan_viaje == id_plan);
        if (planActual) {
            document.getElementById("seccionPlanBase").style.display = "none";
            document.getElementById("seccionItems").style.display = "block"; // Se corrigió el ID aquí
            document.getElementById("tituloPlanActivo").textContent = planActual.nombre_plan;
            document.getElementById("fechasPlanActivo").textContent = `Del ${planActual.fecha_inicio} al ${planActual.fecha_fin}`;
            renderizarResumen();
        }
    }
}

async function crearPlanBase(e) {
    e.preventDefault();
    const payload = {
        nombre_plan: document.getElementById("nombrePlan").value,
        fecha_inicio: document.getElementById("fechaInicio").value,
        fecha_fin: document.getElementById("fechaFin").value,
        id_ubicacion_origen: parseInt(document.getElementById("origenPlan").value),
        id_ubicacion_destino: parseInt(document.getElementById("destinoPlan").value)
    };
    
    try {
        const res = await fetch(`${API_URL}/planes-viaje/`, {
            method: "POST", headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` }, body: JSON.stringify(payload)
        });
        const data = await res.json();
        
        if (res.ok) {
            await cargarPlanExistente(data.id_plan_viaje);
        } else alert(data.detail);
    } catch (error) { console.error(error); alert("Error de conexión"); }
}

function renderizarResumen() {
    const ul = document.getElementById("listaResumen"); ul.innerHTML = "";
    (planActual.items_agregados || []).forEach(it => {
        ul.innerHTML += `<li><strong>${it.fecha_servicio}</strong> | [${it.tipo_item}] ${it.observaciones || ''} <span style="color:#16a34a; font-weight:bold; float:right;">+$${Number(it.subtotal_calculado).toLocaleString()}</span></li>`;
    });
    document.getElementById("costoTotal").innerText = Number(planActual.costo_total_estimado).toLocaleString();
}

function cambiarDePlan() {
    planActual = null; 
    document.getElementById("seccionPlanBase").style.display = "block"; 
    document.getElementById("seccionItems").style.display = "none";
    window.history.replaceState(null, '', 'crear_plan.html'); // Limpia la URL
    document.getElementById("crearPlanForm").reset();
}

async function cargarCategoria() {
    tipoServicioActual = document.getElementById("tipoServicio").value;
    const gTarjetas = document.getElementById("grupoTarjetas");
    const gCarro = document.getElementById("grupoCarroPropio");

    if (!tipoServicioActual) { gTarjetas.style.display = "none"; gCarro.style.display = "none"; return; }

    if (tipoServicioActual === "TRANSPORTE_PROPIO") {
        gTarjetas.style.display = "none"; gCarro.style.display = "block";
        actualizarMapaEnVivo();
        return;
    }

    gTarjetas.style.display = "block"; gCarro.style.display = "none";
    
    const mapTipo = { "HOSPEDAJE": 1, "GASTRONOMIA": 2, "DESTINO_TURISTICO": 3, "TRANSPORTE": 4, "GUIA": 5 };
    serviciosFiltradosMemoria = todosLosServicios.filter(s => s.id_tp_serv === mapTipo[tipoServicioActual]);

    // Filtrar vuelos y buses hacia la ciudad de destino
    if (tipoServicioActual === "TRANSPORTE") {
        try {
            const res = await fetch(`${API_URL}/servicios/transporte/`);
            const transportes = await res.json();
            const destinoPlan = ubicacionesList.find(u => u.id_ubi == planActual.id_ubicacion_destino);
            
            if (destinoPlan) {
                serviciosFiltradosMemoria = serviciosFiltradosMemoria.filter(s => {
                    const tr = transportes.find(t => t.servicio_base.id_servicio === s.id_servicio);
                    if (!tr || !tr.detalle.id_destino) return false;
                    const destTrans = ubicacionesList.find(u => u.id_ubi == tr.detalle.id_destino);
                    return destTrans && destTrans.id_cdad === destinoPlan.id_cdad; 
                });
            }
        } catch (e) { console.error("Error filtrando transporte", e); }
    }
    
    renderizarTarjetas(serviciosFiltradosMemoria);
}

function renderizarTarjetas(servicios) {
    const cCerca = document.getElementById("cardsCerca"); const cLejos = document.getElementById("cardsLejos");
    cCerca.innerHTML = ""; cLejos.innerHTML = "";
    const ubiDestino = ubicacionesList.find(u => u.id_ubi == planActual.id_ubicacion_destino);

    servicios.forEach(s => {
        const img = s.imagen_principal ? (s.imagen_principal.startsWith('http') ? s.imagen_principal : API_URL+s.imagen_principal) : 'https://via.placeholder.com/300x200?text=Servicio';
        const html = `
            <div class="tarjeta-servicio" onclick="abrirModal(${s.id_servicio})">
                <img src="${img}">
                <h4 style="color:#0f172a; margin-bottom:4px; font-size:15px;">${s.nombre}</h4>
                <p style="color:#64748b; font-size:12px;">📍 ${s.ubicacion ? s.ubicacion.direccion : 'Ubicación no registrada'}</p>
            </div>`;
        
        if (ubiDestino && s.ubicacion && s.ubicacion.id_cdad === ubiDestino.id_cdad) cCerca.innerHTML += html;
        else cLejos.innerHTML += html;
    });

    if (cCerca.innerHTML === "") cCerca.innerHTML = "<p style='color:#64748b; font-size: 13px;'>No hay servicios registrados en tu ciudad de destino.</p>";
    if (cLejos.innerHTML === "") cLejos.innerHTML = "<p style='color:#64748b; font-size: 13px;'>No se encontraron más servicios.</p>";
}

async function abrirModal(id_servicio) {
    const s = todosLosServicios.find(x => x.id_servicio === id_servicio);
    servicioSeleccionadoModal = s;
    document.getElementById("modalSubTitulo").textContent = s.nombre;
    const sel = document.getElementById("modalSubSelect"); sel.innerHTML = "<option value=''>Cargando opciones...</option>";
    
    let ep = "";
    if (tipoServicioActual === "HOSPEDAJE") ep = "hospedajes";
    else if (tipoServicioActual === "GASTRONOMIA") ep = "gastronomia/restaurantes";
    else if (tipoServicioActual === "TRANSPORTE") ep = "transporte/";
    else if (tipoServicioActual === "DESTINO_TURISTICO") ep = "recreacion/";
    else if (tipoServicioActual === "GUIA") ep = "guias/";

    try {
        const res = await fetch(`${API_URL}/servicios/${ep}`); const data = await res.json();
        sel.innerHTML = "<option value=''>-- Selecciona Opción --</option>"; 
        let din = "";

        if (tipoServicioActual === "HOSPEDAJE") {
            const hs = data.find(x => x.id_servicio === id_servicio);
            if(hs) hs.habitaciones_disponibles.forEach(h => sel.innerHTML += `<option value="${h.id_hosp}">${h.nom_unidad} ($${h.vlr_noche})</option>`);
            din = `<label style="font-weight:bold; color:#334155;">Personas (Huéspedes):</label><br><input type="number" id="modPer" value="1" min="1" style="width:100%; padding:10px; border-radius:6px; border:1px solid #cbd5e1; margin-top:6px; margin-bottom:16px;"><br>
                   <label style="font-weight:bold; color:#334155;">Cantidad de Noches:</label><br><input type="number" id="modCant" value="1" min="1" style="width:100%; padding:10px; border-radius:6px; border:1px solid #cbd5e1; margin-top:6px; margin-bottom:16px;">`;
        } else if (tipoServicioActual === "GASTRONOMIA") {
            const rs = data.find(x => x.id_servicio === id_servicio);
            if(rs) rs.menu_disponible.forEach(m => sel.innerHTML += `<option value="${m.id_gast}">${m.nom_platillo_menu} ($${m.vlr_estimado})</option>`);
            din = `<label style="font-weight:bold; color:#334155;">Platos / Porciones:</label><br><input type="number" id="modCant" value="1" min="1" style="width:100%; padding:10px; border-radius:6px; border:1px solid #cbd5e1; margin-top:6px; margin-bottom:16px;">`;
        } else {
            const ts = data.find(x => x.servicio_base.id_servicio === id_servicio);
            if(ts) {
                const d = ts.detalle; const id = d.id_trans || d.id_rec || d.id_guia;
                const nom = d.tipo_vehiculo || d.nom_actividad || d.nombre_tour;
                const precio = d.tarifa_base || d.vlr_persona || d.vlr_tour;
                sel.innerHTML += `<option value="${id}">${nom} ($${precio})</option>`;
            }
            din = `<label style="font-weight:bold; color:#334155;">Cantidad (Personas/Pasajeros):</label><br><input type="number" id="modCant" value="1" min="1" style="width:100%; padding:10px; border-radius:6px; border:1px solid #cbd5e1; margin-top:6px; margin-bottom:16px;">`;
        }
        document.getElementById("modalInputsDinamicos").innerHTML = din;
        document.getElementById("modalFecha").value = planActual.fecha_inicio;
        document.getElementById("modalFecha").min = planActual.fecha_inicio;
        document.getElementById("modalFecha").max = planActual.fecha_fin;
        document.getElementById("modalSubservicios").style.display = "flex";
    } catch (e) { sel.innerHTML = "<option value=''>Error cargando opciones.</option>"; }
}

function cerrarModal() { document.getElementById("modalSubservicios").style.display = "none"; }

async function procesarFormularioItem(e) {
    e.preventDefault();
    const sel = document.getElementById("modalSubSelect");
    if (!sel.value) return;

    let cant = parseInt(document.getElementById("modCant").value); let obsAdic = "";
    if (tipoServicioActual === "HOSPEDAJE") obsAdic = `| Habitación para ${document.getElementById("modPer").value} personas por ${cant} noches.`;
    else obsAdic = `| Cant: ${cant}`;

    const payload = {
        id_servicio: servicioSeleccionadoModal.id_servicio, tipo_item: tipoServicioActual, 
        id_item_especifico: parseInt(sel.value), cantidad: cant,
        fecha_servicio: document.getElementById("modalFecha").value, 
        observaciones: `${servicioSeleccionadoModal.nombre} - ${sel.options[sel.selectedIndex].text.split('($')[0].trim()} ${obsAdic}`
    };
    enviarItem(payload);
}

function actualizarMapaEnVivo() {
    if (!planActual.id_ubicacion_origen || !planActual.id_ubicacion_destino) {
        document.getElementById("infoRutaCalculada").innerHTML = "⚠️ Tu plan de viaje no tiene Origen y Destino configurados. Ve a 'Mis Viajes Guardados', pulsa en '📍 Origen/Destino' en este plan para guardarlos y vuelve a intentar.";
        return;
    }

    const ori = ubicacionesList.find(u => u.id_ubi == planActual.id_ubicacion_origen); 
    const des = ubicacionesList.find(u => u.id_ubi == planActual.id_ubicacion_destino);
    if(!ori || !des) return;

    const mapContainer = document.getElementById("mapaCrearPlan");
    if (mapaCrearPlanInstance) { mapaCrearPlanInstance.remove(); } 
    const parent = mapContainer.parentNode; parent.removeChild(mapContainer);
    
    const newMapDiv = document.createElement("div");
    newMapDiv.id = "mapaCrearPlan"; newMapDiv.style.height = "300px"; newMapDiv.style.width = "100%"; newMapDiv.style.marginTop = "10px"; newMapDiv.style.border = "1px solid #ccc"; newMapDiv.style.borderRadius = "8px"; newMapDiv.style.zIndex = "1";
    parent.insertBefore(newMapDiv, document.getElementById("infoRutaCalculada"));

    mapaCrearPlanInstance = L.map("mapaCrearPlan").setView([4.6534, -74.1162], 6);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(mapaCrearPlanInstance);

    document.getElementById("infoRutaCalculada").innerHTML = "⏳ Calculando ruta por carretera...";

    if(L.Routing) {
        L.Routing.control({
            waypoints: [ L.latLng(ori.latitud, ori.longitud), L.latLng(des.latitud, des.longitud) ],
            routeWhileDragging: false, addWaypoints: false, show: false,
            createMarker: function(i, wp) { return L.marker(wp.latLng).bindPopup(i===0 ? "Tu Origen: "+ori.direccion : "Tu Destino: "+des.direccion); },
            lineOptions: { styles: [{ color: '#2563eb', opacity: 0.9, weight: 5 }] }
        }).on('routesfound', function(e) {
            const dKm = Math.round(e.routes[0].summary.totalDistance / 1000); const tM = Math.round(e.routes[0].summary.totalTime / 60);
            document.getElementById("infoRutaCalculada").innerHTML = `🚗 Distancia Vía: <strong>${dKm} km</strong> | ⏱️ <strong>${Math.floor(tM/60)}h ${tM%60}min</strong> | ⛽ Gasolina Estimada: $${(dKm*450).toLocaleString()} COP`;
        }).addTo(mapaCrearPlanInstance);
    }
}

async function agregarCarroPropio() {
    if (!planActual.id_ubicacion_origen || !planActual.id_ubicacion_destino) {
        alert("No puedes agregar carro propio sin tener un origen y destino en el plan.");
        return;
    }
    const payload = { tipo_item: "TRANSPORTE_PROPIO", cantidad: 1, fecha_servicio: planActual.fecha_inicio, observaciones: "Viajar en Carro Propio" };
    enviarItem(payload);
}

async function enviarItem(payload) {
    try {
        const res = await fetch(`${API_URL}/planes-viaje/${planActual.id_plan_viaje}/items`, {
            method: "POST", headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` }, body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) { 
            cerrarModal(); 
            await cargarPlanExistente(planActual.id_plan_viaje);
            alert("¡Agregado al carrito de tu plan!"); 
        } else alert("⚠️ " + data.detail);
    } catch (error) { console.error(error); alert("Error de conexión"); }
}

function finalizarPlan() { window.location.href = "ver_planes.html"; }
function cerrarSesion() { localStorage.clear(); window.location.href = "../login.html"; }
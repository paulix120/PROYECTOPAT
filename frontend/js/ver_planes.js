const API_URL = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");
let planesGlobal = [];

document.addEventListener("DOMContentLoaded", () => {
    if (!token) { window.location.href = "../login.html"; return; }
    cargarMisPlanes();
});

function cerrarSesion() { localStorage.clear(); window.location.href = "../login.html"; }

async function cargarMisPlanes() {
    try {
        const res = await fetch(`${API_URL}/planes-viaje/mis-planes`, { headers: { "Authorization": `Bearer ${token}` } });
        if (res.ok) planesGlobal = await res.json();
        else planesGlobal = [];
    } catch (err) { planesGlobal = []; }
    renderizarPlanes(planesGlobal);
}

function renderizarPlanes(planes) {
    const cont = document.getElementById("listaMisPlanes");
    cont.innerHTML = "";
    let sumaTotal = 0;

    if (!planes || planes.length === 0) {
        cont.innerHTML = `<div style="text-align:center; padding:40px; background:#fff; border-radius:8px; border:1px solid #ccc;">Aún no tienes viajes creados.</div>`;
        document.getElementById("granTotal").textContent = "$0 COP";
        return;
    }

    planes.forEach(plan => {
        const totalPlan = Number(plan.costo_total_estimado) || 0;
        sumaTotal += totalPlan;

        let itemsHTML = "";
        const items = plan.items_agregados || [];

        // Generar cada servicio agregado
        items.forEach(it => {
            const desc = it.observaciones || it.tipo_item;
            const sub = Number(it.subtotal_calculado || 0).toLocaleString();
            let tiempoTxt = "";
            if (it.tiempo_estimado_min > 0) {
                const h = Math.floor(it.tiempo_estimado_min / 60); const m = it.tiempo_estimado_min % 60;
                tiempoTxt = ` | ⏱️ ${h > 0 ? h + 'h ' : ''}${m}m`;
            }
            
            // Renderizado del ítem con botones de editar y eliminar propios
            itemsHTML += `
            <div style="display:flex; justify-content:space-between; margin-bottom: 10px; padding: 12px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 5px;">
                <div>
                    <div style="font-size: 15px; color: #000;"><strong>[${it.tipo_item}]</strong> ${desc}</div>
                    <div style="font-size: 13px; color: #666; margin-top: 5px;">📅 ${it.fecha_servicio} | Cant: ${it.cantidad}${tiempoTxt}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight:bold; color:#28a745; font-size: 16px; margin-bottom: 8px;">+$${sub}</div>
                    <div>
                        <button onclick="editarItem(${it.id_det_plan}, ${it.cantidad}, '${it.tipo_item}', '${it.fecha_servicio}')" style="cursor:pointer; padding: 4px 8px; border:1px solid #ccc; border-radius:4px; background: #fff; font-size: 12px;">✏️ Editar</button>
                        <button onclick="eliminarItem(${it.id_det_plan})" style="cursor:pointer; padding: 4px 8px; border:1px solid #ffcccc; border-radius:4px; background: #ffe6e6; color: #d9534f; font-size: 12px; margin-left: 5px;">🗑️ Eliminar</button>
                    </div>
                </div>
            </div>`;
        });

        const tieneTransporte = items.some(it => it.tipo_item === 'TRANSPORTE' || it.tipo_item === 'TRANSPORTE_PROPIO');
        const badgeT = tieneTransporte
            ? `<span style="background: #fff3cd; color: #856404; font-size: 13px; padding: 5px 12px; border-radius: 20px; font-weight:bold; display: inline-block; margin-left: 15px;">✓ Transporte OK</span>`
            : `<span style="background: #fff3cd; color: #d39e00; font-size: 13px; padding: 5px 12px; border-radius: 20px; font-weight:bold; display: inline-block; margin-left: 15px;">⚠️ Falta Transporte</span>`;

        // Aquí inyectamos el HTML EXACTO a tu primera captura
        cont.innerHTML += `
            <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 10px; padding: 25px; margin-bottom: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <h2 style="margin: 0 0 10px 0; font-size: 32px; font-weight: 900; color: #000;">${plan.nombre_plan}</h2>
                        <div style="color: #666; font-size: 15px; display: flex; align-items: center;">
                            🗓️ Del ${plan.fecha_inicio} al ${plan.fecha_fin} 
                            ${badgeT}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: #666; font-size: 14px;">Presupuesto</div>
                        <div style="color: #28a745; font-size: 26px; font-weight: bold;">$${totalPlan.toLocaleString()} COP</div>
                    </div>
                </div>

                <div style="margin-top: 15px; margin-bottom: 25px;">
                    <button onclick="editarPlan(${plan.id_plan_viaje}, '${plan.nombre_plan}')" style="cursor:pointer; padding: 8px 18px; background: #fff; border: 1px solid #ccc; border-radius: 20px; font-weight: bold; margin-right: 8px;">✏️ Editar Nombre</button>
                    <button onclick="abrirModalOrigenDestino(${plan.id_plan_viaje}, ${plan.id_ubicacion_origen || 'null'}, ${plan.id_ubicacion_destino || 'null'})" style="cursor:pointer; padding: 8px 18px; background: #fff; border: 1px solid #ccc; border-radius: 20px; font-weight: bold; margin-right: 8px;">📍 Origen/Destino</button>
                    <button onclick="eliminarPlan(${plan.id_plan_viaje})" style="cursor:pointer; padding: 8px 18px; background: #ffe6e6; border: 1px solid #ffcccc; color: #d9534f; border-radius: 20px; font-weight: bold;">🗑️ Eliminar Plan</button>
                </div>

                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">

                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h4 style="margin: 0; font-size: 16px;">🗺️ Mapa del Trayecto:</h4>
                    <span id="ruta-info-${plan.id_plan_viaje}" style="font-size: 14px; color: #d9534f; font-weight: bold;">⏳ Calculando...</span>
                </div>
                <div id="map-plan-${plan.id_plan_viaje}" style="height: 300px; width: 100%; border-radius: 8px; border: 1px solid #ccc; z-index: 1;"></div>

                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">

                <h4 style="margin-bottom: 15px; font-size: 16px;">📌 Itinerario y Servicios:</h4>
                ${itemsHTML !== "" ? itemsHTML : "<p style='color:#666;'>No hay servicios agregados todavía.</p>"}

                <div style="display: flex; justify-content: flex-end; gap: 15px; margin-top: 25px;">
                    <button onclick="window.print()" style="cursor:pointer; padding: 12px 20px; border: 1px solid #ccc; background: #fff; border-radius: 6px; font-weight: bold;">🖨️ Imprimir Itinerario</button>
                    <button onclick="window.location.href='crear_plan.html?planId=${plan.id_plan_viaje}'" style="cursor:pointer; padding: 12px 20px; background: #007bff; color: white; border: none; border-radius: 6px; font-weight: bold;">+ Agregar más servicios</button>
                </div>

            </div>`;
    });

    document.getElementById("granTotal").textContent = `$${sumaTotal.toLocaleString()} COP`;
    setTimeout(() => { inicializarMapasDePlanes(planes); }, 200);
}

// =====================================
// FUNCIONES DE EDICIÓN Y ELIMINACIÓN DE PLAN Y SERVICIOS
// =====================================
async function eliminarPlan(idPlan) {
    if(!confirm("¿Estás seguro de eliminar todo el plan de viaje?")) return;
    try {
        const res = await fetch(`${API_URL}/planes-viaje/${idPlan}`, { method: "DELETE", headers: { "Authorization": `Bearer ${token}` }});
        if(res.ok) cargarMisPlanes(); else alert("Error al eliminar.");
    } catch(e) { console.error(e); }
}

async function editarPlan(idPlan, nombreActual) {
    const nuevoNombre = prompt("Nuevo nombre del plan:", nombreActual);
    if (!nuevoNombre) return;
    try {
        const res = await fetch(`${API_URL}/planes-viaje/${idPlan}`, {
            method: "PUT", headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
            body: JSON.stringify({ nombre_plan: nuevoNombre })
        });
        if(res.ok) cargarMisPlanes(); else alert("Error al actualizar el plan.");
    } catch(e) { console.error(e); }
}

let idItemEditando = null;

function editarItem(idDetPlan, cantActual, tipoItem, fechaActual) {
    idItemEditando = idDetPlan;
    document.getElementById("editCantidad").value = cantActual;
    document.getElementById("editFecha").value = fechaActual;
    const esHospedaje = tipoItem === "HOSPEDAJE";
    document.getElementById("campoPersonasEdit").style.display = esHospedaje ? "block" : "none";
    const labels = { HOSPEDAJE: "Cantidad de noches:", GASTRONOMIA: "Cantidad de platos:", TRANSPORTE: "Cantidad de pasajeros:" };
    document.getElementById("labelCantidadEdit").innerHTML = `<b>${labels[tipoItem] || "Cantidad de personas:"}</b>`;
    document.getElementById("modalEditar").style.display = "flex";
}

function cerrarModalEditar() {
    document.getElementById("modalEditar").style.display = "none";
    idItemEditando = null;
}

document.getElementById("formEditarItem").addEventListener("submit", async (e) => {
    e.preventDefault();
    const body = {
        cantidad: parseInt(document.getElementById("editCantidad").value),
        fecha_servicio: document.getElementById("editFecha").value
    };
    if (document.getElementById("campoPersonasEdit").style.display === "block") {
        body.personas = parseInt(document.getElementById("editPersonas").value);
    }
    try {
        const res = await fetch(`${API_URL}/planes-viaje/items/${idItemEditando}`, {
            method: "PUT", headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
            body: JSON.stringify(body)
        });
        if (res.ok) { cerrarModalEditar(); cargarMisPlanes(); }
        else alert("Error al actualizar.");
    } catch (err) { console.error(err); }
});

async function eliminarItem(idDetPlan) {
    if(!confirm("¿Deseas quitar este servicio del itinerario?")) return;
    try {
        const res = await fetch(`${API_URL}/planes-viaje/items/${idDetPlan}`, { method: "DELETE", headers: { "Authorization": `Bearer ${token}` }});
        if(res.ok) cargarMisPlanes(); else alert("Error al eliminar ítem.");
    } catch(e) { console.error(e); }
}

// =====================================
// MODAL DE ORÍGEN Y DESTINO
// =====================================
let idPlanEditandoUbicacion = null;
let ubicacionesCacheMapa = null;

async function obtenerUbicacionesParaMapa() {
    if (ubicacionesCacheMapa) return ubicacionesCacheMapa;
    try {
        const res = await fetch(`${API_URL}/ubicaciones/`);
        ubicacionesCacheMapa = res.ok ? await res.json() : [];
    } catch (e) { ubicacionesCacheMapa = []; }
    return ubicacionesCacheMapa;
}

async function abrirModalOrigenDestino(idPlan, oriActual, desActual) {
    idPlanEditandoUbicacion = idPlan;
    const ubicaciones = await obtenerUbicacionesParaMapa();
    const selOri = document.getElementById("selOrigenPlan");
    const selDes = document.getElementById("selDestinoPlan");
    
    const opciones = ubicaciones.map(u => `<option value="${u.id_ubi}">${u.direccion} (${u.barrio || u.ciudad || ''})</option>`).join("");
    
    selOri.innerHTML = `<option value="">-- Selecciona --</option>` + opciones;
    selDes.innerHTML = `<option value="">-- Selecciona --</option>` + opciones;
    
    if (oriActual) selOri.value = oriActual;
    if (desActual) selDes.value = desActual;
    
    document.getElementById("modalOrigenDestino").style.display = "flex";
}

async function guardarOrigenDestino() {
    const idOri = document.getElementById("selOrigenPlan").value;
    const idDes = document.getElementById("selDestinoPlan").value;
    if (!idOri || !idDes) { alert("Selecciona origen y destino."); return; }
    try {
        const res = await fetch(`${API_URL}/planes-viaje/${idPlanEditandoUbicacion}`, {
            method: "PUT", headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
            body: JSON.stringify({ id_ubicacion_origen: parseInt(idOri), id_ubicacion_destino: parseInt(idDes) })
        });
        if (res.ok) {
            document.getElementById("modalOrigenDestino").style.display = "none";
            cargarMisPlanes(); // Recargamos para actualizar el mapa
        } else alert("Error al guardar origen y destino.");
    } catch(e) { console.error(e); }
}

// =====================================
// MAPAS Y DIBUJO DE RUTAS
// =====================================
async function inicializarMapasDePlanes(planes) {
    const ubicaciones = await obtenerUbicacionesParaMapa();
    const coordsDefault = [4.6534, -74.1162]; // Bogotá por defecto

    planes.forEach(plan => {
        const mapEl = document.getElementById(`map-plan-${plan.id_plan_viaje}`);
        if (!mapEl) return;
        
        const map = L.map(`map-plan-${plan.id_plan_viaje}`, { scrollWheelZoom: false }).setView(coordsDefault, 6);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

        const infoSpan = document.getElementById(`ruta-info-${plan.id_plan_viaje}`);

        if (!plan.id_ubicacion_origen || !plan.id_ubicacion_destino) {
            L.marker(coordsDefault).addTo(map).bindPopup("Sin origen/destino definidos");
            if (infoSpan) infoSpan.innerHTML = `<span style="color:#d9534f;">⚠️ Define el origen y destino del viaje (botón 📍 arriba)</span>`;
            return;
        }

        const ori = ubicaciones.find(u => u.id_ubi === plan.id_ubicacion_origen);
        const des = ubicaciones.find(u => u.id_ubi === plan.id_ubicacion_destino);

        if (!ori || !des) {
            if (infoSpan) infoSpan.innerHTML = `<span style="color:#d9534f;">⚠️ No se encontraron las ubicaciones</span>`;
            return;
        }

        const oriC = [parseFloat(ori.latitud), parseFloat(ori.longitud)];
        const desC = [parseFloat(des.latitud), parseFloat(des.longitud)];

        const itemTransporte = (plan.items_agregados || []).find(
            it => it.tipo_item === 'TRANSPORTE' || it.tipo_item === 'TRANSPORTE_PROPIO'
        );
        const esVuelo = itemTransporte ? /avi[oó]n|vuelo|airbus|boeing/i.test(itemTransporte.observaciones || "") : false;

        if (esVuelo) {
            L.polyline([oriC, desC], { color: "#0ea5e9", weight: 4, dashArray: "10, 10" }).addTo(map);
            L.marker(oriC).addTo(map).bindPopup(`Origen: ${ori.direccion}`);
            L.marker(desC).addTo(map).bindPopup(`Destino: ${des.direccion}`);
            map.fitBounds(L.latLngBounds([oriC, desC]), { padding: [30, 30] });

            const R = 6371; const toR = d => d * Math.PI / 180;
            const a = Math.sin(toR(desC[0]-oriC[0])/2)**2 + Math.cos(toR(oriC[0]))*Math.cos(toR(desC[0]))*Math.sin(toR(desC[1]-oriC[1])/2)**2;
            const distKm = Math.round(R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)));
            const tMin = Math.round((distKm / 800) * 60);
            if (infoSpan) infoSpan.innerHTML = `✈️ Vuelo Directo: <b>${distKm} km</b> | ⏱️ <b>${Math.floor(tMin/60)}h ${tMin%60}min</b>`;
        } else {
            if (L.Routing) {
                L.Routing.control({
                    waypoints: [ L.latLng(oriC[0], oriC[1]), L.latLng(desC[0], desC[1]) ],
                    routeWhileDragging: false, addWaypoints: false, show: false,
                    createMarker: function(i, wp) { return L.marker(wp.latLng).bindPopup(i===0 ? `Origen: ${ori.direccion}` : `Destino: ${des.direccion}`); },
                    lineOptions: { styles: [{ color: '#007bff', opacity: 0.8, weight: 5 }] }
                }).on('routesfound', function(e) {
                    const distKm = Math.round(e.routes[0].summary.totalDistance / 1000);
                    const tMin = Math.round(e.routes[0].summary.totalTime / 60);
                    if (infoSpan) infoSpan.innerHTML = `🚗 Vía Terrestre: <b style="color: #000;">${distKm} km</b> | ⏱️ <b style="color: #000;">${Math.floor(tMin/60)}h ${tMin%60}min</b>`;
                }).addTo(map);
            }
        }
    });
}
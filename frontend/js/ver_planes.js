const API_URL = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");
let planesGlobal = [];

document.addEventListener("DOMContentLoaded", () => {
    if (!token) { window.location.href = "../login.html"; return; }
    cargarMisPlanes();
});

function irA(destino) { window.location.href = destino; }
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

    if (!planes || planes.length === 0) {
        cont.innerHTML = `<div style="text-align:center; padding:40px; background:#fff; border-radius:12px; border:1px dashed #cbd5e1;">Aún no tienes viajes creados.</div>`;
        return;
    }

    let sumaTotal = 0; let proximaFecha = null;

    planes.forEach(plan => {
        const totalPlan = Number(plan.costo_total_estimado) || 0;
        sumaTotal += totalPlan;

        let itemsHTML = "";
        const items = plan.items_agregados || [];

        items.forEach(it => {
            const desc = it.observaciones || it.tipo_item;
            const sub = Number(it.subtotal_calculado || 0).toLocaleString();
            let tiempoTxt = "";
            if (it.tiempo_estimado_min > 0) {
                const h = Math.floor(it.tiempo_estimado_min / 60); const m = it.tiempo_estimado_min % 60;
                tiempoTxt = ` | ⏱️ ${h > 0 ? h + 'h ' : ''}${m}m`;
            }
            itemsHTML += `<div class="item-chip" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px; margin-bottom:8px; display:flex; justify-content:space-between;">
                            <div><strong style="color:#0ea5e9;">[${it.tipo_item}]</strong> ${desc} <div style="font-size:11px; color:#64748b;">📅 ${it.fecha_servicio} | Cant: ${it.cantidad}${tiempoTxt}</div></div>
                            <div style="font-weight:bold; color:#16a34a;">+$${sub}</div>
                          </div>`;
        });

        const tieneTransporte = items.some(it => it.tipo_item === 'TRANSPORTE' || it.tipo_item === 'TRANSPORTE_PROPIO');

        cont.innerHTML += `
            <article class="plan-card" style="background:white; border:1px solid #e2e8f0; border-radius:16px; padding:24px; margin-bottom:24px; box-shadow:0 2px 10px rgba(0,0,0,0.04);">
                <div style="display:flex; justify-content:space-between; margin-bottom:16px;">
                    <div><h3 style="font-size:20px; font-weight:800; color:#0f172a;">${plan.nombre_plan}</h3>
                    <div style="font-size:13px; color:#64748b; margin-top:4px;">🗓️ Del ${plan.fecha_inicio} al ${plan.fecha_fin}</div></div>
                    <div style="text-align:right;"><div style="font-size:12px; color:#64748b;">Presupuesto</div><div style="font-size:22px; font-weight:800; color:#16a34a;">$${totalPlan.toLocaleString()} COP</div></div>
                </div>

                <div style="padding:16px; border-bottom:1px solid #e2e8f0;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;"><h4 style="font-size:13px; font-weight:700;">🗺️ Mapa del Trayecto:</h4><span id="ruta-info-${plan.id_plan_viaje}" style="font-size:12px; font-weight:600; color:#2563eb;">⏳ Calculando...</span></div>
                    <div id="map-plan-${plan.id_plan_viaje}" style="height: 220px; width: 100%; border-radius: 10px; border: 1px solid #cbd5e1; z-index: 1;"></div>
                </div>

                <div style="margin-top:16px;">
                    <h4 style="font-size:14px; font-weight:700; margin-bottom:12px;">📌 Itinerario y Servicios:</h4>
                    ${itemsHTML}
                </div>
            </article>`;
    });

    setTimeout(() => { inicializarMapasDePlanes(planes); }, 100);
}

function inicializarMapasDePlanes(planes) {
    if (typeof L === "undefined") return;

    // Coordenadas fijas por defecto (Si no quieres leerlas del backend)
    const coords = { bogota: [4.6534, -74.1162], medellin: [6.2084, -75.5678], cartagena: [10.4222, -75.5392] };

    planes.forEach(plan => {
        const mapId = `map-plan-${plan.id_plan_viaje}`;
        const mapEl = document.getElementById(mapId);
        if (!mapEl) return;

        const map = L.map(mapId, { scrollWheelZoom: false }).setView(coords.bogota, 6);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: '&copy; OpenStreetMap' }).addTo(map);

        let origenCoord = coords.bogota; let destinoCoord = coords.cartagena; let destinoNombre = "Cartagena";
        const nom = (plan.nombre_plan || "").toLowerCase();
        if (nom.includes("medellin") || nom.includes("medellín")) { destinoCoord = coords.medellin; destinoNombre = "Medellín"; }

        // BUSCAR SI HAY AVIÓN
        let esVuelo = false;
        let tieneTransporte = false;
        (plan.items_agregados || []).forEach(it => {
            if (it.tipo_item === 'TRANSPORTE_PROPIO') tieneTransporte = true;
            if (it.tipo_item === 'TRANSPORTE') {
                tieneTransporte = true;
                if (/avi[oó]n|vuelo|airbus|boeing|avianca/i.test(it.observaciones || "")) esVuelo = true;
            }
        });

        const infoSpan = document.getElementById(`ruta-info-${plan.id_plan_viaje}`);

        if (esVuelo) {
            // LÍNEA RECTA PUNTEADA (AVIÓN)
            L.polyline([origenCoord, destinoCoord], { color: "#0ea5e9", weight: 4, dashArray: "10, 10" }).addTo(map);
            L.marker(origenCoord).addTo(map).bindPopup(`Bogotá (Aeropuerto)`); L.marker(destinoCoord).addTo(map).bindPopup(`${destinoNombre} (Aeropuerto)`);
            map.fitBounds(L.latLngBounds([origenCoord, destinoCoord]), { padding: [30, 30] });

            // Haversine exacto
            const R = 6371; const toR = d => d*Math.PI/180;
            const a = Math.sin(toR(destinoCoord[0]-origenCoord[0])/2)**2 + Math.cos(toR(origenCoord[0]))*Math.cos(toR(destinoCoord[0]))*Math.sin(toR(destinoCoord[1]-origenCoord[1])/2)**2;
            const distKm = Math.round(R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)));
            const tMin = Math.round((distKm / 800) * 60);
            if (infoSpan) infoSpan.innerHTML = `✈️ Vuelo Directo: <b>${distKm} km</b> | ⏱️ <b>${Math.floor(tMin/60)}h ${tMin%60}min</b>`;
        } else if (tieneTransporte) {
            // RUTAS REALES POR CALLES (CARRO / BUS)
            if(L.Routing) {
                L.Routing.control({
                    waypoints: [ L.latLng(origenCoord[0], origenCoord[1]), L.latLng(destinoCoord[0], destinoCoord[1]) ],
                    routeWhileDragging: false, addWaypoints: false, show: false,
                    createMarker: function(i, wp) { return L.marker(wp.latLng).bindPopup(i===0 ? `Origen` : `Destino`); },
                    lineOptions: { styles: [{ color: '#2563eb', opacity: 0.9, weight: 5 }] }
                }).on('routesfound', function(e) {
                    const distKm = Math.round(e.routes[0].summary.totalDistance / 1000); 
                    const tMin = Math.round(e.routes[0].summary.totalTime / 60); 
                    if (infoSpan) infoSpan.innerHTML = `🚗 Vía Terrestre: <b>${distKm} km</b> | ⏱️ <b>${Math.floor(tMin/60)}h ${tMin%60}min</b>`;
                }).addTo(map);
            }
        } else {
            L.marker(origenCoord).addTo(map); L.marker(destinoCoord).addTo(map);
            if (infoSpan) infoSpan.innerHTML = `<span style="color:#ef4444;">⚠️ Agrega transporte</span>`;
        }
    });
}
function obtenerIcono(tipo) { const m = { "HOSPEDAJE": "🏨", "GASTRONOMIA": "🍽️", "RECREACION": "🏖️", "DESTINO_TURISTICO": "🏖️", "TRANSPORTE": "🚌", "GUIA": "🗺️", "TRANSPORTE_PROPIO": "🚗" }; return m[tipo] || "📌"; }
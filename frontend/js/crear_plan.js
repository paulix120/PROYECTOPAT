const API_URL = "http://127.0.0.1:8000";
let idPlanActual = null;
let token = localStorage.getItem("token");

let opcionesActualesFormulario = [];
let misPlanesGuardados = [];
let ubicacionesList = [];

let tieneTransporteEnPlan = false;
let mapaCrearPlanInstance = null;
let controlRuta = null; 

document.addEventListener("DOMContentLoaded", () => {
    if (!token) { window.location.href = "../login.html"; return; }
    document.getElementById("crearPlanForm").addEventListener("submit", crearPlanBase);
    document.getElementById("agregarItemForm").addEventListener("submit", agregarItemAlPlan);
    document.getElementById("filtroOpcionesPlan").addEventListener("input", (e) => renderizarSelectPlan(e.target.value));
    
    document.getElementById("itemEspecifico").addEventListener("change", (e) => {
        const tipo = document.getElementById("tipoServicio").value;
        if (tipo === "TRANSPORTE") {
            const opt = e.target.options[e.target.selectedIndex];
            if(opt && opt.value) {
                const ori = opt.getAttribute("data-origen");
                const des = opt.getAttribute("data-destino");
                const vehiculo = opt.getAttribute("data-vehiculo") || "";
                if(ori && des && ori !== "null" && des !== "null") {
                    document.getElementById("origenSelect").value = ori;
                    document.getElementById("destinoSelect").value = des;
                    actualizarMapaEnVivo(vehiculo);
                }
            }
        }
    });

    cargarUbicaciones();
    cargarMisPlanesExistentes();
});

async function cargarMisPlanesExistentes() {
    try {
        const res = await fetch(`${API_URL}/planes-viaje/mis-planes`, { headers: { "Authorization": `Bearer ${token}` } });
        if (res.ok) {
            misPlanesGuardados = await res.json();
            const sel = document.getElementById("selectMisPlanesExistentes");
            misPlanesGuardados.forEach(p => sel.innerHTML += `<option value="${p.id_plan_viaje}">${p.nombre_plan}</option>`);

            // Capturar ID de URL si venimos del botón "Agregar más servicios"
            const urlParams = new URLSearchParams(window.location.search);
            const planIdURL = urlParams.get('planId');
            if (planIdURL) {
                sel.value = planIdURL;
                seleccionarPlanExistente(planIdURL);
            }
        }
    } catch (e) {}
}

function seleccionarPlanExistente(idPlanStr) {
    if (!idPlanStr) return;
    const plan = misPlanesGuardados.find(p => p.id_plan_viaje === parseInt(idPlanStr));
    if (plan) {
        idPlanActual = plan.id_plan_viaje;
        document.getElementById("seccionPlanBase").style.display = "none";
        document.getElementById("seccionItems").style.display = "block";
        document.getElementById("tituloPlanActivo").textContent = plan.nombre_plan;
        
        let tieneT = false;
        const ul = document.getElementById("listaResumen"); ul.innerHTML = "";
        (plan.items_agregados || []).forEach(it => {
            if(it.tipo_item === "TRANSPORTE" || it.tipo_item === "TRANSPORTE_PROPIO") tieneT = true;
            ul.innerHTML += `<li>${it.fecha_servicio} | [${it.tipo_item}] ${it.observaciones || ''} -> $${Number(it.subtotal_calculado).toLocaleString()}</li>`;
        });
        document.getElementById("costoTotal").innerText = Number(plan.costo_total_estimado).toLocaleString();
        
        tieneTransporteEnPlan = tieneT;
        document.getElementById("estadoTransporteBadge").innerHTML = tieneT ? "<span style='color:#16a34a;'>✓ Transporte Confirmado</span>" : "<span style='color:#dc2626;'>❌ Transporte Pendiente</span>";
    }
}

function cambiarDePlan() {
    idPlanActual = null;
    document.getElementById("seccionPlanBase").style.display = "block";
    document.getElementById("seccionItems").style.display = "none";
    document.getElementById("listaResumen").innerHTML = "";
    document.getElementById("costoTotal").textContent = "0.00";
    window.history.replaceState(null, '', 'crear_plan.html'); // Limpiar la URL
}

async function crearPlanBase(e) {
    e.preventDefault();
    try {
        const res = await fetch(`${API_URL}/planes-viaje/`, {
            method: "POST", headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
            body: JSON.stringify({ nombre_plan: document.getElementById("nombrePlan").value, fecha_inicio: document.getElementById("fechaInicio").value, fecha_fin: document.getElementById("fechaFin").value })
        });
        const data = await res.json();
        if (res.ok) { 
            idPlanActual = data.id_plan_viaje; 
            document.getElementById("seccionPlanBase").style.display = "none"; 
            document.getElementById("seccionItems").style.display = "block"; 
        }
        else alert(data.detail);
    } catch (error) {}
}

async function cargarUbicaciones() {
    try {
        const res = await fetch(`${API_URL}/ubicaciones/`);
        if(res.ok) {
            ubicacionesList = await res.json();
            const selOri = document.getElementById("origenSelect"); const selDes = document.getElementById("destinoSelect");
            selOri.innerHTML = ""; selDes.innerHTML = "";
            ubicacionesList.forEach(u => {
                selOri.innerHTML += `<option value="${u.id_ubi}">${u.direccion} (${u.barrio || u.ciudad || ''})</option>`;
                selDes.innerHTML += `<option value="${u.id_ubi}">${u.direccion} (${u.barrio || u.ciudad || ''})</option>`;
            });
        }
    } catch (e) {}
}

async function cargarOpcionesServicio() {
    const tipo = document.getElementById("tipoServicio").value;
    const gEstandar = document.getElementById("grupoEstandar");
    const gMapa = document.getElementById("grupoGasolina");

    if (tipo === "TRANSPORTE_PROPIO") {
        gEstandar.style.display = "none"; gMapa.style.display = "block";
        setTimeout(() => actualizarMapaEnVivo("carro propio"), 100); return;
    } else if (tipo === "TRANSPORTE") {
        gEstandar.style.display = "block"; gMapa.style.display = "block";
    } else {
        gEstandar.style.display = "block"; gMapa.style.display = "none";
    }
    
    opcionesActualesFormulario = [];
    document.getElementById("itemEspecifico").innerHTML = '<option value="">Cargando...</option>';

    try {
        let ep = tipo === "HOSPEDAJE" ? "hospedajes" : (tipo === "GASTRONOMIA" ? "gastronomia/restaurantes" : (tipo === "TRANSPORTE" ? "transporte/" : "recreacion/"));
        const res = await fetch(`${API_URL}/servicios/${ep}`);
        const data = await res.json();
        
        if (tipo === "HOSPEDAJE") data.forEach(h => (h.habitaciones_disponibles || []).forEach(hab => opcionesActualesFormulario.push({ val: hab.id_hosp, padre: h.id_servicio, texto: `${h.nombre} - ${hab.nom_unidad}` })));
        else if (tipo === "GASTRONOMIA") data.forEach(r => (r.menu_disponible || []).forEach(p => opcionesActualesFormulario.push({ val: p.id_gast, padre: r.id_servicio, texto: `${r.nombre} - ${p.nom_platillo_menu}` })));
        else data.forEach(item => {
            const h = item.detalle;
            opcionesActualesFormulario.push({ 
                val: h.id_trans || h.id_rec, 
                padre: item.servicio_base.id_servicio, 
                texto: `${item.servicio_base.nombre} - ${h.tipo_vehiculo || h.nom_actividad}`,
                idOri: h.id_origen, idDes: h.id_destino, vehiculo: h.tipo_vehiculo || ""
            });
        });
        renderizarSelectPlan("");
    } catch (e) {}
}

function renderizarSelectPlan(filtro) {
    const sel = document.getElementById("itemEspecifico");
    sel.innerHTML = '<option value="">-- Elige una opción --</option>';
    const term = (filtro || "").toLowerCase();
    opcionesActualesFormulario.forEach(opt => {
        if (opt.texto.toLowerCase().includes(term)) {
            sel.innerHTML += `<option value="${opt.val}" data-id-servicio="${opt.padre}" data-origen="${opt.idOri}" data-destino="${opt.idDes}" data-vehiculo="${opt.vehiculo}">${opt.texto}</option>`;
        }
    });
}

function actualizarMapaEnVivo(tipoVehiculoStr = "carro") {
    if (typeof L === "undefined") return;
    const idOri = parseInt(document.getElementById("origenSelect").value);
    const idDes = parseInt(document.getElementById("destinoSelect").value);
    const ori = ubicacionesList.find(u => u.id_ubi === idOri);
    const des = ubicacionesList.find(u => u.id_ubi === idDes);
    if(!ori || !des) return;

    if (!mapaCrearPlanInstance) {
        mapaCrearPlanInstance = L.map("mapaCrearPlan").setView([4.6534, -74.1162], 6);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(mapaCrearPlanInstance);
    } else mapaCrearPlanInstance.invalidateSize();

    if (controlRuta) mapaCrearPlanInstance.removeControl(controlRuta);
    mapaCrearPlanInstance.eachLayer((layer) => { if(layer instanceof L.Marker || layer instanceof L.Polyline) mapaCrearPlanInstance.removeLayer(layer); });

    const esVuelo = /avi[oó]n|vuelo|airbus|boeing/i.test(tipoVehiculoStr);
    document.getElementById("infoRutaCalculada").innerHTML = "⏳ Calculando ruta...";

    if(esVuelo) {
        L.polyline([[ori.latitud, ori.longitud], [des.latitud, des.longitud]], { color: "#0ea5e9", weight: 4, dashArray: "10, 10" }).addTo(mapaCrearPlanInstance);
        L.marker([ori.latitud, ori.longitud]).addTo(mapaCrearPlanInstance).bindPopup(`<b>Origen:</b> ${ori.direccion}`);
        L.marker([des.latitud, des.longitud]).addTo(mapaCrearPlanInstance).bindPopup(`<b>Destino:</b> ${des.direccion}`);
        mapaCrearPlanInstance.fitBounds(L.latLngBounds([[ori.latitud, ori.longitud], [des.latitud, des.longitud]]), { padding: [30, 30] });

        const dKm = Math.round(6371 * 2 * Math.asin(Math.sqrt(Math.sin((des.latitud-ori.latitud)*Math.PI/360)**2 + Math.cos(ori.latitud*Math.PI/180)*Math.cos(des.latitud*Math.PI/180)*Math.sin((des.longitud-ori.longitud)*Math.PI/360)**2)));
        const tM = Math.round((dKm / 800) * 60); 
        document.getElementById("infoRutaCalculada").innerHTML = `✈️ Vuelo Directo: <strong>${dKm} km</strong> | ⏱️ <strong>${Math.floor(tM/60)}h ${tM%60}min</strong>`;
    } else {
        controlRuta = L.Routing.control({
            waypoints: [ L.latLng(ori.latitud, ori.longitud), L.latLng(des.latitud, des.longitud) ],
            routeWhileDragging: false, addWaypoints: false, show: false,
            createMarker: function(i, wp) { return L.marker(wp.latLng).bindPopup(i===0 ? `Origen` : `Destino`); },
            lineOptions: { styles: [{ color: '#2563eb', opacity: 0.9, weight: 5 }] }
        }).on('routesfound', function(e) {
            const dKm = Math.round(e.routes[0].summary.totalDistance / 1000);
            const tM = Math.round(e.routes[0].summary.totalTime / 60);
            const gas = document.getElementById("tipoServicio").value === "TRANSPORTE_PROPIO" ? ` | ⛽ $${(dKm*450).toLocaleString()} COP` : '';
            document.getElementById("infoRutaCalculada").innerHTML = `🚗 Distancia Vía: <strong>${dKm} km</strong> | ⏱️ <strong>${Math.floor(tM/60)}h ${tM%60}min</strong>${gas}`;
        }).addTo(mapaCrearPlanInstance);
    }
}

async function agregarItemAlPlan(e) {
    e.preventDefault();
    const tipo = document.getElementById("tipoServicio").value;
    let payload = { tipo_item: tipo, cantidad: parseInt(document.getElementById("cantidadItem").value), fecha_servicio: document.getElementById("fechaServicio").value, observaciones: "" };

    if (tipo === "TRANSPORTE_PROPIO") {
        payload.id_ubicacion_origen = parseInt(document.getElementById("origenSelect").value);
        payload.id_ubicacion_destino = parseInt(document.getElementById("destinoSelect").value);
        payload.observaciones = "Viajar en Carro Propio";
        tieneTransporteEnPlan = true;
    } else {
        const opt = document.getElementById("itemEspecifico").options[document.getElementById("itemEspecifico").selectedIndex];
        payload.id_item_especifico = parseInt(opt.value);
        payload.id_servicio = parseInt(opt.getAttribute("data-id-servicio")) || null;
        payload.observaciones = opt.text;
        if (tipo === "TRANSPORTE") tieneTransporteEnPlan = true;
    }

    try {
        const res = await fetch(`${API_URL}/planes-viaje/${idPlanActual}/items`, {
            method: "POST", headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` }, body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
            document.getElementById("costoTotal").innerText = Number(data.NUEVO_TOTAL).toLocaleString();
            document.getElementById("listaResumen").innerHTML += `<li>${payload.fecha_servicio} | ${payload.observaciones} -> $${Number(data.subtotal).toLocaleString()}</li>`;
            document.getElementById("estadoTransporteBadge").innerHTML = tieneTransporteEnPlan ? "<span style='color:#16a34a;'>✓ Confirmado</span>" : "<span style='color:#dc2626;'>❌ Pendiente</span>";
        } else alert(data.detail);
    } catch (error) {}
}

function finalizarPlanConValidacion() {
    if (!tieneTransporteEnPlan) { alert("⚠️ OBLIGATORIO: Debes agregar un transporte."); return; }
    window.location.href = "ver_planes.html";
}
function cerrarSesion() { localStorage.clear(); window.location.href = "../login.html"; }   
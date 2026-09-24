const API_URL = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");

let todosLosServicios = [];
let idPlanActual = null;
let opcionesActualesFormulario = [];

document.addEventListener("DOMContentLoaded", () => {
    if (!token) {
        alert("Debes iniciar sesión primero.");
        const enSubcarpeta = window.location.pathname.includes("/menu_usuario/");
        window.location.href = enSubcarpeta ? "../login.html" : "login.html";
        return;
    }

    const userName = localStorage.getItem("userName") || "Usuario Normal";
    const nombreEl = document.getElementById("nombreUsuario");
    const avatarEl = document.getElementById("avatarLetras");
    if (nombreEl) nombreEl.textContent = userName;
    if (avatarEl) avatarEl.textContent = userName.substring(0, 2).toUpperCase();

    configurarNavegacion();
    cargarCatalogoServicios();
    
    const searchInput = document.getElementById("searchInput");
    if (searchInput) searchInput.addEventListener("input", filtrarCatalogo);
    
    const crearPlanForm = document.getElementById("crearPlanForm");
    if (crearPlanForm) crearPlanForm.addEventListener("submit", crearPlanBase);

    const tipoServicio = document.getElementById("tipoServicio");
    if (tipoServicio) tipoServicio.addEventListener("change", cargarOpcionesFormularioPlan);

    const filtroPlan = document.getElementById("filtroOpcionesPlan");
    if (filtroPlan) {
        filtroPlan.addEventListener("input", (e) => {
            renderizarOpcionesSelect(e.target.value);
        });
    }

    const agregarItemForm = document.getElementById("agregarItemForm");
    if (agregarItemForm) agregarItemForm.addEventListener("submit", agregarItemAlPlan);
});

function configurarNavegacion() {
    const botonesMenu = document.querySelectorAll("[data-view]");
    const vistas = document.querySelectorAll(".view");

    const titulos = {
        "inicio": ["Catálogo de Servicios", "Explora los mejores destinos, hoteles y más."],
        "detalle-servicio": ["Detalles del Servicio", "Información completa y opciones disponibles."],
        "crear-plan": ["Arma tu Plan de Viaje", "Crea tu carrito y agrega los servicios que desees."],
        "mis-viajes": ["Historial de Mis Viajes", "Tus planes creados y guardados en la plataforma."]
    };

    botonesMenu.forEach(boton => {
        boton.addEventListener("click", () => {
            const vistaSeleccionada = boton.dataset.view;
            cambiarVista(vistaSeleccionada, botonesMenu, vistas, titulos);
            if (vistaSeleccionada === "mis-viajes") cargarMisPlanes();
            if (vistaSeleccionada === "inicio") cargarCatalogoServicios();
        });
    });
}

function cambiarVista(idVista, botonesMenu, vistas, titulos) {
    if(!botonesMenu) botonesMenu = document.querySelectorAll("[data-view]");
    botonesMenu.forEach(item => item.classList.remove("active"));
    const btnActivo = document.querySelector(`[data-view="${idVista}"]`);
    if(btnActivo) btnActivo.classList.add("active");

    if(!vistas) vistas = document.querySelectorAll(".view");
    vistas.forEach(vista => vista.classList.remove("active"));
    const target = document.getElementById("view-" + idVista);
    if(target) target.classList.add("active");

    if(titulos && titulos[idVista]) {
        const titleEl = document.getElementById("header-title");
        const subEl = document.getElementById("header-subtitle");
        if(titleEl) titleEl.textContent = titulos[idVista][0];
        if(subEl) subEl.textContent = titulos[idVista][1];
    }
}

// ==========================================
// CATÁLOGO E IMÁGENES
// ==========================================
async function cargarCatalogoServicios() {
    try {
        const response = await fetch(`${API_URL}/servicios/`);
        if (!response.ok) throw new Error("Error al conectar con la API");
        todosLosServicios = await response.json();
        renderizarCatalogo(todosLosServicios);
    } catch (error) {
        console.error("Error cargando el catálogo:", error);
    }
}

function renderizarCatalogo(servicios) {
    const contRecreacion = document.getElementById("listaRecreacion");
    const contHospedaje = document.getElementById("listaHospedaje");
    const contGastronomia = document.getElementById("listaGastronomia");
    const contTransporte = document.getElementById("listaTransporte");
    const contGuias = document.getElementById("listaGuias");

    if (contRecreacion) contRecreacion.innerHTML = ""; 
    if (contHospedaje) contHospedaje.innerHTML = ""; 
    if (contGastronomia) contGastronomia.innerHTML = ""; 
    if (contTransporte) contTransporte.innerHTML = ""; 
    if (contGuias) contGuias.innerHTML = "";

    servicios.forEach(srv => {
        let imgSrc = 'https://via.placeholder.com/300x200?text=Sin+Imagen';
        if(srv.imagen_principal) {
            imgSrc = srv.imagen_principal.startsWith('http') ? srv.imagen_principal : API_URL + srv.imagen_principal;
        }

        const ubicacionStr = srv.ubicacion ? `${srv.ubicacion.direccion}, ${srv.ubicacion.barrio || ''}` : 'Ubicación no especificada';

        const cardHTML = `
            <div class="card clickable" onclick="verDetalleServicio(${srv.id_servicio}, ${srv.id_tp_serv})">
                <img src="${imgSrc}" alt="${srv.nombre}" class="card-img" onerror="this.src='https://via.placeholder.com/300x200?text=Sin+Imagen'">
                <div class="card-body">
                    <h4 style="color:#2563eb; margin-bottom:6px; font-size:15px;">${srv.nombre}</h4>
                    <p style="font-size:12px; color:#16a34a; font-weight:bold; margin-bottom:8px;">📍 ${ubicacionStr}</p>
                    <p style="font-size:13px; color:#64748b; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">${srv.descripcion}</p>
                </div>
            </div>
        `;
        
        if (srv.id_tp_serv === 3 && contRecreacion) contRecreacion.innerHTML += cardHTML;
        else if (srv.id_tp_serv === 1 && contHospedaje) contHospedaje.innerHTML += cardHTML;
        else if (srv.id_tp_serv === 2 && contGastronomia) contGastronomia.innerHTML += cardHTML;
        else if (srv.id_tp_serv === 4 && contTransporte) contTransporte.innerHTML += cardHTML;
        else if (srv.id_tp_serv === 5 && contGuias) contGuias.innerHTML += cardHTML;
    });
}

function filtrarCatalogo() {
    const query = document.getElementById("searchInput").value.toLowerCase();
    const filtrados = todosLosServicios.filter(srv => 
        srv.nombre.toLowerCase().includes(query) || 
        srv.descripcion.toLowerCase().includes(query) ||
        (srv.ubicacion && srv.ubicacion.direccion.toLowerCase().includes(query)) ||
        (srv.ubicacion && srv.ubicacion.barrio && srv.ubicacion.barrio.toLowerCase().includes(query))
    );
    renderizarCatalogo(filtrados);
}

// ==========================================
// VER DETALLES A FONDO
// ==========================================
async function verDetalleServicio(idServicio, idTipoServicio) {
    const srv = todosLosServicios.find(s => s.id_servicio === idServicio);
    if(!srv) return;

    const nombresTipos = {1: "Hospedaje", 2: "Gastronomía", 3: "Recreación", 4: "Transporte", 5: "Guía Turístico"};
    
    document.getElementById("detalleNombre").textContent = srv.nombre;
    document.getElementById("detalleCategoria").textContent = nombresTipos[idTipoServicio] || "Servicio";
    document.getElementById("detalleDescripcion").textContent = srv.descripcion;
    
    if(srv.ubicacion) {
        document.getElementById("detalleDireccion").textContent = srv.ubicacion.direccion;
        document.getElementById("detalleBarrio").textContent = srv.ubicacion.barrio || "No registrado";
        document.getElementById("detalleCP").textContent = srv.ubicacion.codigo_postal || "No registrado";
    } else {
        document.getElementById("detalleDireccion").textContent = "N/A";
        document.getElementById("detalleBarrio").textContent = "N/A";
        document.getElementById("detalleCP").textContent = "N/A";
    }

    const imgEl = document.getElementById("detalleImagen");
    if(srv.imagen_principal) {
        imgEl.src = srv.imagen_principal.startsWith('http') ? srv.imagen_principal : API_URL + srv.imagen_principal;
    } else {
        imgEl.src = "https://via.placeholder.com/300x200?text=Sin+Imagen";
    }

    const contenedorOpciones = document.getElementById("contenedorOpcionesServicio");
    const listaOpciones = document.getElementById("listaOpciones");
    const tituloOpciones = document.getElementById("tituloOpciones");
    
    contenedorOpciones.style.display = "none";
    listaOpciones.innerHTML = "";

    try {
        if (idTipoServicio === 1) { // Hospedaje
            const res = await fetch(`${API_URL}/servicios/hospedajes`);
            const hoteles = await res.json();
            const hotelActual = hoteles.find(h => h.id_servicio === idServicio);
            if (hotelActual && hotelActual.habitaciones_disponibles.length > 0) {
                tituloOpciones.textContent = "🏨 Habitaciones Disponibles";
                hotelActual.habitaciones_disponibles.forEach(hab => {
                    listaOpciones.innerHTML += `
                        <div class="list-row">
                            <div>
                                <strong style="font-size:15px; color:#0f172a;">${hab.nom_unidad}</strong>
                                <span style="display:block; margin-top:4px; font-size:13px; color:#64748b;">Capacidad: ${hab.capacidad_personas} personas | Check-in: ${hab.horario_checkin || 'N/A'}</span>
                            </div>
                            <span class="badge badge-success" style="font-size:14px; height:fit-content; padding: 8px 12px;">$${hab.vlr_noche} / noche</span>
                        </div>
                    `;
                });
                contenedorOpciones.style.display = "block";
            }
        } 
        else if (idTipoServicio === 2) { // Gastronomía
            const res = await fetch(`${API_URL}/servicios/gastronomia/restaurantes/${idServicio}`);
            const restaurante = await res.json();
            if (restaurante.menu_disponible && restaurante.menu_disponible.length > 0) {
                tituloOpciones.textContent = "🍽️ Menú del Restaurante";
                restaurante.menu_disponible.forEach(plato => {
                    listaOpciones.innerHTML += `
                        <div class="list-row">
                            <div>
                                <strong style="font-size:15px; color:#0f172a;">${plato.nom_platillo_menu}</strong>
                                <span style="display:block; margin-top:4px; font-size:13px; color:#64748b;">Porciones: ${plato.porciones}</span>
                            </div>
                            <span class="badge badge-success" style="font-size:14px; height:fit-content; padding: 8px 12px;">$${plato.vlr_estimado}</span>
                        </div>
                    `;
                });
                contenedorOpciones.style.display = "block";
            }
        }
        else if (idTipoServicio === 3 || idTipoServicio === 4 || idTipoServicio === 5) {
            let endpoint = "";
            if (idTipoServicio === 3) endpoint = "recreacion";
            if (idTipoServicio === 4) endpoint = "transporte";
            if (idTipoServicio === 5) endpoint = "guias";
            
            const res = await fetch(`${API_URL}/servicios/${endpoint}/`);
            const serviciosTipo = await res.json();
            const srvActual = serviciosTipo.find(s => s.servicio_base.id_servicio === idServicio);
            
            if (srvActual && srvActual.detalle) {
                const det = srvActual.detalle;
                tituloOpciones.textContent = "📌 Detalles Adicionales";
                
                let info = "";
                if(idTipoServicio === 3) info = `Actividad: ${det.nom_actividad} | Duración: ${det.duracion || 'N/A'}`;
                if(idTipoServicio === 4) info = `Vehículo: ${det.tipo_vehiculo} | Pasajeros: ${det.capacidad_pasajeros}`;
                if(idTipoServicio === 5) info = `Tour: ${det.nombre_tour} | Duración: ${det.duracion_horas}h | Dificultad: ${det.dificultad}`;

                let precio = det.vlr_persona || det.tarifa_base || det.vlr_tour || 0;

                listaOpciones.innerHTML = `
                    <div class="list-row">
                        <div>
                            <strong style="font-size:14px; color:#0f172a;">${info}</strong>
                            <span style="display:block; margin-top:4px; font-size:13px; color:#64748b;">Horario: ${det.horario || det.horario_servicio || 'N/A'}</span>
                        </div>
                        <span class="badge badge-success" style="font-size:14px; height:fit-content; padding: 8px 12px;">$${precio}</span>
                    </div>
                `;
                contenedorOpciones.style.display = "block";
            }
        }
    } catch (err) {
        console.error("Error al cargar detalles:", err);
    }

    const titulos = {"detalle-servicio": ["Detalles del Servicio", "Información completa y opciones disponibles."]};
    cambiarVista("detalle-servicio", document.querySelectorAll("[data-view]"), document.querySelectorAll(".view"), titulos);
}

function volverAlCatalogo() {
    const titulos = {"inicio": ["Catálogo de Servicios", "Explora los mejores destinos, hoteles y más."]};
    cambiarVista("inicio", document.querySelectorAll("[data-view]"), document.querySelectorAll(".view"), titulos);
}

// ==========================================
// CREAR PLAN Y MIS VIAJES
// ==========================================
async function crearPlanBase(e) {
    e.preventDefault();
    const nombrePlan = document.getElementById("nombrePlan").value;
    const fechaInicio = document.getElementById("fechaInicio").value;
    const fechaFin = document.getElementById("fechaFin").value;
    try {
        const response = await fetch(`${API_URL}/planes-viaje/`, {
            method: "POST",
            headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
            body: JSON.stringify({ nombre_plan: nombrePlan, fecha_inicio: fechaInicio, fecha_fin: fechaFin })
        });
        const data = await response.json();
        if (response.ok) {
            idPlanActual = data.id_plan_viaje;
            document.getElementById("seccionPlanBase").style.display = "none";
            document.getElementById("seccionPlanItems").style.display = "block";
            const inputFecha = document.getElementById("fechaServicio");
            inputFecha.min = fechaInicio; inputFecha.max = fechaFin; inputFecha.value = fechaInicio;
        } else alert(data.detail || "Error al crear el plan.");
    } catch (error) { console.error(error); alert("Error de conexión"); }
}

async function cargarOpcionesFormularioPlan() {
    const tipo = document.getElementById("tipoServicio").value;
    const select = document.getElementById("itemEspecifico");
    const filtroInput = document.getElementById("filtroOpcionesPlan");
    if(filtroInput) filtroInput.value = "";
    opcionesActualesFormulario = [];

    select.innerHTML = '<option value="">Cargando opciones...</option>';
    try {
        let endpoint = "";
        if (tipo === "HOSPEDAJE") endpoint = "/servicios/hospedajes";
        else if (tipo === "GASTRONOMIA") endpoint = "/servicios/gastronomia/restaurantes";
        else if (tipo === "TRANSPORTE") endpoint = "/servicios/transporte/";
        else if (tipo === "DESTINO_TURISTICO") endpoint = "/servicios/recreacion/";
        else { select.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>'; return; }

        const response = await fetch(`${API_URL}${endpoint}`);
        const data = await response.json();

        if (tipo === "HOSPEDAJE") {
            data.forEach(h => h.habitaciones_disponibles.forEach(hab => {
                opcionesActualesFormulario.push({
                    val: hab.id_hosp,
                    padre: h.id_servicio,
                    texto: `${h.nombre} - ${hab.nom_unidad} ($${hab.vlr_noche})`
                });
            }));
        } else if (tipo === "GASTRONOMIA") {
            data.forEach(r => r.menu_disponible.forEach(p => {
                opcionesActualesFormulario.push({
                    val: p.id_gast,
                    padre: r.id_servicio,
                    texto: `${r.nombre} - ${p.nom_platillo_menu} ($${p.vlr_estimado})`
                });
            }));
        } else if (tipo === "TRANSPORTE" || tipo === "DESTINO_TURISTICO") {
            data.forEach(item => {
                const p = item.servicio_base; const h = item.detalle;
                const nombreItem = tipo === "TRANSPORTE" ? h.tipo_vehiculo : h.nom_actividad;
                const precioItem = tipo === "TRANSPORTE" ? h.tarifa_base : h.vlr_persona;
                opcionesActualesFormulario.push({
                    val: h.id_trans || h.id_rec,
                    padre: p.id_servicio,
                    texto: `${p.nombre} - ${nombreItem} ($${precioItem})`
                });
            });
        }

        renderizarOpcionesSelect("");
    } catch (error) { 
        console.error(error);
        select.innerHTML = '<option value="">Error cargando opciones</option>'; 
    }
}

function renderizarOpcionesSelect(filtro) {
    const select = document.getElementById("itemEspecifico");
    select.innerHTML = '<option value="">-- Elige una opción --</option>';
    const term = (filtro || "").toLowerCase();

    opcionesActualesFormulario.forEach(opt => {
        if (opt.texto.toLowerCase().includes(term)) {
            select.innerHTML += `<option value="${opt.val}" data-padre="${opt.padre}">${opt.texto}</option>`;
        }
    });

    if (opcionesActualesFormulario.length > 0 && select.children.length === 1) {
        select.innerHTML += `<option value="" disabled>No se encontraron resultados para "${filtro}"</option>`;
    }
}

async function agregarItemAlPlan(e) {
    e.preventDefault();
    const select = document.getElementById("itemEspecifico");
    const option = select.options[select.selectedIndex];
    if(!option || !option.value) {
        alert("Por favor selecciona una opción válida.");
        return;
    }
    try {
        const response = await fetch(`${API_URL}/planes-viaje/${idPlanActual}/items`, {
            method: "POST",
            headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
            body: JSON.stringify({
                id_servicio: parseInt(option.getAttribute("data-padre")),
                tipo_item: document.getElementById("tipoServicio").value,
                id_item_especifico: parseInt(option.value),
                cantidad: parseInt(document.getElementById("cantidadItem").value),
                fecha_servicio: document.getElementById("fechaServicio").value,
                observaciones: ""
            })
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById("costoTotal").textContent = data.NUEVO_TOTAL;
            document.getElementById("listaResumen").innerHTML += `
                <div class="list-row" style="margin-top:8px;">
                    <div><strong>${document.getElementById("fechaServicio").value}</strong> | ${option.text}</div>
                    <span class="badge badge-success">+$${data.subtotal}</span>
                </div>
            `;
            alert("Ítem agregado con éxito al carrito");
        } else alert(data.detail || "Error al añadir ítem");
    } catch (error) { alert("Error de conexión"); }
}

async function cargarMisPlanes() {
    const contenedor = document.getElementById("listaMisPlanes");
    try {
        const response = await fetch(`${API_URL}/planes-viaje/mis-planes`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const planes = await response.json();
        
        contenedor.innerHTML = "";
        if(planes.length === 0) { contenedor.innerHTML = "<p style='color:#64748b;'>No tienes planes creados.</p>"; return; }

        planes.forEach(plan => {
            let itemsHTML = plan.items_agregados.map(i => `
                <div class="list-row">
                    <div><strong>${i.fecha_servicio}</strong> | [${i.tipo_item}] Cant: ${i.cantidad}</div>
                    <span style="color:#16a34a; font-weight:bold;">$${i.subtotal_calculado}</span>
                </div>
            `).join('');
            
            contenedor.innerHTML += `
                <div class="card" style="width:100%; max-width:700px; padding:20px; margin-bottom:20px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="color:#2563eb; font-size:16px;">${plan.nombre_plan} <span class="badge badge-info">${plan.estado}</span></h4>
                        <div class="plan-price">Total Estimado: $${plan.costo_total_estimado}</div>
                    </div>
                    <p style="color:#64748b; font-size:13px; margin:8px 0 15px;">Del ${plan.fecha_inicio} al ${plan.fecha_fin}</p>
                    <h5 style="margin-bottom:8px; font-size:13px; color:#0f172a;">Itinerario / Servicios:</h5>
                    <div class="list">${itemsHTML !== '' ? itemsHTML : '<p style="font-size:12px; color:#64748b;">Sin servicios añadidos.</p>'}</div>
                </div>
            `;
        });
    } catch (error) { contenedor.innerHTML = "<p style='color:red'>Error cargando historial.</p>"; }
}

function cerrarSesion() {
    localStorage.clear();
    const enSubcarpeta = window.location.pathname.includes("/menu_usuario/");
    window.location.href = enSubcarpeta ? "../login.html" : "login.html"; 
}

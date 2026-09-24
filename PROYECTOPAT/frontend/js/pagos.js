const API_URL = "http://127.0.0.1:8000";

let metodoSeleccionadoId = 1; // 1: Tarjeta, 2: PSE, 3: Nequi
let planId = 1; // Por defecto el plan 1
let totalPlan = 0;

// ==========================================
// 1. CARGAR DETALLES DEL PLAN
// ==========================================
document.addEventListener("DOMContentLoaded", async () => {
    // Si viene en la URL como ?id_plan=1 o desde localStorage
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("id_plan")) {
        planId = parseInt(urlParams.get("id_plan"));
    } else if (localStorage.getItem("plan_id_pago")) {
        planId = parseInt(localStorage.getItem("plan_id_pago"));
    }

    try {
        const response = await fetch(`${API_URL}/pagos/plan/${planId}`);
        if (!response.ok) {
            throw new Error("No se pudo obtener la información del plan.");
        }
        const data = await response.json();

        // Renderizar datos del plan
        document.getElementById("planTitulo").textContent = data.nombre_plan;
        if (data.fecha_inicio && data.fecha_fin) {
            document.getElementById("planFechas").textContent = `📅 ${data.fecha_inicio} al ${data.fecha_fin}`;
        }

        // Renderizar lista de servicios
        const listaDiv = document.getElementById("listaServicios");
        listaDiv.innerHTML = "";
        
        if (data.servicios && data.servicios.length > 0) {
            data.servicios.forEach(s => {
                const item = document.createElement("div");
                item.className = "summary-item";
                item.innerHTML = `
                    <span>${s.nombre} (${s.tipo})</span>
                    <strong>$${s.precio.toLocaleString("es-CO")}</strong>
                `;
                listaDiv.appendChild(item);
            });
        }

        totalPlan = data.total;
        document.getElementById("planTotalCOP").textContent = `$${totalPlan.toLocaleString("es-CO")} COP`;
        document.getElementById("btnPagar").innerHTML = `<i class="fa-solid fa-lock"></i> Pagar $${totalPlan.toLocaleString("es-CO")} COP`;

        document.getElementById("resumenCargando").style.display = "none";
        document.getElementById("resumenContenido").style.display = "block";

    } catch (err) {
        console.error(err);
        document.getElementById("resumenCargando").innerHTML = `
            <p style="color: #ef4444;">No se encontró el plan de viaje #${planId}.</p>
            <p style="font-size: 0.8rem;">Cargando monto de prueba de $350.000 COP</p>
        `;
        totalPlan = 350000;
        document.getElementById("planTotalCOP").textContent = `$${totalPlan.toLocaleString("es-CO")} COP`;
        document.getElementById("resumenContenido").style.display = "block";
    }
});

// ==========================================
// 2. CAMBIAR DE MÉTODO (TABS)
// ==========================================
function cambiarMetodo(idMetodo, tabElement) {
    metodoSeleccionadoId = idMetodo;
    document.querySelectorAll(".method-tab").forEach(tab => tab.classList.remove("active"));
    tabElement.classList.add("active");

    // Ocultar todos los formularios
    document.getElementById("formTarjeta").style.display = "none";
    document.getElementById("formPSE").style.display = "none";
    document.getElementById("formNequi").style.display = "none";

    // Mostrar el seleccionado
    if (idMetodo === 1) document.getElementById("formTarjeta").style.display = "block";
    if (idMetodo === 2) document.getElementById("formPSE").style.display = "block";
    if (idMetodo === 3) document.getElementById("formNequi").style.display = "block";
}

// ==========================================
// 3. INICIAR PROCESAMIENTO SIMULADO
// ==========================================
async function iniciarPago() {
    const overlayProcesando = document.getElementById("overlayProcesando");
    const mensajeEstado = document.getElementById("mensajeEstado");

    overlayProcesando.style.display = "flex";
    mensajeEstado.textContent = "Conectando con la entidad bancaria...";

    // Simular los pasos bancarios realistas
    setTimeout(() => {
        mensajeEstado.textContent = "Validando fondos y seguridad...";
    }, 900);

    setTimeout(async () => {
        mensajeEstado.textContent = "Aprobando transacción...";

        try {
            // Llamar al endpoint del backend
            const response = await fetch(`${API_URL}/pagos/procesar`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    id_plan_viaje: planId,
                    id_met_pago: metodoSeleccionadoId,
                    valor_total: totalPlan,
                    titular: document.getElementById("tarjetaTitular").value || "Usuario PAT"
                })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Error en el pago");
            }

            const dataPago = await response.json();

            // Ocultar procesando y mostrar voucher de éxito
            overlayProcesando.style.display = "none";
            document.getElementById("reciboReferencia").textContent = dataPago.referencia_transaccion;
            document.getElementById("reciboMonto").textContent = `$${dataPago.valor_total.toLocaleString("es-CO")} COP`;
            document.getElementById("reciboFecha").textContent = dataPago.fecha_pago;

            document.getElementById("overlayExito").style.display = "flex";

        } catch (error) {
            overlayProcesando.style.display = "none";
            alert("⚠️ " + error.message);
        }
    }, 1800);
}
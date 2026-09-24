import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from sqlalchemy import text

from app.db.session import get_session

router = APIRouter(prefix="/pagos", tags=["Pagos"])

# ==========================================
# ESQUEMAS PYDANTIC
# ==========================================
class MetodoPagoResponse(BaseModel):
    id_met_pago: int
    nombre: str
    descripcion: Optional[str] = None

class ProcesarPagoRequest(BaseModel):
    id_plan_viaje: int
    id_met_pago: int
    valor_total: float
    titular: Optional[str] = None
    metodo_nombre: Optional[str] = None

# ==========================================
# 1. OBTENER MÉTODOS DE PAGO
# ==========================================
@router.get("/metodos", response_model=List[MetodoPagoResponse])
def listar_metodos_pago(session: Session = Depends(get_session)):
    try:
        query = text("SELECT id_met_pago, nombre, descripcion FROM metodo_pago")
        results = session.execute(query).fetchall()
        if results:
            return [{"id_met_pago": r[0], "nombre": r[1], "descripcion": r[2]} for r in results]
    except Exception:
        pass

    return [
        {"id_met_pago": 1, "nombre": "Tarjeta de Crédito / Débito", "descripcion": "Visa, Mastercard, Amex"},
        {"id_met_pago": 2, "nombre": "PSE (Transferencia Bancaria)", "descripcion": "Débito desde cuenta bancaria"},
        {"id_met_pago": 3, "nombre": "Billetera Digital", "descripcion": "Nequi / Daviplata"}
    ]

# ==========================================
# 2. OBTENER INFORMACIÓN DEL PLAN A PAGAR
# ==========================================
@router.get("/plan/{id_plan}")
def obtener_resumen_plan(id_plan: int, session: Session = Depends(get_session)):
    plan_query = text("SELECT * FROM plan_viaje WHERE id_plan_viaje = :id_plan")
    result = session.execute(plan_query, {"id_plan": id_plan})
    plan_row = result.mappings().first()
    
    if not plan_row:
        raise HTTPException(status_code=404, detail="El plan de viaje no existe.")
    
    plan_dict = dict(plan_row)
    nombre_plan = plan_dict.get("nombre") or plan_dict.get("titulo") or f"Plan de Viaje #{id_plan}"
    descripcion = plan_dict.get("descripcion", "Plan turístico personalizado")
    fecha_inicio = str(plan_dict.get("fecha_inicio")) if plan_dict.get("fecha_inicio") else None
    fecha_fin = str(plan_dict.get("fecha_fin")) if plan_dict.get("fecha_fin") else None
    presupuesto = float(plan_dict.get("presupuesto") or 0.0)

    servicios_lista = []
    total_calculado = 0.0

    try:
        detalles_query = text("""
            SELECT s.id_servicio, s.nombre, s.precio_base
            FROM det_plan_viaje dp
            JOIN servicio s ON dp.id_servicio = s.id_servicio
            WHERE dp.id_plan_viaje = :id_plan
        """)
        detalles = session.execute(detalles_query, {"id_plan": id_plan}).fetchall()
        for d in detalles:
            precio = float(d[2]) if d[2] else 0.0
            total_calculado += precio
            servicios_lista.append({
                "id_servicio": d[0],
                "nombre": d[1],
                "precio": precio,
                "tipo": "Servicio Turístico"
            })
    except Exception:
        pass

    if total_calculado == 0 and presupuesto > 0:
        total_calculado = presupuesto
    elif total_calculado == 0:
        total_calculado = 350000.0

    return {
        "id_plan_viaje": id_plan,
        "nombre_plan": nombre_plan,
        "descripcion": descripcion,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "total": total_calculado,
        "servicios": servicios_lista
    }

# ==========================================
# 3. PROCESAR PAGO (PASARELA SIMULADA)
# ==========================================
@router.post("/procesar")
def procesar_pago(datos: ProcesarPagoRequest, session: Session = Depends(get_session)):
    codigo_ref = f"PAT-TX-{uuid.uuid4().hex[:8].upper()}"
    ahora = datetime.now()
    
    try:
        insert_query = text("""
            INSERT INTO pagos (id_plan_viaje, id_met_pago, valor_total, estado, referencia_transaccion, fecha_pago)
            VALUES (:id_plan, :id_met, :valor, 'APROBADO', :ref, :fecha)
        """)
        
        session.execute(insert_query, {
            "id_plan": datos.id_plan_viaje,
            "id_met": datos.id_met_pago,
            "valor": datos.valor_total,
            "ref": codigo_ref,
            "fecha": ahora
        })
        
        try:
            session.execute(
                text("UPDATE plan_viaje SET estado = 'PAGADO' WHERE id_plan_viaje = :id_plan"),
                {"id_plan": datos.id_plan_viaje}
            )
        except Exception:
            pass

        session.commit()
        
        id_pago_query = text("SELECT id_pago FROM pagos WHERE referencia_transaccion = :ref")
        id_creado = session.execute(id_pago_query, {"ref": codigo_ref}).first()
        id_pago = id_creado[0] if id_creado else 1

        return {
            "mensaje": "¡Pago procesado con éxito!",
            "id_pago": id_pago,
            "referencia_transaccion": codigo_ref,
            "id_plan_viaje": datos.id_plan_viaje,
            "valor_total": datos.valor_total,
            "estado": "APROBADO",
            "fecha_pago": ahora.strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al procesar el pago: {str(e)}")
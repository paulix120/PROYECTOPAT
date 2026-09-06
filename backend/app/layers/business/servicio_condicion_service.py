from fastapi import HTTPException, status
from sqlmodel import Session
from app.layers.data.servicio_condicion_repository import ServicioCondicionRepository
from app.layers.data.servicio_repository import ServicioRepository
from app.layers.models.servicio_condicion import ServicioCondicion, ServicioCondicionCreate
from app.layers.models.auth import User
from app.layers.business.servicio_service import ServicioService

class ServicioCondicionService:
    @staticmethod
    def asignar_condicion(db: Session, data: ServicioCondicionCreate, usuario_actual: User):
        prov = ServicioService.validar_permisos_proveedor(db, usuario_actual.id_usu, 1)
        servicio = ServicioRepository.obtener_servicio_por_id(db, data.id_servicio)
        
        if not servicio or servicio.id_prov != prov.id_prov:
            raise HTTPException(status_code=403, detail="El servicio no te pertenece.")

        # Intentar guardar. Si falla es porque ya estaba asignada (por el UNIQUE de la BD)
        try:
            nueva_relacion = ServicioCondicion(id_servicio=data.id_servicio, id_condi=data.id_condi)
            return ServicioCondicionRepository.crear(db, nueva_relacion)
        except Exception:
            raise HTTPException(status_code=400, detail="Esta condición ya está asignada a este servicio.")

    @staticmethod
    def remover_condicion(db: Session, id_servicio_condi: int, usuario_actual: User):
        relacion = ServicioCondicionRepository.obtener_por_id(db, id_servicio_condi)
        if not relacion:
            raise HTTPException(status_code=404, detail="Relación no encontrada.")

        prov = ServicioService.validar_permisos_proveedor(db, usuario_actual.id_usu, 1)
        servicio = ServicioRepository.obtener_servicio_por_id(db, relacion.id_servicio)
        
        if not servicio or servicio.id_prov != prov.id_prov:
            raise HTTPException(status_code=403, detail="No tienes permiso para modificar esto.")

        ServicioCondicionRepository.eliminar(db, relacion)
        return {"mensaje": "Condición removida del servicio exitosamente."}
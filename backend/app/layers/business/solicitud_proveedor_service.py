from fastapi import HTTPException, status
from sqlmodel import Session
from app.layers.data.solicitud_proveedor_repository import SolicitudProveedorRepository
from app.layers.data.proveedor_repository import ProveedorRepository
from app.layers.data.user_repository import UserRepository
from app.layers.models.solicitud_proveedor import SolicitudProveedor, SolicitudProveedorCreate, SolicitudRevision, SolicitudTpServicio
from app.layers.models.proveedor import Proveedor, ProveedorTpServicio
from app.layers.models.auth import User

class SolicitudProveedorService:
    
    @staticmethod
    def crear_solicitud(db: Session, data: SolicitudProveedorCreate, usuario_actual: User):
        if usuario_actual.id_rol == 3: # 3 = Proveedor (Corregido según tu BD)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya eres un proveedor activo.")

        if not data.tipos_servicio_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Debes solicitar al menos un tipo de servicio.")

        solicitudes_previas = SolicitudProveedorRepository.obtener_por_usuario(db, usuario_actual.id_usu)
        for sol in solicitudes_previas:
            if sol.estado == "EN_REVISION":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ya tienes una solicitud en revisión.")

        nueva_solicitud = SolicitudProveedor(
            id_usu=usuario_actual.id_usu,
            nit=data.nit.strip(),
            razon_social=data.razon_social.strip(),
            telefono_contacto=data.telefono_contacto.strip(),
            cuenta_bancaria=data.cuenta_bancaria.strip(),
            banco=data.banco.strip(),
            estado="EN_REVISION"
        )
        solicitud_guardada = SolicitudProveedorRepository.crear(db, nueva_solicitud)

        for id_servicio in set(data.tipos_servicio_ids):
            SolicitudProveedorRepository.agregar_servicio_solicitado(
                db, SolicitudTpServicio(id_sp=solicitud_guardada.id_sp, id_tp_serv=id_servicio)
            )

        return solicitud_guardada

    @staticmethod
    def revisar_solicitud(db: Session, id_sp: int, data: SolicitudRevision):
        solicitud = SolicitudProveedorRepository.obtener_por_id(db, id_sp)
        
        if not solicitud:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitud no encontrada.")
        if solicitud.estado != "EN_REVISION":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esta solicitud ya fue procesada.")
        if data.estado not in ["APROBADA", "RECHAZADA"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El estado debe ser APROBADA o RECHAZADA.")

        solicitud.estado = data.estado
        solicitud.observaciones = data.observaciones
        SolicitudProveedorRepository.actualizar(db, solicitud)

        if data.estado == "APROBADA":
            nuevo_proveedor = Proveedor(id_usu=solicitud.id_usu, id_sp=solicitud.id_sp, estado="ACTIVO")
            proveedor_guardado = ProveedorRepository.crear(db, nuevo_proveedor)

            servicios_pedidos = SolicitudProveedorRepository.obtener_servicios_de_solicitud(db, solicitud.id_sp)
            for serv in servicios_pedidos:
                ProveedorRepository.agregar_servicio_autorizado(
                    db, ProveedorTpServicio(id_prov=proveedor_guardado.id_prov, id_tp_serv=serv.id_tp_serv)
                )

            usuario = UserRepository.obtener_por_id(db, solicitud.id_usu)
            if usuario:
                usuario.id_rol = 3 # 3 = Proveedor (Corregido según tu BD)
                UserRepository.actualizar(db, usuario)

        return {"mensaje": f"Solicitud {data.estado} exitosamente."}

    @staticmethod
    def listar_todas(db: Session):
        return SolicitudProveedorRepository.obtener_todas(db)
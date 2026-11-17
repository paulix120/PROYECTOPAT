from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.layers.data.solicitud_proveedor_repository import SolicitudProveedorRepository
from app.layers.data.proveedor_repository import ProveedorRepository
from app.layers.data.user_repository import UserRepository
from app.layers.models.solicitud_proveedor import (
    SolicitudProveedor,
    SolicitudProveedorCreate,
    SolicitudRevision,
    SolicitudTpServicio,
)
from app.layers.models.proveedor import Proveedor, ProveedorTpServicio
from app.layers.models.auth import User


class SolicitudProveedorService:

    @staticmethod
    def crear_solicitud(db: Session, data: SolicitudProveedorCreate, usuario_actual: User):
        if usuario_actual.id_rol == 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya eres un proveedor activo.",
            )

        if not data.tipos_servicio_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debes solicitar al menos un tipo de servicio.",
            )

        solicitudes_previas = SolicitudProveedorRepository.obtener_por_usuario(db, usuario_actual.id_usu)
        for sol in solicitudes_previas:
            if sol.estado == "EN_REVISION":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya tienes una solicitud en revisión.",
                )

        nit_limpio = data.nit.strip()
        if SolicitudProveedorRepository.obtener_por_nit(db, nit_limpio):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una solicitud registrada con ese NIT.",
            )

        nueva_solicitud = SolicitudProveedor(
            id_usu=usuario_actual.id_usu,
            nit=nit_limpio,
            razon_social=data.razon_social.strip(),
            telefono_contacto=data.telefono_contacto.strip(),
            cuenta_bancaria=data.cuenta_bancaria.strip(),
            banco=data.banco.strip(),
            estado="EN_REVISION",
        )

        try:
            solicitud_guardada = SolicitudProveedorRepository.crear(db, nueva_solicitud, commit=False)

            for id_servicio in set(data.tipos_servicio_ids):
                SolicitudProveedorRepository.agregar_servicio_solicitado(
                    db,
                    SolicitudTpServicio(id_sp=solicitud_guardada.id_sp, id_tp_serv=id_servicio),
                    commit=False,
                )

            db.commit()
            db.refresh(solicitud_guardada)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uno o más tipos de servicio seleccionados no son válidos o el NIT ya existe.",
            )
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al registrar la solicitud de proveedor.",
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estado debe ser APROBADA o RECHAZADA.",
            )

        try:
            solicitud.estado = data.estado
            solicitud.observaciones = data.observaciones
            SolicitudProveedorRepository.actualizar(db, solicitud, commit=False)

            if data.estado == "APROBADA":
                proveedor_existente = ProveedorRepository.obtener_por_usuario(db, solicitud.id_usu)
                if proveedor_existente:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Este usuario ya está registrado como proveedor.",
                    )

                nuevo_proveedor = Proveedor(
                    id_usu=solicitud.id_usu,
                    id_sp=solicitud.id_sp,
                    estado="ACTIVO",
                )
                proveedor_guardado = ProveedorRepository.crear(db, nuevo_proveedor, commit=False)

                servicios_pedidos = SolicitudProveedorRepository.obtener_servicios_de_solicitud(
                    db, solicitud.id_sp
                )
                for serv in servicios_pedidos:
                    ProveedorRepository.agregar_servicio_autorizado(
                        db,
                        ProveedorTpServicio(id_prov=proveedor_guardado.id_prov, id_tp_serv=serv.id_tp_serv),
                        commit=False,
                    )

                usuario = UserRepository.obtener_por_id(db, solicitud.id_usu)
                if not usuario:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario asociado a la solicitud no encontrado.",
                    )
                usuario.id_rol = 3  # 3 = Proveedor
                UserRepository.actualizar(db, usuario, commit=False)

            db.commit()
        except HTTPException:
            db.rollback()
            raise
        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al procesar la revisión de la solicitud.",
            )

        return {"mensaje": f"Solicitud {data.estado} exitosamente."}

    @staticmethod
    def listar_todas(db: Session):
        return SolicitudProveedorRepository.obtener_todas(db)
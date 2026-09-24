from sqlmodel import Session
from fastapi import HTTPException
from app.layers.data.base_repository import BaseRepository
from app.layers.models.auth import User
from app.layers.models.servicio import Servicio
from app.layers.business.servicio_service import ServicioService 
from app.layers.models.servicio_transporte import ServicioTransporte, TransporteCreate, TransporteUpdate
from app.layers.data.servicio_transporte_repository import ServicioTransporteRepository

class ServicioTransporteService:
    @staticmethod
    def crear(db: Session, data: TransporteCreate, usuario: User):
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 4) 
        nuevo_padre = Servicio(nombre=data.nombre, descripcion=data.descripcion, id_tp_serv=4, id_tp_turi=data.id_tp_turi, id_gama=data.id_gama, id_prov=prov.id_prov, id_ubi=data.id_ubi)
        padre_guardado = BaseRepository.guardar(db, nuevo_padre)
        
        nuevo_hijo = ServicioTransporte(
            id_servicio=padre_guardado.id_servicio, 
            tipo_vehiculo=data.tipo_vehiculo, 
            capacidad_pasajeros=data.capacidad_pasajeros, 
            vlr_km=data.vlr_km, 
            tarifa_base=data.tarifa_base, 
            horario_servicio=data.horario_servicio,
            es_ruta_programada=data.es_ruta_programada,
            id_origen=data.id_origen,
            id_destino=data.id_destino,
            fecha_salida=data.fecha_salida
        )
        BaseRepository.guardar(db, nuevo_hijo)
        return {"mensaje": "Transporte creado", "id_servicio": padre_guardado.id_servicio}

    @staticmethod
    def listar(db: Session):
        datos = ServicioTransporteRepository.listar(db)
        return [{"servicio_base": p, "detalle": h} for p, h in datos]

    @staticmethod
    def actualizar(db: Session, id_servicio: int, data: TransporteUpdate, usuario: User):
        padre = ServicioTransporteRepository.obtener_padre(db, id_servicio)
        if not padre or padre.id_tp_serv != 4: raise HTTPException(404, "Servicio no encontrado.")
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 4)
        if padre.id_prov != prov.id_prov: raise HTTPException(403, "No te pertenece.")

        hijo = ServicioTransporteRepository.obtener_hijo(db, id_servicio)
        datos = data.model_dump(exclude_unset=True)
        for k in ["nombre", "descripcion", "id_tp_turi", "id_gama", "id_ubi"]:
            if k in datos: setattr(padre, k, datos[k])
            
        # Agregamos los nuevos campos para que se puedan actualizar
        for k in ["tipo_vehiculo", "capacidad_pasajeros", "vlr_km", "tarifa_base", "horario_servicio", "es_ruta_programada", "id_origen", "id_destino", "fecha_salida"]:
            if k in datos: setattr(hijo, k, datos[k])

        BaseRepository.actualizar(db, padre)
        BaseRepository.actualizar(db, hijo)
        return {"mensaje": "Transporte actualizado"}

    @staticmethod
    def eliminar(db: Session, id_servicio: int, usuario: User):
        padre = ServicioTransporteRepository.obtener_padre(db, id_servicio)
        if not padre or padre.id_tp_serv != 4: raise HTTPException(404, "Servicio no encontrado.")
        prov = ServicioService.validar_permisos_proveedor(db, usuario.id_usu, 4)
        if padre.id_prov != prov.id_prov: raise HTTPException(403, "No te pertenece.")
            
        padre.activo = False
        BaseRepository.actualizar(db, padre)
        return {"mensaje": "Transporte eliminado correctamente."}